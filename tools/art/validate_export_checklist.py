#!/usr/bin/env python3
"""Check an auditable Factorio sprite-export work order; this is NOT a render or game test.

Usage:
  python3 tools/art/validate_export_checklist.py path/to/ASSET_PRODUCTION_EXPORT_CHECKLIST.md
  python3 tools/art/validate_export_checklist.py path/to/work-order.md --require export
  python3 tools/art/validate_export_checklist.py path/to/work-order.md --require publish
"""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

GATES = tuple("P%02d" % number for number in range(13))
STATES = {"PASS", "PENDING", "IN_PROGRESS", "BLOCKED", "NOT_APPLICABLE"}
REQUIRED_FOR_STAGE = {
    "plan": (),
    "calibrate": GATES[:6],
    "export": GATES[:10],
    "publish": GATES,
}
MISSING = {"", "-", "—", "TBD", "TODO", "NONE", "N/A"}
GATE_ID = re.compile(r"^(P\d\d)(?:\s|$)")


def inspect(content: str, required_stage: str = "plan") -> tuple[list[str], dict[str, dict[str, str]]]:
    issues = []
    rows = {}
    for line_number, line in enumerate(content.splitlines(), start=1):
        if not line.lstrip().startswith("|"):
            continue
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        if not cells:
            continue
        m = GATE_ID.match(cells[0])
        if not m:
            continue
        gate = m.group(1)
        if gate in rows:
            issues.append(f"line {line_number}: duplicate gate {gate}")
            continue
        if gate not in GATES:
            issues.append(f"line {line_number}: unknown gate {gate}")
            continue
        if len(cells) < 3:
            issues.append(f"line {line_number}: {gate} needs status and evidence cells")
            continue
        status = cells[1].upper()
        evidence = cells[2]
        rows[gate] = {"status": status, "evidence": evidence, "line": str(line_number)}
        if status not in STATES:
            issues.append(f"line {line_number}: {gate} has invalid status {status}")
        elif status in {"PASS", "NOT_APPLICABLE"} and evidence.upper() in MISSING:
            issues.append(f"line {line_number}: {gate} {status} lacks audit evidence/reason")

    for gate in GATES:
        if gate not in rows:
            issues.append("missing " + gate)

    for gate in REQUIRED_FOR_STAGE[required_stage]:
        row = rows.get(gate)
        if row is None:
            continue
        if row["status"] != "PASS" and row["status"] != "NOT_APPLICABLE":
            issues.append(f"{gate} not cleared for {required_stage}: {row['status']}")
    return issues, rows


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("work_order", type=Path)
    parser.add_argument("--require", choices=REQUIRED_FOR_STAGE, default="plan")
    parser.add_argument("--json", action="store_true", help="Machine-readable report")
    args = parser.parse_args()
    try:
        content = args.work_order.read_text(encoding="utf-8")
    except OSError as exc:
        parser.error(str(exc))
    issues, rows = inspect(content, args.require)
    next_gate = next((gate for gate in GATES
                      if gate not in rows or rows[gate]["status"] not in {"PASS", "NOT_APPLICABLE"}), None)
    report = {
        "file": str(args.work_order),
        "required_stage": args.require,
        "ready_for_stage": not issues,
        "gate_count": len(rows),
        "passed": sum(v["status"] == "PASS" for v in rows.values()),
        "next_gate": next_gate,
        "issues": issues,
        "note": "Static checklist only; passing does not prove Blender output, visual approval, or Factorio load.",
    }
    if args.json:
        print(json.dumps(report, indent=2))
    else:
        print(f"Export work order {args.work_order}: {len(rows)}/{len(GATES)} gates recorded")
        print("Next unresolved gate:", next_gate or "none")
        for issue in issues:
            print("BLOCK:", issue)
        print("PASS: static checklist format" if not issues else "BLOCKED: required gates unresolved or malformed")
        print(report["note"])
    return 0 if not issues else 1


if __name__ == "__main__":
    raise SystemExit(main())
