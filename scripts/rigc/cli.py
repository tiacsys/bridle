# Copyright (c) 2026 TiaC Systems
# SPDX-License-Identifier: Apache-2.0
"""rigc CLI -- the front door.

`expand <rig_yml>` takes --shield-dir* --board --board-dts --build-info
--bindings-dir* --include-dir* --connector-dir* --revision --variant
--out-dir (* = repeatable). --board-dts/--build-info/--bindings-dir feed
the board reader (board/); --shield-dir/
--include-dir/--connector-dir/--revision/--variant feed the loader.
--board feeds the loader too, and is the ONLY source of `rig.board`
(rig.yml has no `board:` key of its own): omitted, `rig.board` is simply
"" -- legal through the loader, and a diagnostic only once this file is
about to read a real board devicetree (see the board-empty check right
before load_board, below). A clean analysis emits the rig
artifacts (`emitter.emit`) plus the build-glue handoff
(`emitter.context.render`) through the one writer (`emitter.write_
artifacts`) and returns 0.
main(argv) -> int is callable in-process, so the argv contract has
subprocess-free unit tests.

The positional `rig` and `--promote <shield-name>` are mutually exclusive
alternatives for the SAME slot: a promoted shield has no rig.yml on disk,
so `--promote` makes `_expand` synthesize `promote.promote_shield`'s own
pair straight into this run's workdir and load THAT by path -- the
loader, deps, diagnostics and emitter never learn the difference.
`--revision` alongside `--promote` means the SHIELD's own revision (baked
into the synthesized content file), never a rig-level axis -- a promoted
rig declares no revisions of its own, so it is never forwarded to
`loader.load`.

`--promote`'s value may also be a `;`-separated LIST of shield targets:
`promote.promote_shield_list` synthesizes the N-instance pair instead,
and `--revision` plays no part (each element carries its own `@rev`
inline in the list text, since one scalar flag cannot carry N
per-element revisions).

Exit vocabulary: 0 accept, 1 rejected input, 2 usage error (argparse's
own), 3 not implemented (see unimplemented.py).

**The workdir lives inside `--out-dir`, as `<out-dir>/rigc-generated`**,
never in /tmp, so it inherits the owning build directory's lifetime:
`west build -p`, `rm -rf build/` and pytest's own tmp_path retention each
reap it for free. Its name is DETERMINISTIC (no mkdtemp suffix), it is
wiped on entry so a previous run's intermediates can never be mistaken
for this run's, and it is KEPT on every exit -- it is the only record of
what this run actually fed its own parsers (a promoted shield's
synthesized rig.yml/content pair, each shield's `.dts` and its
cpp-preprocessed `.pre`, the board's included), and an accepted run is
exactly the run whose emitted overlay someone later questions.

**The workdir NAME is NOT cosmetic**: the test harness's own
`normalize()` (`tests/integration/conftest.py`'s `_WORKDIR_RE`) strips a
path ending in `rigc-generated` to a stable placeholder before comparing
rendered stderr against a golden. A cpp-preprocess-failure detail (e.g.
`param-missing-header`) embeds this path verbatim inside gcc's own stderr
text, so the trailing component MUST stay literally `rigc-generated` or
the comparison sees an un-normalized absolute path and byte-mismatches a
golden that has nothing else wrong with it."""

from __future__ import annotations

import argparse
import logging
import os
import shutil
import sys

from . import analyzer, loader, promote
from .board import BuildRecipe, load_board, recipe_from_build_info
from .deps import union as deps_union
from .diag import Diagnostic, LoadError, has_errors, render
from .diag import error as diag_error
from .emitter import context, emit, write_artifacts
from .model import ConnectorType
from .registry import load_types
from .unimplemented import Unimplemented

log = logging.getLogger(__name__)

#: The workdir's name inside --out-dir. Load-bearing, not cosmetic: the
#: test harness's own normalizer (tests/integration/conftest.py
#: _WORKDIR_RE) strips a path ending in this to a stable placeholder
#: before comparing rendered stderr against a byte-exact golden. See this
#: module's docstring.
WORKDIR_NAME = "rigc-generated"

#: Marks a handler `_configure_logging` itself installed, so a repeated
#: `main()` call (every in-process unit test makes one) never accumulates
#: a second stderr handler -- each call starts from a clean slate and
#: re-derives the CURRENT environment's answer.
_OWN_HANDLER = "_rigc_cli_handler"


