#!/usr/bin/env python3
"""Regression tests for Factorio sprite-production work-order parsing."""
import unittest
from pathlib import Path
import importlib.util

SRC = Path(__file__).with_name("validate_export_checklist.py")
spec = importlib.util.spec_from_file_location("validate_export_checklist", SRC)
check = importlib.util.module_from_spec(spec)
spec.loader.exec_module(check)


def fixture(status="PENDING", evidence="—"):
    lines = ["| Gate | Status | Evidence |", "| --- | --- | --- |"]
    lines += [f"| {key} sample action | {status} | {evidence} |" for key in check.GATES]
    return "\n".join(lines)


class ChecklistAuditTests(unittest.TestCase):
    def test_all_pending_is_valid_plan_not_export(self):
        issues, rows = check.inspect(fixture())
        self.assertEqual(issues, [])
        self.assertEqual(len(rows), 13)
        issues, _ = check.inspect(fixture(), "export")
        self.assertTrue(any("P00 not cleared" in x for x in issues))

    def test_pass_needs_evidence(self):
        issues, _ = check.inspect(fixture(status="PASS"))
        self.assertEqual(len(issues), 13)

    def test_complete_with_evidence_is_structurally_publish_ready(self):
        issues, _ = check.inspect(fixture(status="PASS", evidence="commit abc123 / log path"),
                                  "publish")
        self.assertEqual(issues, [])

    def test_duplicate_and_missing_gates_fail(self):
        lines = fixture().splitlines()
        lines = lines[:-1] + [lines[2]]
        issues, _ = check.inspect("\n".join(lines))
        self.assertTrue(any("duplicate gate P00" in x for x in issues))
        self.assertTrue(any("missing P12" in x for x in issues))

    def test_bad_state_detected(self):
        issues, _ = check.inspect(fixture().replace("| P03 sample action | PENDING", "| P03 sample action | DONE"))
        self.assertTrue(any("invalid status DONE" in x for x in issues))

    def test_not_applicable_needs_reason(self):
        issues, _ = check.inspect(fixture("NOT_APPLICABLE", "—"))
        self.assertEqual(len(issues), 13)


if __name__ == "__main__":
    unittest.main()
