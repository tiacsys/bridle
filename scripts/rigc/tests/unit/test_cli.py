# Copyright (c) 2026 TiaC Systems
# SPDX-License-Identifier: Apache-2.0
"""Unit: cli — the frozen front door.

Two contracts live here, both cli.py's own: the frozen argv surface
(`expand <rig_yml>` + the nine options, asserted in-process via
build_parser()/main(), no subprocess) and the loud-refusal behaviour of
unimplemented paths (exit 3, single-line `rigc: not implemented: <what>`
on stderr, never a traceback, never exit 1, never a silent accept).

Every `main([...])` call below passes an EXPLICIT `--shield-dir` pointing
at an empty/nonexistent directory (`_no_shields`) -- shield-dir scanning
runs unconditionally, before rig.yml even opens, and
the CLI's own bare-invocation fallback is the vendored PRODUCTION shield
library (`loader/library.py`'s `SHIELDS_DIR`, direct-API/test use only per
its own docstring). Omitting `--shield-dir` here would make these unit
tests silently scan and cpp-parse real repo shield content -- a
subprocess call and a hermeticity violation both, so every call site
supplies one (`glob.glob` on a directory that does not exist just returns
`[]`, no error -- the directory need not exist, only be named).
"""

from __future__ import annotations

import argparse
import logging
import re
from pathlib import Path
from textwrap import dedent

import pytest

from rigc import cli
from rigc.cli import _configure_logging, build_parser, main


def _no_shields(tmp_path: Path) -> list[str]:
    """Point EVERY library root that has a production fallback at an
    empty directory -- --shield-dir alone is not enough: --connector-dir
    has the identical None-falls-back-to-the-real-tree shape
    (cli._expand -> load_types -> registry.BINDINGS), so omitting it
    would let the unit suite read production connector bindings and
    headers. A unit test touches NO production data."""
    empty = tmp_path / "no_library_here"
    return ["--shield-dir", str(empty), "--connector-dir", str(empty), "--include-dir", str(empty)]


def _parse(extra: list[str]) -> argparse.Namespace:
    return build_parser().parse_args(["expand", "rig.yml", "--out-dir", "out", *extra])


# --------------------------------------------------------- the argv surface


def test_positional_rig_and_out_dir() -> None:
    args = _parse([])
    assert args.command == "expand"
    assert args.rig == "rig.yml"
    assert args.out_dir == "out"


def test_defaults_are_none() -> None:
    args = _parse([])
    assert args.shield_dirs is None
    assert args.board is None
    assert args.board_dts is None
    assert args.build_info is None
    assert args.bindings_dirs is None
    assert args.include_dirs is None
    assert args.connector_dirs is None
    assert args.revision is None
    assert args.variant is None
    assert args.verbose == 0
    assert args.promote is None


# ------------------------------------------- --promote / positional exclusion


def test_promote_and_positional_rig_are_mutually_exclusive() -> None:
    with pytest.raises(SystemExit) as e:
        build_parser().parse_args(
            ["expand", "rig.yml", "--promote", "some_shield", "--out-dir", "out"]
        )
    assert e.value.code == 2


def test_neither_rig_nor_promote_given_is_a_usage_error() -> None:
    with pytest.raises(SystemExit) as e:
        build_parser().parse_args(["expand", "--out-dir", "out"])
    assert e.value.code == 2


def test_promote_alone_parses() -> None:
    args = build_parser().parse_args(
        ["expand", "--promote", "adafruit_data_logger", "--out-dir", "out"]
    )
    assert args.rig is None
    assert args.promote == "adafruit_data_logger"


def test_repeatable_options_accumulate_in_order() -> None:
    args = _parse(
        [
            "--shield-dir",
            "s1",
            "--shield-dir",
            "s2",
            "--bindings-dir",
            "b1",
            "--bindings-dir",
            "b2",
            "--include-dir",
            "i1",
            "--include-dir",
            "i2",
            "--connector-dir",
            "c1",
            "--connector-dir",
            "c2",
        ]
    )
    assert args.shield_dirs == ["s1", "s2"]
    assert args.bindings_dirs == ["b1", "b2"]
    assert args.include_dirs == ["i1", "i2"]
    assert args.connector_dirs == ["c1", "c2"]


