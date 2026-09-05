# Copyright (c) 2026 TiaC Systems
# SPDX-License-Identifier: Apache-2.0
"""Meta: the test-tree conventions, enforced structurally.

The one test module whose subject is not a production unit but the tests
tree itself (recorded exemption in _META_MODULES below). It enforces:

  - every test module lives under exactly one of tests/unit/,
    tests/integration/ or tests/integration_stay/ -- the latter two are
    one LAYER in two homes (see _LAYER_DIRS);
  - unit test modules NAME THEIR UNIT: a
    test_<name>.py directly under tests/unit/ must name a python module
    of the rigc package (or the tests' own conftest); when one unit needs
    several test modules they live in a sub-folder tests/unit/<name>/
    that itself names the unit. Tests may USE other units, but the named
    unit is the subject;
  - no module under tests/unit/ imports subprocess (the structural proxy
    for "a unit test uses NO subprocess");
  - no pytest markers under tests/unit/ -- the directory IS the
    classification there; the integration layer keeps exactly one
    marker, `build`, because check.sh's fast gate selects on it
    (`pytest -m "not build"`), and every integration test that reaches a
    real west/cmake configure must carry it;
  - no module-scope environment lookup of the Zephyr tree variable
    anywhere in the package or its tests (the dtsio.py:27 collection
    trap, designed out: pytest imports every module before deselection).
"""

from __future__ import annotations

import ast
import textwrap
from collections.abc import Iterator
from pathlib import Path

import rigc

RIGC_DIR = Path(rigc.__file__).resolve().parent
TESTS_DIR = RIGC_DIR / "tests"

#: Test modules whose subject is the tests tree / conventions themselves,
#: not a production unit -- the recorded exemption from unit naming.
_META_MODULES = {"test_layer_discipline"}

#: The integration LAYER's two directories. The split is by TETHER, not by
#: kind: integration/ holds the tests that read nothing outside
#: tests/fixtures/, rigc/ and doc/, so they travel with the transpiler when
#: it is vendored into another repository; integration_stay/ holds the ones
#: read this repo's own boards/rigs/, boards/shields/ or boards/extend/ and
#: therefore stay behind with the hardware definitions. Every guard over
#: "the integration layer" must walk BOTH -- a guard that walks only the
#: first would, after the split, cover almost none of the build tests,
#: which is exactly the regression this constant exists to prevent.
_INTEGRATION_DIRS = ("integration", "integration_stay")

#: The unit LAYER's two directories, split by the SAME tether rule: unit/
#: holds the tests that read nothing outside rigc/ and tests/fixtures/
#: (threading `rigc.tests.roots`' vendored connector bindings and shield
#: library rather than taking any module-relative fallback), so they travel;
#: unit_stay/ holds the ones whose SUBJECT is this repo's own corpus -- the
#: shield census and its mutation control -- which cannot travel and should
#: not be rewritten against fixtures, since a fixture census asserts only
#: that the fixtures are the fixtures.
_UNIT_DIRS = ("unit", "unit_stay")

#: Every directory a test module may live in, as the (top, layer) prefix of
#: its rigc-relative path.
_LAYER_DIRS = tuple(("tests", name) for name in _UNIT_DIRS + _INTEGRATION_DIRS)


def _python_files(root: Path) -> list[Path]:
    return sorted(p for p in root.rglob("*.py") if "__pycache__" not in p.parts)


def _unit_files() -> list[tuple[Path, Path]]:
    """Every python file in the unit LAYER, as (path, path-relative-to-its-
    own-unit-directory) pairs.

    Both directories, always. A guard that walked only tests/unit/ would
    stop covering anything moved to tests/unit_stay/ -- silently, since a
    guard that inspects nothing passes. That is the regression
    _INTEGRATION_DIRS' own comment describes, and this helper exists so the
    unit side cannot repeat it: adding a third unit directory means editing
    _UNIT_DIRS, and nothing else.
    """
    pairs = []
    for name in _UNIT_DIRS:
        root = TESTS_DIR / name
        if not root.is_dir():
            continue
        pairs += [(p, p.relative_to(root)) for p in _python_files(root)]
    return pairs


