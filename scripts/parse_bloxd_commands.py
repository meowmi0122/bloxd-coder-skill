#!/usr/bin/env python3
"""Extract and classify slash commands from Bloxd.io notes or source code."""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

CATEGORIES = {
    "mute": {"mute", "unmute", "silence", "unsilence"},
    "name_effect": {"name", "nickname", "nametag", "title", "prefix", "suffix"},
    "player_management": {"kick", "ban", "unban", "op", "deop", "whitelist"},
    "teleport": {"tp", "teleport", "spawn", "home", "warp"},
    "moderation": {"warn", "jail", "freeze", "kill", "clear"},
}

COMMAND_RE = re.compile(r"(?<!\w)/([A-Za-z][A-Za-z0-9_-]*)(?:\s+([^\n\r`]+))?")


def classify(name: str) -> str:
    lowered = name.lower()
    for category, names in CATEGORIES.items():
        if lowered in names:
            return category
    return "other"


def extract(text: str) -> list[dict[str, str]]:
    results = []
    for match in COMMAND_RE.finditer(text):
        name, args = match.group(1), (match.group(2) or "").strip()
        results.append({"command": f"/{name}", "arguments": args, "category": classify(name)})
    return results


def ordered(results: list[dict[str, str]]) -> list[dict[str, str]]:
    """Keep mute before name-effect commands, as required by the skill."""
    order = {"mute": 0, "name_effect": 1, "player_management": 2, "teleport": 3, "moderation": 4, "other": 5}
    return sorted(results, key=lambda item: (order[item["category"]], item["command"]))


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path, help="Text or source file to scan")
    parser.add_argument("--json", action="store_true", help="Print JSON instead of a readable list")
    args = parser.parse_args()
    data = ordered(extract(args.input.read_text(encoding="utf-8")))
    if args.json:
        print(json.dumps(data, ensure_ascii=False, indent=2))
        return
    for item in data:
        suffix = f" {item['arguments']}" if item["arguments"] else ""
        print(f"[{item['category']}] {item['command']}{suffix}")


if __name__ == "__main__":
    main()