def _configure_logging(verbosity: int = 0) -> None:
    """Attach a real stderr handler to the `rigc` logger tree ONLY when
    asked to, either via `-v`/`-vv` on the command line (`verbosity` 1 or
    2+, INFO or DEBUG respectively) or, when neither flag was given, via
    `RIGC_LOG=<level>` in the environment -- otherwise the package root's
    `NullHandler` (rigc/__init__.py) is the only handler and nothing
    reaches stderr, Python's own `lastResort` notwithstanding. The CLI
    flag wins over the environment when both are present, since it is the
    more explicit, per-invocation request.

    Enabling this during a golden-comparing run BREAKS the comparison BY
    DESIGN: every enabled record lands on the exact same stderr stream the
    renderer's own bytes are compared against. Called from `main()` after
    argv is parsed, so an in-process unit test can pass a verbosity or
    monkeypatch the environment and observe the effect without a
    subprocess."""
    root = logging.getLogger("rigc")
    for h in list(root.handlers):
        if getattr(h, _OWN_HANDLER, False):
            root.removeHandler(h)
    level_name: str | None
    if verbosity >= 2:
        level_name = "DEBUG"
    elif verbosity == 1:
        level_name = "INFO"
    else:
        level_name = os.environ.get("RIGC_LOG")
    if level_name is None:
        return
    handler = logging.StreamHandler(sys.stderr)
    setattr(handler, _OWN_HANDLER, True)
    handler.setFormatter(
        logging.Formatter("%(asctime)s %(levelname)s %(name)s:%(funcName)s: %(message)s")
    )
    root.addHandler(handler)
    root.setLevel(level_name.upper())


def _resolve_recipe(
    include_dirs: list[str] | None,
    bindings_dirs: list[str] | None,
    build_info: str | None,
) -> BuildRecipe | None:
    """--build-info wins if given (one path, no per-dir bookkeeping); else
    an explicit --include-dir/--bindings-dir pair, if either was given;
    else None -- the caller (load_board) turns a still-None recipe
    into a clear diagnostic once/if it is actually needed, rather than
    this function guessing at "nothing usable"."""
    if build_info is not None:
        return recipe_from_build_info(os.path.abspath(build_info))
    if include_dirs or bindings_dirs:
        return BuildRecipe(
            include_dirs=[os.path.abspath(d) for d in (include_dirs or [])],
            bindings_dirs=[os.path.abspath(d) for d in (bindings_dirs or [])],
        )
    return None


def build_parser() -> argparse.ArgumentParser:
    """The frozen argv surface. Public so the argv contract gets unit
    tests without a subprocess."""
    ap = argparse.ArgumentParser(
        prog="rigc",
        description="Compile a rig file: reject invalid input or emit the "
        "devicetree overlay + build artifacts.",
        allow_abbrev=False,
    )
    sub = ap.add_subparsers(dest="command", required=True)
    p = sub.add_parser(
        "expand",
        help="run one rig through the pipeline and write the outputs to --out-dir",
    )
    rig_or_promote = p.add_mutually_exclusive_group(required=True)
    rig_or_promote.add_argument(
        "rig",
        nargs="?",
        default=None,
        help="path to the rig's metadata file, rig.yml",
    )
    rig_or_promote.add_argument(
        "--promote",
        default=None,
        metavar="TARGET",
        help="a promotion TARGET to expand in place of a real rig.yml: "
        "<shield>[@rev][:<key>=<value>...], or a `;`-separated list of "
        "those -- synthesizes promote.promote_shield's own rig.yml/"
        "content pair into this run's workdir and loads that. Mutually "
        "exclusive with the positional rig",
    )
    p.add_argument(
        "--shield-dir",
        dest="shield_dirs",
        action="append",
        metavar="DIR",
        default=None,
        help="a shield-library root; repeatable",
    )
    p.add_argument(
        "--board",
        default=None,
        metavar="NAME",
        help="the board to build against, in Zephyr's own "
        "<board>/<soc>/<variant> spelling -- the ONLY source of a rig's "
        "board (no rig file declares one). Omitted, the rig loads with "
        "an empty board, which every stage but the board reader accepts",
    )
    p.add_argument("--board-dts", default=None, help="the rig's board's own .dts")
    p.add_argument(
        "--include-dir",
        dest="include_dirs",
        action="append",
        metavar="DIR",
        default=None,
        help="a cpp -I directory; repeatable",
    )
    p.add_argument(
        "--bindings-dir",
        dest="bindings_dirs",
        action="append",
        metavar="DIR",
        default=None,
        help="an edtlib bindings directory; repeatable",
    )
    p.add_argument(
        "--connector-dir",
        dest="connector_dirs",
        action="append",
        metavar="DIR",
        default=None,
        help="a connector-type root; repeatable",
    )
    p.add_argument(
        "--build-info",
        default=None,
        metavar="PATH",
        help="recover the cpp/bindings recipe from a real build's build_info.yml",
    )
    p.add_argument(
        "--revision",
        default=None,
        metavar="REV",
        help="the selected revision axis value",
    )
    p.add_argument(
        "--variant",
        default=None,
        metavar="NAME",
        help="the selected variant axis value",
    )
    p.add_argument("--out-dir", required=True, help="directory to write the emitted artifacts into")
    p.add_argument(
        "-v",
        "--verbose",
        action="count",
        default=0,
        help="-v for INFO logging on stderr, -vv for DEBUG; overrides RIGC_LOG when given",
    )
    return ap