def test_single_valued_options() -> None:
    args = _parse(
        [
            "--board",
            "some_board/soc/rig",
            "--board-dts",
            "b.dts",
            "--build-info",
            "bi.yml",
            "--revision",
            "2",
            "--variant",
            "b",
        ]
    )
    assert args.board == "some_board/soc/rig"
    assert args.board_dts == "b.dts"
    assert args.build_info == "bi.yml"
    assert args.revision == "2"
    assert args.variant == "b"


def test_verbose_counts_repeats() -> None:
    assert _parse([]).verbose == 0
    assert _parse(["-v"]).verbose == 1
    assert _parse(["-vv"]).verbose == 2
    assert _parse(["-v", "-v"]).verbose == 2
    assert _parse(["--verbose", "--verbose", "--verbose"]).verbose == 3


def test_out_dir_is_required() -> None:
    with pytest.raises(SystemExit) as e:
        build_parser().parse_args(["expand", "rig.yml"])
    assert e.value.code == 2


def test_subcommand_is_required() -> None:
    with pytest.raises(SystemExit) as e:
        build_parser().parse_args([])
    assert e.value.code == 2


def test_unknown_option_is_a_usage_error() -> None:
    with pytest.raises(SystemExit) as e:
        _parse(["--no-such-flag"])
    assert e.value.code == 2


def test_unknown_command_is_a_usage_error() -> None:
    with pytest.raises(SystemExit) as e:
        build_parser().parse_args(["translate", "rig.yml"])
    assert e.value.code == 2


def test_main_is_callable_in_process(tmp_path: Path) -> None:
    """main(argv) -> int -- returns rather than raises for every
    non-usage outcome (here: an unimplemented path, exit code 3)."""
    ret = main(
        [
            "expand",
            str(tmp_path / "no-such-rig.yml"),
            "--out-dir",
            str(tmp_path / "out"),
            *_no_shields(tmp_path),
        ]
    )
    assert isinstance(ret, int)
    assert ret == 3


def test_board_reading_options_are_now_live(tmp_path: Path) -> None:
    """--board-dts/--build-info/--bindings-dir wire into the board
    reader. A rig with no board-resolution problem of its own (loader
    accepts cleanly) but naming a --board-dts that does not exist on
    disk must be rejected (exit 1, phys-board) -- proving the option
    actually reaches load_board rather than being parsed and discarded.
    (A rig the LOADER itself rejects first -- e.g. unreadable -- still
    exits 3 regardless of these options: see test_recipe_resolved_lazily
    below.) --board is given here too: rig.yml carries no board: of its
    own, so with no board injected, cli.py's own board-empty check would
    reject BEFORE ever reaching --board-dts, which is not what this test
    means to exercise."""
    (tmp_path / "rig.yml").write_text(
        dedent("""\
        rig:
          name: r
        """)
    )
    (tmp_path / "r.yml").write_text(
        dedent("""\
        instances: []
        """)
    )
    ret = main(
        [
            "expand",
            str(tmp_path / "rig.yml"),
            "--out-dir",
            str(tmp_path / "out"),
            *_no_shields(tmp_path),
            "--board",
            "some_board/soc/rig",
            "--board-dts",
            str(tmp_path / "no-such-board.dts"),
        ]
    )
    assert ret == 1


