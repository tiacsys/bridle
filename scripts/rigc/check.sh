#!/bin/sh
# Copyright (c) 2026 TiaC Systems
# SPDX-License-Identifier: Apache-2.0
#
# The rig transpiler's own gate: mypy clean + pytest green + a coverage floor.
#
# It lives BESIDE the tool rather than in scripts/, because it checks exactly
# one subtree and nothing else in this repository -- it must never name, check
# or depend on a path outside scripts/rigc/. That self-containment is not
# tidiness: it is what let the transpiler arrive here as a unit, and what lets
# it be run without reference to whatever wider gate this repository layers on
# top. Keep it that way.
#
# Usage:  ZEPHYR_BASE=<zephyr tree> scripts/rigc/check.sh
#   CHECK_FAST=1   deselect tests marked 'build'. Currently a no-op: this suite
#                  carries none, because every build-reaching test is tethered
#                  to a real board and stays in the repository the transpiler
#                  came from. Kept because the marker is declared, and a build
#                  test against a rig defined HERE may yet be written.
#   PYTHON=<path>  interpreter to use (default python3). Point it at the
#                  workspace venv so mypy and pytest are the pinned ones.
set -e
cd "$(dirname "$0")"

PY="${PYTHON:-python3}"
CFG=pyproject.toml

if [ -z "$ZEPHYR_BASE" ]; then
    echo "check.sh: ZEPHYR_BASE is not set -- export it (the zephyr tree)." >&2
    echo "  It locates dtlib/edtlib for both mypy (MYPYPATH) and the tests." >&2
    exit 2
fi
export MYPYPATH="$ZEPHYR_BASE/scripts/dts/python-devicetree/src"

# Every tool is pointed at pyproject.toml explicitly rather than left to
# discovery: this file is not at the repository root, and a bare invocation
# from elsewhere would silently pick up different settings, or none.
echo "== mypy: rigc =="
# From the parent, so `rigc` is a package rather than the working directory.
(cd .. && "$PY" -m mypy --config-file rigc/"$CFG" rigc)

mkdir -p .reports
echo "== pytest: rigc unit (with coverage) =="
# Failure is captured, not fatal, so the browsable reports below still render
# for a RED run -- the run you most want a report for. Both statuses are
# re-raised once they have.
rigc_status=0
"$PY" -m coverage run --rcfile="$CFG" -m pytest -c "$CFG" --rootdir=. tests/unit \
    --durations=25 --junitxml=.reports/junit-rigc.xml || rigc_status=$?
# `coverage report` carries fail_under, so it EXITS NON-ZERO on a regression.
coverage_status=0
"$PY" -m coverage report --rcfile="$CFG" || coverage_status=$?
#   $BROWSER scripts/rigc/.reports/coverage-rigc-html/index.html
#   $BROWSER scripts/rigc/.reports/junit-rigc.html
"$PY" -m coverage html --rcfile="$CFG" -q -d .reports/coverage-rigc-html
[ -f .reports/junit-rigc.xml ] && \
    "$PY" junit_html.py .reports/junit-rigc.xml .reports/junit-rigc.html
[ "$rigc_status" -eq 0 ] || exit "$rigc_status"
[ "$coverage_status" -eq 0 ] || {
    echo "check.sh: rigc unit coverage below the fail_under floor" >&2
    exit "$coverage_status"
}

echo "== pytest: rigc integration =="
# A SEPARATE invocation from the unit run above, and it must stay separate:
# coverage is measured over the in-process unit layer only, because this suite
# drives the CLI as a subprocess, which `coverage` cannot see inside. Folding
# the two together would dilute the figure with subprocess work it never
# measures, not raise it.
if [ -n "$CHECK_FAST" ]; then
    suite=fast
else
    suite=full
fi
frozen_status=0
if [ -n "$CHECK_FAST" ]; then
    "$PY" -m pytest -c "$CFG" --rootdir=. -m "not build" tests/integration \
        --durations=25 --junitxml=".reports/junit-$suite.xml" || frozen_status=$?
else
    "$PY" -m pytest -c "$CFG" --rootdir=. tests/integration \
        --durations=25 --junitxml=".reports/junit-$suite.xml" || frozen_status=$?
fi
#   $BROWSER scripts/rigc/.reports/junit-full.html
[ -f ".reports/junit-$suite.xml" ] && \
    "$PY" junit_html.py ".reports/junit-$suite.xml" ".reports/junit-$suite.html"
[ "$frozen_status" -eq 0 ] || exit "$frozen_status"

echo "check.sh: ALL GREEN"