def test_every_test_module_is_layer_classified() -> None:
    offenders = []
    for path in _python_files(RIGC_DIR):
        if not path.name.startswith("test_"):
            continue
        rel = path.relative_to(RIGC_DIR)
        if rel.parts[:2] not in _LAYER_DIRS:
            offenders.append(str(rel))
    assert not offenders, (
        "test modules outside tests/{unit,unit_stay,integration,"
        "integration_stay}/ (the directory IS the layer classification): "
        f"{offenders}"
    )


def _top_level_units() -> set[str]:
    """Every valid unit NAME directly under the rigc package: a bare
    module (cli.py -> "cli") or a SUB-PACKAGE (loader/ -> "loader") --
    either way, a name a test module or a tests/unit/<name>/ sub-folder
    may claim as its subject."""
    units = {p.stem for p in RIGC_DIR.glob("*.py")}
    units |= {
        p.name
        for p in RIGC_DIR.iterdir()
        if p.is_dir() and (p / "__init__.py").is_file() and p.name != "tests"
    }
    # conftest.py and compare.py are the tests package's own modules, not
    # production units -- both still get a named test module (test_conftest.py,
    # test_compare.py) under the same "test modules name their unit" rule.
    return units | {"conftest", "compare"}


def test_unit_test_modules_name_their_unit() -> None:
    """test_<name>.py names a rigc module (or the tests package's own
    conftest/compare); a sub-folder under tests/unit/ names the unit its
    modules share -- a PACKAGE (e.g. loader/) is as valid a unit name
    here as a bare module."""
    units = _top_level_units()
    offenders = []
    for path, rel in _unit_files():
        if not path.name.startswith("test_"):
            continue
        if len(rel.parts) == 1:  # directly under the unit directory
            subject = path.stem.removeprefix("test_")
            if subject not in units and path.stem not in _META_MODULES:
                offenders.append(f"{rel}: no unit named '{subject}'")
        else:  # unit/<subject>/...
            subject = rel.parts[0]
            if subject not in units:
                offenders.append(f"{rel}: no unit named '{subject}'")
    assert not offenders, (
        "unit test modules must name the unit under test "
        f"(test_<module>.py, or a tests/unit/<module>/ sub-folder): "
        f"{offenders}"
    )


def test_unit_modules_import_no_subprocess() -> None:
    offenders = []
    for path, _rel in _unit_files():
        tree = ast.parse(path.read_text(), filename=str(path))
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                names = [alias.name for alias in node.names]
            elif isinstance(node, ast.ImportFrom):
                names = [node.module or ""]
            else:
                continue
            if any(n == "subprocess" or n.startswith("subprocess.") for n in names):
                offenders.append(f"{path.name}:{node.lineno}")
    assert not offenders, (
        "tests/unit/ modules importing subprocess (reaching code through "
        f"the CLI front door is integration by definition): {offenders}"
    )


def test_no_pytest_markers_under_tests_unit() -> None:
    """Markers are banned in the UNIT tree, where the directory is the
    classification. The integration tree keeps exactly one marker, `build`,
    because the fast gate selects on it (`pytest -m "not build"`) -- a
    layer marker there would be the second mechanism for a fact the
    directory already states, which is what made the two enforcement
    regimes contradict each other before they were split this way."""
    offenders = []
    for path, _rel in _unit_files():
        tree = ast.parse(path.read_text(), filename=str(path))
        for node in ast.walk(tree):
            if (
                isinstance(node, ast.Attribute)
                and node.attr == "mark"
                and isinstance(node.value, ast.Name)
                and node.value.id == "pytest"
            ):
                offenders.append(f"{path.relative_to(RIGC_DIR)}:{node.lineno}")
    assert not offenders, (
        "pytest markers found under tests/unit/ -- there the directory is "
        f"the classification, markers are banned: {offenders}"
    )


# ---------------------------------------------------------------- build-marker guard

# Functions whose OWN body launches a real west/cmake configure, read out of
# tests/integration_stay/corpus.py, test_resolved_corpus.py and
# test_cmake_alone_entry.py rather than guessed: a blanket "calls
# subprocess" heuristic would misclassify every fixture that calls
# harness.run_expand, which is a subprocess too but only plain
# expansion -- never a build. All five live on the stay side today: a build
# needs a real board, and every real board is an extension defined
# alongside the rigs.
# `_run_build_rig` (test_cmake_alone_entry.py's own west-build-rig
# reference path) retired along with `west build-rig` itself -- there is
# no successor entry for it; `_run_build` below is NOT its replacement,
# it already existed and already used the surviving cmake entry point by
# construction (see that command's own retired docstring).
_BUILD_HELPERS = frozenset(
    {
        "plain_build_for",  # corpus.py: session-cached `west build --cmake-only` per board
        "_run_plain_build",  # corpus.py: the plain `west build --cmake-only` itself
        "_run_build",  # test_resolved_corpus.py: `west build --cmake-only -- -DRIG=`
        "_build_and_freeze_dts",  # test_resolved_corpus.py: wraps _run_build
        "_run_cmake_alone",  # test_cmake_alone_entry.py: a bare `cmake -S -B` configure
    }
)