def test_board_option_reaches_load_board_with_the_given_name(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    """--board threads straight to `rig.board` -- proven the same way as
    the option above (a --board-dts that does not exist forces a
    phys-board rejection), but checking that the GIVEN name is what
    load_board's own diagnostic embeds. rig.yml declares no board: of
    its own -- --board is the only source."""
    (tmp_path / "rig.yml").write_text(
        dedent("""\
        rig:
          name: r
        """)
    )
    (tmp_path / "r.yml").write_text(
        dedent("""\
        instances: []
        """)
    )
    ret = main(
        [
            "expand",
            str(tmp_path / "rig.yml"),
            "--out-dir",
            str(tmp_path / "out"),
            *_no_shields(tmp_path),
            "--board",
            "given_board/soc/rig",
            "--board-dts",
            str(tmp_path / "no-such-board.dts"),
        ]
    )
    assert ret == 1
    err = capsys.readouterr().err
    assert "given_board/soc/rig" in err


def test_board_option_absent_is_a_clean_phys_board_reject(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    """The negative control: omitting --board, with no board: declaration
    in rig.yml to fall back to, must still be a clean phys-board
    rejection -- never a crash, and never load_board's own confusing
    "unknown board ''" (this fixture's --board-dts, which would
    otherwise force exactly that, proves cli.py's own board-empty check
    fires FIRST: --board-dts is never even reached)."""
    (tmp_path / "rig.yml").write_text(
        dedent("""\
        rig:
          name: r
        """)
    )
    (tmp_path / "r.yml").write_text(
        dedent("""\
        instances: []
        """)
    )
    ret = main(
        [
            "expand",
            str(tmp_path / "rig.yml"),
            "--out-dir",
            str(tmp_path / "out"),
            *_no_shields(tmp_path),
            "--board-dts",
            str(tmp_path / "no-such-board.dts"),
        ]
    )
    assert ret == 1
    err = capsys.readouterr().err
    assert "[phys-board]" in err
    assert "no board given" in err
    assert "no-such-board.dts" not in err


def test_recipe_resolved_lazily(tmp_path: Path) -> None:
    """A bogus --build-info path must never crash the run when the rig
    itself is rejected first (here: unreadable) -- the recipe is a
    board-reading concern, resolved only once the loader has already
    accepted, never eagerly alongside the other inputs (cli.py's own
    docstring at the _resolve_recipe call site). `open()`-ing a
    nonexistent --build-info path must never surface as an unhandled
    FileNotFoundError -- a traceback is never an acceptable outcome."""
    ret = main(
        [
            "expand",
            str(tmp_path / "no-such-rig.yml"),
            "--out-dir",
            str(tmp_path / "out"),
            *_no_shields(tmp_path),
            "--build-info",
            str(tmp_path / "no-such-build-info.yml"),
        ]
    )
    assert ret == 3


# ------------------------------------------------- loud, distinct refusals


def _run(capsys: pytest.CaptureFixture[str], argv: list[str]) -> tuple[int, str]:
    ret = main(argv)
    captured = capsys.readouterr()
    assert captured.out == ""  # diagnostics and refusals: stderr only
    return ret, captured.err


def test_unreadable_rig_refuses(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    ret, err = _run(
        capsys,
        [
            "expand",
            str(tmp_path / "absent.yml"),
            "--out-dir",
            str(tmp_path / "out"),
            *_no_shields(tmp_path),
        ],
    )
    assert ret == 3
    assert err.startswith("rigc: not implemented: ")
    assert len(err.splitlines()) == 1  # one line -- never a traceback


def test_out_of_scope_feature_refuses(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    """params:/config: are fully implemented -- a YAML parse failure is
    the capability that stays Unimplemented: no frozen golden covers
    lang-parse wording, so Unimplemented remains the deliberate,
    always-acceptable choice."""
    (tmp_path / "rig.yml").write_text(
        dedent("""\
        rig: [this is not, valid: yaml
        """)
    )
    ret, err = _run(
        capsys,
        [
            "expand",
            str(tmp_path / "rig.yml"),
            "--out-dir",
            str(tmp_path / "out"),
            *_no_shields(tmp_path),
        ],
    )
    assert ret == 3
    assert err.startswith("rigc: not implemented: ")


def _write_zero_instance_rig(tmp_path: Path) -> None:
    """A rig with zero instances needs no cpp from the emitter (no params
    to resolve, no shield,param-includes header to probe) -- the shape
    every accept-path test below reuses so board reading is the only
    thing left to stub.
    Carries no `board:` of its own -- every caller must pass `--board`
    itself, the only source."""
    (tmp_path / "rig.yml").write_text(
        dedent("""\
        rig:
          name: r
        """)
    )
    (tmp_path / "r.yml").write_text(
        dedent("""\
        instances: []
        """)
    )


def _stub_board_reading(monkeypatch: pytest.MonkeyPatch) -> None:
    """Board reading is integration-only by construction (the same
    cpp/unit-test seam that applies to the shield side) -- stubbed
    rather than exercised via a real board .dts + cpp."""
    from rigc.model import Board

    def fake_load_board(name: str, workdir: str, board_dts=None, recipe=None):
        return Board(name=name, sockets={}), [], frozenset()

    monkeypatch.setattr(cli, "load_board", fake_load_board)


def test_accept_path_now_accepts_and_writes_artifacts(
    tmp_path: Path, capsys: pytest.CaptureFixture[str], monkeypatch: pytest.MonkeyPatch
) -> None:
    """Input the loader/analyzer find nothing wrong with exits 0 and
    writes the rig artifacts + context.cmake -- proving the full accept
    path (emit, context.render, the one writer) without a subprocess."""
    _write_zero_instance_rig(tmp_path)
    _stub_board_reading(monkeypatch)

    out_dir = tmp_path / "out"
    ret, err = _run(
        capsys,
        [
            "expand",
            str(tmp_path / "rig.yml"),
            "--out-dir",
            str(out_dir),
            *_no_shields(tmp_path),
            "--board",
            "some_board/soc/rig",
        ],
    )
    assert ret == 0
    assert err == ""  # no diagnostics at all -- not even a warning
    for fname in ("rig-gen.overlay", "config-sheet.md", "expectations.yml", "context.cmake"):
        assert (out_dir / fname).is_file(), fname
    assert not (out_dir / "rig-gen-includes.dtsi").exists()  # no params: at all
    assert not (out_dir / "rig-gen.conf").exists()  # never emitted

    context_text = (out_dir / "context.cmake").read_text()
    assert 'set(RIG_NAME "r")' in context_text
    assert 'set(RIG_BOARD "some_board/soc/rig")' in context_text
    assert 'set(RIG_SHIELDS "")' in context_text


# ----------------------------------------------------------- the workdir


def _workdir_of(out_dir: Path) -> Path:
    """Where cli.py puts its workdir for a given --out-dir. Derived from
    cli.WORKDIR_NAME rather than spelled again, so a rename cannot leave
    these tests asserting a path nothing writes.

    The location is a property of the code under test, so these tests
    assert it directly -- and nothing can leak into real /tmp, because a
    workdir inside --out-dir is inside tmp_path by construction."""
    return out_dir / cli.WORKDIR_NAME


def test_accept_path_keeps_the_workdir(
    tmp_path: Path, capsys: pytest.CaptureFixture[str], monkeypatch: pytest.MonkeyPatch
) -> None:
    """An ACCEPTED run is the one that produces an overlay somebody
    later doubts, so its intermediates -- the shield
    `.dts` the loader wrote, the cpp-preprocessed `.pre` of each, a
    promoted shield's synthesized pair -- are exactly the evidence that
    doubt needs, and success is no reason to burn them.

    The control against "then it never wrote anything at all": the
    accept path's own artifacts must still have landed in --out-dir,
    which is a different directory."""
    _write_zero_instance_rig(tmp_path)
    _stub_board_reading(monkeypatch)

    out_dir = tmp_path / "out"
    ret, _err = _run(
        capsys,
        [
            "expand",
            str(tmp_path / "rig.yml"),
            "--out-dir",
            str(out_dir),
            *_no_shields(tmp_path),
            "--board",
            "some_board/soc/rig",
        ],
    )

    assert ret == 0
    assert _workdir_of(out_dir).is_dir()
    assert (out_dir / "context.cmake").is_file()


def test_reject_path_keeps_the_workdir(
    tmp_path: Path, capsys: pytest.CaptureFixture[str], monkeypatch: pytest.MonkeyPatch
) -> None:
    """The other exit, kept for the same reason: a rejected board-dts is
    real evidence a cpp failure's own rendered diagnostic points at
    (e.g. `param-missing-header`, which embeds this very path inside
    gcc's stderr text), so the directory must survive this exit too.

    Held as a SEPARATE test rather than folded into the accept one: the
    two exits reach the end of `_expand` by different routes (this one
    returns early from `_reject`, the other falls off the end), and one
    route surviving proves nothing about the other."""
    _write_zero_instance_rig(tmp_path)
    out_dir = tmp_path / "out"

    ret, _err = _run(
        capsys,
        [
            "expand",
            str(tmp_path / "rig.yml"),
            "--out-dir",
            str(out_dir),
            *_no_shields(tmp_path),
            "--board",
            "some_board/soc/rig",
            "--board-dts",
            str(tmp_path / "no-such-board.dts"),
        ],
    )

    assert ret == 1
    assert _workdir_of(out_dir).is_dir()


def test_entry_wipe_clears_a_previous_runs_workdir(
    tmp_path: Path, capsys: pytest.CaptureFixture[str], monkeypatch: pytest.MonkeyPatch
) -> None:
    """The one deletion `_expand` still does, and the negative control
    for the two retention tests above: "keep the workdir" must not decay
    into "accumulate every run's intermediates in one directory".

    A stale file left in the workdir by a previous run into the same
    --out-dir is GONE after the next run, because a `.pre` that no
    longer corresponds to the overlay sitting next to it is worse
    evidence than no `.pre` at all. Planted under a name nothing in the
    pipeline writes, so its survival could only mean the entry wipe
    stopped happening."""
    _write_zero_instance_rig(tmp_path)
    _stub_board_reading(monkeypatch)

    out_dir = tmp_path / "out"
    stale = _workdir_of(out_dir) / "a-previous-runs-leftover.dts.pre"
    stale.parent.mkdir(parents=True)
    stale.write_text("/* the run before this one */\n")

    ret, _err = _run(
        capsys,
        [
            "expand",
            str(tmp_path / "rig.yml"),
            "--out-dir",
            str(out_dir),
            *_no_shields(tmp_path),
            "--board",
            "some_board/soc/rig",
        ],
    )

    assert ret == 0
    assert _workdir_of(out_dir).is_dir()  # kept, per the ruling
    assert not stale.exists()  # but not this run's content


# --------------------------------------------------------------- --promote


def test_promote_writes_promote_shields_own_documents_verbatim(
    tmp_path: Path, capsys: pytest.CaptureFixture[str], monkeypatch: pytest.MonkeyPatch
) -> None:
    """There is exactly ONE desugaring: --promote's materialized
    rig.yml/content pair is byte-identical to promote.promote_shield's
    own return, for the exact name/filename it chose. No --board is
    given, so this run rejects at cli.py's own board-empty check: the
    loader itself no longer needs a board to accept a promoted rig's
    topology, so this is the first and only place a missing one still
    matters. The workdir is kept on that reject, which is what lets
    this test read the two files back off disk."""
    from rigc.promote import promote_shield

    out_dir = tmp_path / "out"
    ret, _err = _run(
        capsys,
        [
            "expand",
            "--promote",
            "adafruit_data_logger",
            "--out-dir",
            str(out_dir),
            *_no_shields(tmp_path),
        ],
    )

    assert ret == 1
    workdir = _workdir_of(out_dir)
    expected = promote_shield("adafruit_data_logger")
    assert (workdir / "rig.yml").read_text() == expected.rig_yml
    assert (workdir / expected.content_name).read_text() == expected.content


def test_promote_with_revision_bakes_the_shields_own_revision(
    tmp_path: Path, capsys: pytest.CaptureFixture[str], monkeypatch: pytest.MonkeyPatch
) -> None:
    """--revision alongside --promote means the SHIELD's own revision --
    baked into the synthesized content file's `shield:` reference, never
    forwarded to loader.load as a rig-level axis selection (a promoted
    rig declares no revisions: of its own). Reused promote_shield
    directly as the oracle, same as the test above."""
    from rigc.promote import promote_shield

    out_dir = tmp_path / "out"
    ret, _err = _run(
        capsys,
        [
            "expand",
            "--promote",
            "i2c_sensor",
            "--revision",
            "2",
            "--out-dir",
            str(out_dir),
            *_no_shields(tmp_path),
        ],
    )

    assert ret == 1
    workdir = _workdir_of(out_dir)
    expected = promote_shield("i2c_sensor", revision="2")
    assert (workdir / "rig.yml").read_text() == expected.rig_yml
    assert (workdir / expected.content_name).read_text() == expected.content
    assert "shield: i2c_sensor@2" in expected.content


def test_promote_with_a_dotted_config_opt_writes_a_config_block_verbatim(
    tmp_path: Path, capsys: pytest.CaptureFixture[str], monkeypatch: pytest.MonkeyPatch
) -> None:
    """The end-to-end `--promote <shield>:config.<label>=<value>` path,
    threaded through cli.py's own `--promote` branch
    (args.promote.partition(":") -> parse_promotion_opts ->
    promote_shield) rather than calling promote_shield directly:
    proves `ParsedPromotionOpts.config` actually reaches the printed
    text via THIS module's own plumbing, not merely via promote.py's own
    printer in isolation. A MUTATION that routed `config.<label>=` to
    `params` instead (or dropped `config=opts.config or None` from this
    module's own promote_shield call) would make this fail on the
    PRINTED BLOCK itself -- either as a `params:` block quoting `config`
    as a device label, or as a missing `config:` block entirely."""
    from rigc.promote import promote_shield

    out_dir = tmp_path / "out"
    ret, _err = _run(
        capsys,
        [
            "expand",
            "--promote",
            "adafruit_winc1500:config.w_irq_jmp=D2",
            "--out-dir",
            str(out_dir),
            *_no_shields(tmp_path),
        ],
    )

    assert ret == 1
    workdir = _workdir_of(out_dir)
    expected = promote_shield("adafruit_winc1500", config={"w_irq_jmp": "D2"})
    assert (workdir / expected.content_name).read_text() == expected.content
    assert "    config:\n      w_irq_jmp: D2\n" in expected.content
    assert (workdir / "rig.yml").read_text() == expected.rig_yml


# --------------------------------------------------------------- logging


def test_stderr_carries_only_renderer_bytes_when_rigc_log_is_unset(
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
    caplog: pytest.LogCaptureFixture,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """The stderr-purity discipline test: with RIGC_LOG unset, the package
    root's NullHandler (rigc/__init__.py) is the only handler on the
    `rigc` tree, so a full main() run over a REJECTING input puts ONLY
    the renderer's own bytes on stderr -- while caplog, which taps
    Python's real root logger independently of our own (silent) handler,
    still observes that the pipeline actually emitted records, proving
    this is a "nothing configured" outcome rather than "nothing
    happened"."""
    monkeypatch.delenv("RIGC_LOG", raising=False)
    caplog.set_level(logging.DEBUG, logger="rigc")

    (tmp_path / "rig.yml").write_text("not-rig: {}\n")
    ret, err = _run(
        capsys,
        [
            "expand",
            str(tmp_path / "rig.yml"),
            "--out-dir",
            str(tmp_path / "out"),
            *_no_shields(tmp_path),
        ],
    )

    assert ret == 1
    assert "error[lang-schema]" in err
    # ONLY renderer bytes -- none of our own log formatting leaked in.
    assert "INFO" not in err
    assert "DEBUG" not in err
    assert "rigc.cli" not in err
    assert "rigc.loader" not in err
    # ...yet the pipeline really did log: caplog observed the records via
    # propagation, entirely independent of the (silent) handler above.
    assert any("argv" in m for m in caplog.messages)
    assert any(r.name == "rigc.loader" for r in caplog.records)


def test_rigc_log_env_attaches_a_real_stderr_handler(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """RIGC_LOG=<level> is one way a real handler reaches the `rigc`
    logger tree (the other is -v/-vv, see below) -- read fresh at the top
    of every main() call (not at import time), so this is observable
    without a subprocess."""
    monkeypatch.setenv("RIGC_LOG", "debug")

    main(
        [
            "expand",
            str(tmp_path / "no-such-rig.yml"),
            "--out-dir",
            str(tmp_path / "out"),
            *_no_shields(tmp_path),
        ]
    )

    root = logging.getLogger("rigc")
    real_handlers = [
        h
        for h in root.handlers
        if isinstance(h, logging.StreamHandler) and not isinstance(h, logging.NullHandler)
    ]
    assert len(real_handlers) == 1
    assert root.getEffectiveLevel() == logging.DEBUG

    # Deterministic cleanup -- a repeated main() call always re-derives
    # its handler state from the CURRENT environment, so unsetting and
    # calling _configure_logging() again leaves the logger tree exactly
    # as every OTHER test in this module expects to find it.
    monkeypatch.delenv("RIGC_LOG")
    _configure_logging()


def _assert_verbose_flag_attaches_a_real_stderr_handler(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, flag: str, level: int
) -> None:
    """-v/-vv reach `_configure_logging` the same way RIGC_LOG does, with
    no environment variable involved at all. A plain helper, not a
    parametrized test -- tests/unit/ bans pytest markers outright
    (test_layer_discipline.py), directory-classified only."""
    monkeypatch.delenv("RIGC_LOG", raising=False)

    main(
        [
            "expand",
            str(tmp_path / "no-such-rig.yml"),
            "--out-dir",
            str(tmp_path / "out"),
            *_no_shields(tmp_path),
            flag,
        ]
    )

    root = logging.getLogger("rigc")
    real_handlers = [
        h
        for h in root.handlers
        if isinstance(h, logging.StreamHandler) and not isinstance(h, logging.NullHandler)
    ]
    assert len(real_handlers) == 1
    assert root.getEffectiveLevel() == level

    _configure_logging()  # same deterministic cleanup as the test above


def test_dash_v_attaches_a_real_stderr_handler_at_info(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    _assert_verbose_flag_attaches_a_real_stderr_handler(tmp_path, monkeypatch, "-v", logging.INFO)


def test_dash_vv_attaches_a_real_stderr_handler_at_debug(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    _assert_verbose_flag_attaches_a_real_stderr_handler(tmp_path, monkeypatch, "-vv", logging.DEBUG)


def test_verbose_flag_overrides_rigc_log(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """The CLI flag is the more explicit, per-invocation request, so it
    wins when both are present -- here RIGC_LOG asks for DEBUG but -v
    (INFO) is what the run actually gets."""
    monkeypatch.setenv("RIGC_LOG", "debug")

    main(
        [
            "expand",
            str(tmp_path / "no-such-rig.yml"),
            "--out-dir",
            str(tmp_path / "out"),
            *_no_shields(tmp_path),
            "-v",
        ]
    )

    assert logging.getLogger("rigc").getEffectiveLevel() == logging.INFO

    monkeypatch.delenv("RIGC_LOG")
    _configure_logging()


def test_log_format_carries_a_timestamp_and_the_emitting_function(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    """Every enabled record must be traceable to WHEN it fired and WHICH
    function emitted it -- both are missing from a plain level+name
    format and neither is recoverable after the fact."""
    monkeypatch.delenv("RIGC_LOG", raising=False)

    main(
        [
            "expand",
            str(tmp_path / "no-such-rig.yml"),
            "--out-dir",
            str(tmp_path / "out"),
            *_no_shields(tmp_path),
            "-v",
        ]
    )

    err = capsys.readouterr().err
    assert "rigc.cli:main" in err  # module:function
    assert re.search(r"\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}", err)

    _configure_logging()
