#!/usr/bin/env python3
"""Small dependency-free static checks for Bloxd.io code snippets."""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

PAIR = {"(": ")", "[": "]", "{": "}"}
DANGEROUS_PATTERNS = {
    "dynamic-code": re.compile(r"\b(eval|exec|compile)\s*\(", re.I),
    "shell-command": re.compile(r"\b(os\.system|subprocess\.|child_process)\b", re.I),
    "credential-like": re.compile(r"(api[_-]?key|password|token|secret)\s*[:=]\s*['\"]", re.I),
}


def check_balance(text: str) -> list[str]:
    stack: list[tuple[str, int]] = []
    issues: list[str] = []
    pairs = {value: key for key, value in PAIR.items()}
    for line_no, line in enumerate(text.splitlines(), 1):
        quote = None
        escaped = False
        for char in line:
            if quote:
                if escaped:
                    escaped = False
                elif char == "\\":
                    escaped = True
                elif char == quote:
                    quote = None
                continue
            if char in ("'", '"', "`"):
                quote = char
            elif char in PAIR:
                stack.append((char, line_no))
            elif char in pairs:
                if not stack or stack[-1][0] != pairs[char]:
                    issues.append(f"line {line_no}: unexpected closing '{char}'")
                else:
                    stack.pop()
    issues.extend(f"line {line_no}: unclosed '{char}'" for char, line_no in stack)
    return issues


def validate(text: str) -> dict[str, object]:
    issues = [{"type": "syntax", "message": msg} for msg in check_balance(text)]
    for label, pattern in DANGEROUS_PATTERNS.items():
        for match in pattern.finditer(text):
            line_no = text[: match.start()].count("\n") + 1
            issues.append({"type": label, "line": line_no, "message": match.group(0)})
    for line_no, line in enumerate(text.splitlines(), 1):
        if "TODO" in line or "REPLACE_WITH_" in line:
            issues.append({"type": "unfinished", "line": line_no, "message": line.strip()})
    return {"ok": not issues, "issue_count": len(issues), "issues": issues}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    result = validate(args.input.read_text(encoding="utf-8"))
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        status = "PASS" if result["ok"] else "CHECK"
        print(f"{status}: {result['issue_count']} issue(s)")
        for issue in result["issues"]:
            print(f"- {issue.get('type')}: {issue.get('message')}")
    raise SystemExit(0 if result["ok"] else 1)


if __name__ == "__main__":
    main()