#: argv[0] values that ARE a build, however they are launched. A curated
#: helper set can only ever list the launchers that exist when it is
#: written; several tests run `subprocess.run(["cmake", ...])` inline with
#: no helper at all, and those must not be invisible just because nobody
#: named them. Recognising the command itself closes the class rather than
#: the instance. "cmake" is unconditionally a configure; "west"/WEST_EXE is
#: not -- west also fronts non-configuring subcommands (`west rigs
#: --boards-for`, a plain census query), so an argv headed by one of
#: these two needs its SUBCOMMAND checked too (see
#: _WEST_BUILD_SUBCOMMANDS below) rather than being treated as a build
#: on sight.
_BUILD_COMMANDS = frozenset({"cmake", "WEST_EXE", "west"})

#: The west subcommands that actually configure cmake -- an argv headed by
#: "west"/WEST_EXE only counts as a build launch when elts[1] is one of
#: these; every other west subcommand (a listing, a query) is not.
#: "build-rig" retired along with the command it named -- `build` is the
#: one surviving configuring subcommand a rig build ever launches now.
_WEST_BUILD_SUBCOMMANDS = frozenset({"build"})

#: ast.parse never yields an AsyncFunctionDef for a `def`, but the isinstance
#: check in _defs_by_name asks for both, so the dict value type must too.
_FuncDef = ast.FunctionDef | ast.AsyncFunctionDef


def _call_targets(node: ast.AST) -> Iterator[str]:
    """Every Call inside node, by its callee's bare identifier -- a build
    helper in this tree is always invoked unqualified or as
    `harness.<name>`/`corpus.<name>`, never reassigned to another name, so the trailing
    identifier (Name.id, or Attribute.attr for a dotted call) is enough to
    recognize it."""
    for child in ast.walk(node):
        if isinstance(child, ast.Call):
            func = child.func
            if isinstance(func, ast.Name):
                yield func.id
            elif isinstance(func, ast.Attribute):
                yield func.attr


def _argv_head_name(elt: ast.expr) -> str | None:
    """The bare identifier an argv element names, however it is spelled --
    a string literal ("cmake") or a Name (WEST_EXE). None for anything
    else (an f-string, a variable holding something other than a bare
    command name, ...)."""
    if isinstance(elt, ast.Constant) and isinstance(elt.value, str):
        return elt.value
    if isinstance(elt, ast.Name):
        return elt.id
    return None


def _launches_build_inline(node: ast.AST) -> bool:
    """Whether node's own body launches a build WITHOUT going through a
    named helper -- a subprocess call whose argv list opens with a build
    command (a "cmake" literal, or the WEST_EXE constant/"west" literal
    FOLLOWED BY a configuring subcommand -- see _WEST_BUILD_SUBCOMMANDS).
    Without this a test can run the slowest configure in the tree and stay
    invisible to the guard simply by not naming a function."""
    # Any argv-shaped literal whose first element is a build command, not
    # just one passed directly as a call argument: the prevailing idiom here
    # binds it first (cmd = ["cmake", ...]) and calls subprocess.run(cmd),
    # so matching only call arguments misses exactly the tests that do that.
    for child in ast.walk(node):
        if not isinstance(child, (ast.List, ast.Tuple)) or not child.elts:
            continue
        head_name = _argv_head_name(child.elts[0])
        if head_name not in _BUILD_COMMANDS:
            continue
        if head_name == "cmake":
            return True
        # west / WEST_EXE: a configure only when the SUBCOMMAND says so.
        # An argv with no second element (bare "west"/WEST_EXE) names no
        # subcommand to check, so it cannot be a configure launch either.
        if len(child.elts) < 2:
            continue
        if _argv_head_name(child.elts[1]) in _WEST_BUILD_SUBCOMMANDS:
            return True
    return False


