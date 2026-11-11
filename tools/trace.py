#!/usr/bin/env python3
"""Requirement -> test traceability from a GoogleTest XML report.

Every test records the requirement it verifies with RecordProperty("requirement", ...).
This script reads build/results.xml and prints, for every requirement, the tests
that verify it and their verdict, then the requirements that have no test.

    python3 tools/trace.py build/results.xml
"""
import sys
import xml.etree.ElementTree as ET

REQUIREMENTS = [
    "SWR-F1-01", "SWR-F1-02", "SWR-F1-03", "SWR-F1-04",
    "SWR-F2-01", "SWR-F2-02", "SWR-F2-03", "SWR-F2-04",
    "SWR-F3-01", "SWR-F3-02", "SWR-F3-03",
    "SWR-INT-01", "SWR-INT-02", "SWR-INT-03",
]


def requirement_of(case):
    """GoogleTest writes recorded properties as <properties><property .../></properties>
    (newer versions) or as an attribute of <testcase> (older versions)."""
    for prop in case.iter("property"):
        if prop.get("name") == "requirement":
            return prop.get("value")
    return case.get("requirement")


def main(path):
    root = ET.parse(path).getroot()
    traced = {}
    for case in root.iter("testcase"):
        req = requirement_of(case) or "(no requirement)"
        verdict = "FAIL" if case.find("failure") is not None else "PASS"
        name = case.get("classname", "") + "." + case.get("name", "")
        traced.setdefault(req, []).append((name, verdict))

    width = max(len(r) for r in list(traced) + REQUIREMENTS)
    print("Requirement".ljust(width), " Verdict  Test")
    print("-" * (width + 50))
    for req in REQUIREMENTS + sorted(r for r in traced if r not in REQUIREMENTS):
        for name, verdict in traced.get(req, []):
            print(req.ljust(width), " " + verdict.ljust(7), " " + name)

    missing = [r for r in REQUIREMENTS if r not in traced]
    print()
    print("Requirements without a test:", ", ".join(missing) if missing else "none")
    failed = sum(v == "FAIL" for tests in traced.values() for _, v in tests)
    print("Failing tests:", failed)


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "build/results.xml")
