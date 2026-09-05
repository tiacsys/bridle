# Copyright (c) 2026 TiaC Systems
# SPDX-License-Identifier: Apache-2.0
"""Render a pytest --junitxml file as one self-contained HTML page.

Stdlib only, deliberately — the same no-new-dependency rule as driving
coverage.py directly (pyproject.toml [tool.coverage.*]). check.sh calls
this after EVERY pytest invocation, including failed ones (the status is
captured and re-raised after rendering): a red run is precisely when a
browsable report is worth having.

Usage: junit_html.py <junit.xml> <out.html>

Layout: suite summary up top; failures and errors first, each expandable
to the full captured message; then every module with its own pass/fail
counts and per-test rows. Companion to timing_report.py, which reads the
same files for wall-time diffing.
"""

from __future__ import annotations

import html
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

_CSS = """
body { font: 14px/1.5 system-ui, sans-serif; margin: 2rem auto;
       max-width: 60rem; padding: 0 1rem; }
h1 { font-size: 1.3rem; } h2 { font-size: 1.1rem; margin-top: 2rem; }
table { border-collapse: collapse; width: 100%; }
td, th { text-align: left; padding: .15rem .6rem .15rem 0;
         border-bottom: 1px solid #8884; }
td.t { text-align: right; font-variant-numeric: tabular-nums; }
.badge { display: inline-block; min-width: 4.5em; text-align: center;
         border-radius: .3em; padding: 0 .4em; font-size: .85em; }
.pass { background: #2e7d3222; color: #2e7d32; }
.fail { background: #c6282822; color: #c62828; }
.skip { background: #f9a82522; color: #9a6700; }
summary { cursor: pointer; margin: .3rem 0; }
pre { background: #8881; padding: .6rem; overflow-x: auto; font-size: .85em; }
@media (prefers-color-scheme: dark) {
  body { background: #1c1c1c; color: #ddd; }
  .pass { color: #7bc67e; } .fail { color: #ef9a9a; } .skip { color: #e0b856; }
}
"""


def _status(tc: ET.Element) -> tuple[str, ET.Element | None]:
    for kind in ("error", "failure", "skipped"):
        node = tc.find(kind)
        if node is not None:
            return ("skip" if kind == "skipped" else "fail", node)
    return "pass", None


def _testcases(root: ET.Element) -> list[ET.Element]:
    return list(root.iter("testcase"))


def render(xml_path: Path) -> str:
    root = ET.parse(xml_path).getroot()
    suites = root.findall("testsuite") if root.tag == "testsuites" else [root]
    cases = _testcases(root)

    counts = {"pass": 0, "fail": 0, "skip": 0}
    rows_by_module: dict[str, list[str]] = {}
    failures: list[str] = []
    total_time = 0.0
    for tc in cases:
        status, detail = _status(tc)
        counts[status] += 1
        module = (tc.get("classname") or "?").rsplit(".", 1)[-1]
        name = tc.get("name") or "?"
        time = float(tc.get("time") or 0.0)
        total_time += time
        badge = {"pass": "passed", "fail": "FAILED", "skip": "skipped"}[status]
        rows_by_module.setdefault(module, []).append(
            f"<tr><td><span class='badge {status}'>{badge}</span></td>"
            f"<td>{html.escape(name)}</td><td class='t'>{time:.2f}s</td></tr>"
        )
        if status == "fail" and detail is not None:
            text = html.escape((detail.get("message") or "") + "\n" + (detail.text or ""))
            failures.append(
                f"<details><summary><span class='badge fail'>FAILED</span> "
                f"{html.escape(module)}::{html.escape(name)}</summary>"
                f"<pre>{text}</pre></details>"
            )

    suite_name = ", ".join(s.get("name") or "?" for s in suites)
    stamp = ", ".join(filter(None, (s.get("timestamp") for s in suites)))
    parts = [
        "<!DOCTYPE html><html><head><meta charset='utf-8'>",
        f"<title>{html.escape(xml_path.name)}</title>",
        f"<style>{_CSS}</style></head><body>",
        f"<h1>{html.escape(xml_path.name)} — {html.escape(suite_name)}</h1>",
        f"<p><span class='badge pass'>{counts['pass']} passed</span> "
        f"<span class='badge fail'>{counts['fail']} failed</span> "
        f"<span class='badge skip'>{counts['skip']} skipped</span> "
        f"— {total_time:.1f}s test time"
        f"{' — ' + html.escape(stamp) if stamp else ''}</p>",
    ]
    if failures:
        parts.append(f"<h2>Failures ({len(failures)})</h2>")
        parts += failures
    for module in sorted(rows_by_module):
        rows = rows_by_module[module]
        parts.append(
            f"<h2>{html.escape(module)} ({len(rows)})</h2><table>" + "".join(rows) + "</table>"
        )
    parts.append("</body></html>")
    return "".join(parts)


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print("usage: junit_html.py <junit.xml> <out.html>", file=sys.stderr)
        return 2
    xml_path, out_path = Path(argv[0]), Path(argv[1])
    out_path.write_text(render(xml_path))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
