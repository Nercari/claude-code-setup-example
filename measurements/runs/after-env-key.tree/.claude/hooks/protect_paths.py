#!/usr/bin/env python3
"""PreToolUse hook: block edits to protected paths. Standard library only.

Claude Code sends the tool call as JSON on stdin. Exit code 2 blocks the call
and the message on stderr is shown to Claude. Exit 0 lets the normal
permission flow continue.

Fail-open on unreadable input: a broken hook must not freeze all work.
"""
import json
import re
import sys
from pathlib import PurePosixPath

# Directory names that are protected anywhere in the path.
PROTECTED_DIRS = {"migrations"}
# File names (regex) that are protected. .env.example is allowed on purpose.
PROTECTED_FILES = [re.compile(r"^\.env$"), re.compile(r"^\.env\.(?!example$).+")]


def protected_reason(file_path):
    """Return a reason string if file_path is protected, else None."""
    parts = PurePosixPath(str(file_path).replace("\\", "/")).parts
    if not parts:
        return None
    for part in parts[:-1]:
        if part in PROTECTED_DIRS:
            return f"'{part}/' is protected (applied migrations are never edited)"
    name = parts[-1]
    for pattern in PROTECTED_FILES:
        if pattern.match(name):
            return f"'{name}' holds secrets and is protected"
    return None


def main():
    try:
        event = json.load(sys.stdin)
        tool_input = event.get("tool_input") or {}
        file_path = tool_input.get("file_path") or tool_input.get("path")
    except Exception:
        return 0
    if not isinstance(file_path, str) or not file_path:
        return 0
    reason = protected_reason(file_path)
    if reason:
        print(f"Blocked by protect_paths hook: {reason}. Ask the user before changing it.", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