def _abspath_dirs(dirs: list[str] | None) -> list[str] | None:
    """Absolutize a repeatable --xxx-dir flag's value, or None when the
    flag was never given -- the identical pattern every repeatable
    directory option in this module's argv surface (--shield-dir,
    --connector-dir, --include-dir) follows. Returns a fresh list the
    caller owns."""
    return [os.path.abspath(d) for d in dirs] if dirs else None


def _reject(diags: list[Diagnostic]) -> int:
    """Render diags to stderr and return the reject exit code -- the ONE
    place every `_expand()` rejection funnels through, so the verdict log
    line and the exit code can never drift apart."""
    log.info("verdict: rejected, exit 1")
    print(render(diags), file=sys.stderr)
    return 1


def _materialize_promotion(
    args: argparse.Namespace,
    workdir: str,
    shield_dirs: list[str] | None,
    types: dict[str, ConnectorType],
    include_dirs: list[str] | None,
) -> tuple[str, str | None] | list[Diagnostic]:
    """--promote materializes promote.promote_shield's own two
    documents into THIS run's workdir and loads them by path --
    everything past this point (loader, deps, diagnostics, emitter)
    runs on a real rig.yml on a real path, exactly as for an
    authored one. The workdir is kept on every exit, so a promoted
    shield always leaves the synthesized pair on disk -- the evidence a
    user needs to look at, at a path inside the workdir the rendered
    diagnostic itself names, whether the run rejected or accepted.

    Returns the written rig_path and the revision `_expand` should load
    with, or the diagnostics naming why the promotion target failed to
    parse. The returned revision is always None on success: the
    SHIELD's own revision is baked into the synthesized content file's
    `shield:` reference, and a promoted rig declares no revision axis
    of its own, so nothing is forwarded to loader.load as a rig-level
    selection. Reads args.promote/args.revision only; shield_dirs is
    the caller's already-absolutized --shield-dir list, and `types` the
    registry the caller already built from --connector-dir/--include-dir,
    and `include_dirs` that same --include-dir list, which the template's
    own cpp run needs directly. All three are read-only, and none is
    optional here on purpose: the
    promotion path parses a shield template, and letting it fall back to
    registry.load_types()'s module-relative default is exactly how an
    explicit --connector-dir got ignored. The caller owns the returned
    path and diagnostics."""
    # --promote's value is the promotion TARGET, not a bare
    # shield name: `<shield>[@rev][:<key>=<value>...]`, or a
    # `;`-separated LIST of such targets. cmake forwards list_rigs'
    # `{PROMOTED}` here opaquely and never parses it, so this is the
    # one parser for the option grammar no matter how many options
    # -- or elements -- it grows.
    if ";" in args.promote:
        elements = promote.parse_promotion_list(args.promote, shield_dirs, types, include_dirs)
        if isinstance(elements, str):
            return [diag_error("lang-promote-opts", elements)]
        promoted = promote.promote_shield_list(elements)
    else:
        shield_name, _, opt_text = args.promote.partition(":")
        # Resolved here, ahead of parse_promotion_opts's own
        # slot-validation grammar (a bare socket= on a plural shield,
        # a socket.<slot>= on a single-plug one, an unknown slot).
        # check_promotable is deliberately NOT called here:
        # list_rigs.py/west_commands/rigs.py already validate
        # promotability before ever forwarding a target this far, and
        # this is the one entry point every OTHER caller's --promote
        # value already passes through -- duplicating the check here
        # would be a second authority for the same fact.
        resolved = promote.resolve_for_promotion(shield_name, shield_dirs, types, include_dirs)
        opts = promote.parse_promotion_opts(opt_text or None, args.promote, resolved)
        if isinstance(opts, str):
            # No SourceRef: the offending text is argv, not a file,
            # and the message already quotes the target verbatim.
            return [diag_error("lang-promote-opts", opts)]
        promoted = promote.promote_shield(
            shield_name,
            args.revision,
            socket=opts.fixed.get("socket"),
            sockets=opts.sockets or None,
            config=opts.config or None,
            params=opts.params or None,
        )
    rig_path = os.path.join(workdir, "rig.yml")
    with open(rig_path, "w") as f:
        f.write(promoted.rig_yml)
    with open(os.path.join(workdir, promoted.content_name), "w") as f:
        f.write(promoted.content)
    return rig_path, None