def _defs_by_name(tree: ast.Module) -> dict[str, _FuncDef]:
    return {n.name: n for n in tree.body if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef))}


def _reaches_build_helper(name: str, defs: dict[str, _FuncDef], memo: dict[str, bool]) -> bool:
    """Whether the module-local def `name` -- a test, a fixture, or a
    plain helper -- transitively reaches a _BUILD_HELPERS entry: by
    calling one directly, by calling another module-local def that does,
    or by declaring a PARAMETER named after a module-local fixture that
    does (a fixture parameter is pytest's own implicit call). memo also
    doubles as cycle protection: a name is provisionally False while its
    own body is still being walked, so a (currently nonexistent) fixture
    cycle can only under- not over-report."""
    if name in memo:
        return memo[name]
    fn = defs.get(name)
    if fn is None:
        return False
    memo[name] = False
    reached = _launches_build_inline(fn) or any(
        called in _BUILD_HELPERS or _reaches_build_helper(called, defs, memo)
        for called in _call_targets(fn)
    )
    if not reached:
        # `p.arg in _BUILD_HELPERS` matters even though every helper is a
        # plain function today: turning one into a real pytest fixture is
        # the natural refactor, and it would otherwise blind every consumer
        # at once.
        params = fn.args.args + fn.args.kwonlyargs
        reached = any(
            p.arg in _BUILD_HELPERS or _reaches_build_helper(p.arg, defs, memo) for p in params
        )
    memo[name] = reached
    return reached


def _mark_names(nodes: list[ast.expr]) -> Iterator[str]:
    """The mark name(s) a list of attribute-chain expressions resolve to
    -- shared by a module-level `pytestmark = pytest.mark.x` (or a list of
    those) and a function's `@pytest.mark.x` decorators, both plain
    attribute-access expressions of the same shape."""
    for node in nodes:
        if (
            isinstance(node, ast.Attribute)
            and isinstance(node.value, ast.Attribute)
            and isinstance(node.value.value, ast.Name)
            and node.value.value.id == "pytest"
            and node.value.attr == "mark"
        ):
            yield node.attr


def _module_build_mark(tree: ast.Module) -> bool:
    """True if the module-level `pytestmark = ...` assignment carries
    pytest.mark.build -- applies to every test in the module regardless of
    its own decorators."""
    for stmt in tree.body:
        if isinstance(stmt, ast.Assign) and any(
            isinstance(t, ast.Name) and t.id == "pytestmark" for t in stmt.targets
        ):
            value = stmt.value
            elts = value.elts if isinstance(value, (ast.List, ast.Tuple)) else [value]
            if "build" in _mark_names(elts):
                return True
    return False


def _is_build_marked(fn: _FuncDef, module_marked: bool) -> bool:
    return module_marked or "build" in _mark_names(fn.decorator_list)


def _collect_unmarked_build_tests(path: Path, offenders: list[str]) -> None:
    """Append `<module>::<test>` for every test in `path` that reaches a
    build and carries no build marker. Mutates the caller's list."""
    tree = ast.parse(path.read_text(), filename=str(path))
    defs = _defs_by_name(tree)
    module_marked = _module_build_mark(tree)
    memo: dict[str, bool] = {}
    for fn_name, fn in defs.items():
        if not fn_name.startswith("test_"):
            continue
        if _reaches_build_helper(fn_name, defs, memo) and not _is_build_marked(fn, module_marked):
            offenders.append(f"{path.relative_to(RIGC_DIR)}::{fn_name}")


def test_every_build_reaching_integration_test_is_marked_build() -> None:
    """The other half of the merged discipline: directory decides unit vs
    integration, but `build` survives as a marker because check.sh's
    fast gate selects on it (`pytest -m "not build"`). An integration
    test that runs a real
    west/cmake configure and carries no @pytest.mark.build silently runs
    inside that fast gate -- or, symmetrically, hides from `-m "not
    build"` when someone means to select only builds.

    See test_build_reaching_guard_detects_an_unmarked_build_test below for
    this guard's own negative control."""
    offenders: list[str] = []
    for layer in _INTEGRATION_DIRS:
        for path in _python_files(TESTS_DIR / layer):
            if not path.name.startswith("test_"):
                continue
            _collect_unmarked_build_tests(path, offenders)
    assert not offenders, (
        "integration tests that reach a west/cmake build but carry no "
        f"@pytest.mark.build: {offenders}"
    )