def _expand(args: argparse.Namespace) -> int:
    # Absolute up front, like the whole pipeline expects: the cmake seam
    # runs this CLI from the build dir, so inputs must be cwd-independent
    # -- and the diagnostics' message paths are spec'd absolute. A
    # --promote target has no path yet (it is materialized into the
    # workdir below, once one exists), so this stays None until then.
    rig_path = os.path.abspath(args.rig) if args.rig is not None else None
    shield_dirs = _abspath_dirs(args.shield_dirs)
    connector_dirs = _abspath_dirs(args.connector_dirs)
    # header_dirs is the RAW --include-dir list, threaded to every cpp
    # invocation this run makes: the connector-type registry's <type>.h
    # lookup, every .shield template's own translation unit, and a
    # shield device's own shield,param-includes/per-instance-parameter
    # resolution -- one list serves all three.
    header_dirs = _abspath_dirs(args.include_dirs)
    board_dts = os.path.abspath(args.board_dts) if args.board_dts else None

    # Wiped on entry so a previous run's intermediates can never be
    # mistaken for this run's; see the module docstring for the
    # workdir's location, naming and retention rules.
    out_dir = os.path.abspath(args.out_dir)
    log.info("out-dir: %s", out_dir)
    workdir = os.path.join(out_dir, WORKDIR_NAME)
    shutil.rmtree(workdir, ignore_errors=True)
    os.makedirs(workdir)
    log.info("workdir: %s", workdir)
    revision = args.revision

    try:
        # Resolved here and threaded down, replacing what would otherwise
        # be a re-glob/re-parse per caller. types_deps rides RIG_DEPENDS
        # below (every connector-type YAML and index header this run's
        # registry actually read). Inside this same try: load_types can
        # itself raise LoadError now (lang-connector-root, registry.py's
        # own docstring) when no --connector-dir was given AND its
        # dev/test fallback does not exist either -- a standalone
        # invocation missing the flag, or a workspace where rigc's
        # source no longer sits next to the real connector types. That
        # must reject cleanly through the SAME path as every other
        # loader-stage failure, never as an uncaught exception.
        types, types_deps = load_types(connector_dirs=connector_dirs, header_dirs=header_dirs)
        # Promotion is materialized INSIDE this try, and AFTER the registry
        # exists, for one reason each. After: resolving a promotion target
        # parses the shield template, which needs the connector types this
        # run was given -- reaching load_types() a second time on its own
        # would silently take the module-relative fallback and read
        # production bindings straight past an explicit --connector-dir.
        # Inside: a promotion that hits a bad connector root must then
        # reject through the same LoadError path as every other
        # loader-stage failure.
        if args.promote is not None:
            result = _materialize_promotion(args, workdir, shield_dirs, types, header_dirs)
            if isinstance(result, list):
                return _reject(result)
            rig_path, revision = result
        # argparse's mutually exclusive group guarantees one of rig/--promote
        assert rig_path is not None
        rig, diags, rig_deps = loader.load(
            rig_path,
            workdir,
            shield_dirs=shield_dirs,
            revision=revision,
            variant=args.variant,
            board=args.board,
            types=types,
            include_dirs=header_dirs,
        )
    except LoadError as e:
        # The registry load above, or loader.load() itself -- the latter
        # already converts its own LoadErrors to the normal return shape
        # internally in the common case, so this is mostly a backstop for
        # it, but the FIRST-line catch for the former.
        return _reject(list(e.diags))
    if rig is None or has_errors(diags):
        return _reject(diags)

    # Pass 1: board reading. The recipe is resolved HERE, not up front
    # alongside the other inputs: it opens a real file (--build-info)
    # eagerly, and doing that before the loader even runs would turn a
    # caller's typo'd --build-info path into an unhandled crash on a
    # rig that was going to be rejected anyway (never a traceback, the
    # reject convention) -- resolving it only once the loader has
    # already accepted is what load_board's own "no usable
    # recipe" diagnostic exists to report cleanly instead.
    #
    # rig.board is "" whenever this run injected none: the loader
    # itself never requires one, since a rig's topology never needed a
    # board to assemble. This is the one place that still does --
    # passing "" straight to load_board would search for a
    # board literally named "" and report the confusing "unknown board
    # ''" rather than the honest fact that none was given, so it is
    # caught here first, before load_board ever runs. Unlike a `lang-*`
    # loader finding, this has no rig.yml line to blame (there is no
    # `board:` key to point at) -- phys-board, no refs, matching every
    # other board-reading diagnostic's own unanchored shape.
    if not rig.board:
        return _reject(
            diags
            + [
                diag_error(
                    "phys-board",
                    f"rig '{rig.name}': no board given -- a rig has no board "
                    "of its own any more (board: left rig.yml's grammar "
                    "entirely); pass --board <name>",
                )
            ]
        )
    #
    # load_board's own diagnostics carry no `rig`-side src ref
    # (a "phys-board" finding is never anchored to a rig.yml line), so
    # they simply extend the diags list gathered so far: a rejection
    # here is never a reason to drop the loader's own (empty, since
    # has_errors already returned above) findings.
    recipe = _resolve_recipe(args.include_dirs, args.bindings_dirs, args.build_info)
    board, board_diags, board_deps = load_board(
        rig.board, workdir, board_dts=board_dts, recipe=recipe
    )
    diags += board_diags
    if board is None:
        return _reject(diags)

    # Pass 2: the analyzer -- mating/socket resolution, nets,
    # addresses, CS, wires, labels.
    solved, analyzer_diags = analyzer.analyze(rig, board, types)
    diags += analyzer_diags
    if has_errors(diags):
        return _reject(diags)

    # Accept: emit the rig artifacts (emitter.emit -- strong contract,
    # cannot fail here) plus the build-glue handoff (context.render,
    # kept a SEPARATE value function so cli.py never builds
    # context.cmake's text itself), then ONE writer for everything.
    # RIG_DEPENDS is every real source-tree
    # file this run actually touched: the connector-type registry,
    # the loader's own closure (rig.yml, its content file, qualifier
    # delta fragments, every shield resolution across all three
    # topology stages -- eager scan breadth and resolution history
    # alike, see loader.load's own docstring), and the board's .dts.
    all_deps = deps_union(types_deps, rig_deps, board_deps)
    artifacts = emit(rig, solved, types, workdir, include_dirs=header_dirs)
    artifacts["context.cmake"] = context.render(rig, all_deps)
    write_artifacts(out_dir, artifacts)

    log.info("verdict: accepted, exit 0")
    if diags:  # warnings only -- errors would have exited above
        print(render(diags), file=sys.stderr)
    return 0


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    _configure_logging(getattr(args, "verbose", 0))
    log.info("argv: %s", vars(args))
    try:
        if args.command == "expand":
            return _expand(args)
        raise Unimplemented(f"command '{args.command}'")  # unreachable:
        # add_subparsers(required=True) already usage-errors on anything else
    except Unimplemented as e:
        log.info("verdict: refusal (%s), exit 3", e.what)
        print(f"rigc: not implemented: {e.what}", file=sys.stderr)
        return 3


if __name__ == "__main__":
    sys.exit(main())