def test_the_build_helper_set_is_exactly_the_known_launchers() -> None:
    """An INDEPENDENT list, deliberately not derived from _BUILD_HELPERS.

    A control that iterates the set under test is vacuous: dropping a
    helper just shrinks the loop, so the guard silently enforces less and
    every case still passes. Spelling the names out here means removing one
    from the production set fails this test, and ADDING one fails it too --
    which forces whoever adds a launcher to also give it a control below."""
    expected = {
        "plain_build_for",
        "_run_plain_build",
        "_run_build",
        "_build_and_freeze_dts",
        "_run_cmake_alone",
    }
    assert expected == _BUILD_HELPERS, (
        "the build-launcher set changed; add or remove its control here and "
        "in the reachability cases below, deliberately"
    )


def test_each_known_launcher_is_acted_on_by_the_reachability_walk() -> None:
    """One synthetic module per launcher, names spelled out rather than
    read from _BUILD_HELPERS for the same reason as above."""
    for helper in (
        "plain_build_for",
        "_run_plain_build",
        "_run_build",
        "_build_and_freeze_dts",
        "_run_cmake_alone",
    ):
        tree = ast.parse(
            textwrap.dedent(f"""
            def {helper}(*args, **kwargs):
                return None

            def test_configures_clean():
                {helper}("x", None)
            """)
        )
        defs = _defs_by_name(tree)
        assert _reaches_build_helper("test_configures_clean", defs, {}), helper


def test_a_fixture_parameter_naming_a_launcher_reaches_a_build() -> None:
    """The `p.arg in _BUILD_HELPERS` branch: a test can reach a build by
    DECLARING a parameter named after a launcher, with no local definition
    of it at all -- pytest's own implicit call. Inert while every launcher
    is a plain function, but converting one into a real fixture is the
    natural refactor and would blind every consumer at once."""
    tree = ast.parse(
        textwrap.dedent("""
        def test_configures_clean(plain_build_for):
            return plain_build_for
        """)
    )
    defs = _defs_by_name(tree)
    assert _reaches_build_helper("test_configures_clean", defs, {})


def test_an_indirect_two_hop_chain_still_reaches_a_build() -> None:
    """The recursive half of the walk, which the docstring claims and
    nothing else exercises: every real chain in the tree happens to have a
    _BUILD_HELPERS entry at BOTH ends, so depth-1 alone would satisfy it
    and a broken recursion would go unnoticed."""
    tree = ast.parse(
        textwrap.dedent("""
        def _run_build(rig, out):
            return None

        def _inner(rig):
            return _run_build(rig, None)

        def _wrapper(rig):
            return _inner(rig)

        def test_configures_clean():
            _wrapper("x")
        """)
    )
    defs = _defs_by_name(tree)
    assert _reaches_build_helper("test_configures_clean", defs, {})


def test_an_inline_cmake_launch_counts_as_a_build() -> None:
    """A test that runs cmake with no named helper at all -- the shape that
    made eight real cmake-alone tests invisible to a purely helper-based
    guard, protected only by a module-level marker they did not have to
    carry."""
    inline = ast.parse(
        textwrap.dedent("""
        def test_configures_clean():
            cmd = ["cmake", "-S", "app", "-B", "out"]
            subprocess.run(cmd, capture_output=True)
        """)
    )
    defs = _defs_by_name(inline)
    assert _reaches_build_helper("test_configures_clean", defs, {})

    free = ast.parse(
        textwrap.dedent("""
        def test_rejects_cleanly():
            cmd = ["python3", "-m", "rigc", "expand", "rig.yml"]
            subprocess.run(cmd, capture_output=True)
        """)
    )
    defs2 = _defs_by_name(free)
    assert not _reaches_build_helper("test_rejects_cleanly", defs2, {})


def test_an_inline_west_launch_only_counts_as_a_build_for_a_configuring_subcommand() -> None:
    """west fronts non-configuring subcommands too (`west rigs
    --boards-for`) -- an inline WEST_EXE argv only counts as a build
    when its SECOND element names one of
    _WEST_BUILD_SUBCOMMANDS. A bare WEST_EXE with no subcommand at all is
    unknown, never a build (it cannot configure anything by itself)."""
    configures = ast.parse(
        textwrap.dedent("""
        def test_configures_clean():
            cmd = [WEST_EXE, "build", "-b", "x", "app"]
            subprocess.run(cmd, capture_output=True)
        """)
    )
    defs = _defs_by_name(configures)
    assert _reaches_build_helper("test_configures_clean", defs, {})

    queries = ast.parse(
        textwrap.dedent("""
        def test_lists_boards():
            cmd = [WEST_EXE, "rigs", "--boards-for", "x"]
            subprocess.run(cmd, capture_output=True)
        """)
    )
    defs2 = _defs_by_name(queries)
    assert not _reaches_build_helper("test_lists_boards", defs2, {})

    bare = ast.parse(
        textwrap.dedent("""
        def test_bare_west():
            cmd = [WEST_EXE]
            subprocess.run(cmd, capture_output=True)
        """)
    )
    defs3 = _defs_by_name(bare)
    assert not _reaches_build_helper("test_bare_west", defs3, {})


def test_build_reaching_guard_detects_an_unmarked_build_test() -> None:
    """Negative control for the guard above: a guard nobody proved can
    fail is worthless. A synthetic module
    reaching _run_build with no @pytest.mark.build must be flagged by the
    same primitives the real guard uses; the identical module WITH the
    marker must not."""
    unmarked = ast.parse(
        textwrap.dedent("""
        def _run_build(rig_name, build_dir):
            return None

        def test_configures_clean():
            _run_build("x", None)
        """)
    )
    defs = _defs_by_name(unmarked)
    fn = defs["test_configures_clean"]
    assert _reaches_build_helper("test_configures_clean", defs, {})
    assert not _is_build_marked(fn, _module_build_mark(unmarked))

    marked = ast.parse(
        textwrap.dedent("""
        import pytest

        def _run_build(rig_name, build_dir):
            return None

        @pytest.mark.build
        def test_configures_clean():
            _run_build("x", None)
        """)
    )
    defs2 = _defs_by_name(marked)
    fn2 = defs2["test_configures_clean"]
    assert _reaches_build_helper("test_configures_clean", defs2, {})
    assert _is_build_marked(fn2, _module_build_mark(marked))

    # The fixture-parameter path: a test names a fixture, never calling
    # the build helper itself.
    via_fixture = ast.parse(
        textwrap.dedent("""
        import pytest

        def _run_build(rig_name, build_dir):
            return None

        def plain_build():
            return _run_build("x", None)

        def test_uses_plain_build(plain_build):
            assert plain_build is not None
        """)
    )
    defs3 = _defs_by_name(via_fixture)
    fn3 = defs3["test_uses_plain_build"]
    assert _reaches_build_helper("test_uses_plain_build", defs3, {})
    assert not _is_build_marked(fn3, _module_build_mark(via_fixture))


def _import_time_constants(tree: ast.Module) -> Iterator[ast.Constant]:
    """Constants evaluated at import time: module body and class bodies,
    with function/method bodies skipped (code inside them runs only when
    called) and bare-string docstring statements skipped."""

    def visit(body: list[ast.stmt]) -> Iterator[ast.Constant]:
        for stmt in body:
            if isinstance(stmt, (ast.FunctionDef, ast.AsyncFunctionDef)):
                continue
            if isinstance(stmt, ast.ClassDef):
                yield from visit(stmt.body)
                continue
            if (
                isinstance(stmt, ast.Expr)
                and isinstance(stmt.value, ast.Constant)
                and isinstance(stmt.value.value, str)
            ):
                continue  # docstring
            for node in ast.walk(stmt):
                if isinstance(node, ast.Constant):
                    yield node

    return visit(tree.body)


def test_no_module_scope_zephyr_tree_lookup() -> None:
    forbidden = "ZEPHYR" + "_BASE"  # split so this file's own module
    offenders = []  # scope never carries the literal
    for path in _python_files(RIGC_DIR):
        tree = ast.parse(path.read_text(), filename=str(path))
        for const in _import_time_constants(tree):
            if const.value == forbidden:
                offenders.append(f"{path.relative_to(RIGC_DIR)}:{const.lineno}")
    assert not offenders, (
        f"module-scope {forbidden} reference (breaks collection for "
        f"selections that never run it -- keep lookups inside functions): "
        f"{offenders}"
    )
