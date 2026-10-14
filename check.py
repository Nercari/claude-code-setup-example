#!/usr/bin/env python3
import json
import re
import shlex
import shutil
import subprocess
import sys
from pathlib import Path

AFTER = Path(__file__).resolve().parent / "after"
BEFORE = Path(__file__).resolve().parent / "before"
RESULTS = []


def check(name):
    def deco(fn):
        try:
            detail = fn()
            RESULTS.append((name, True, detail or ""))
        except Exception as exc:
            RESULTS.append((name, False, f"{type(exc).__name__}: {exc}"))
        return fn
    return deco


def frontmatter(path):
    text = path.read_text(encoding="utf-8")
    m = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    assert m, f"{path.name}: no frontmatter block at top of file"
    fields = {}
    for line in m.group(1).splitlines():
        if ":" in line and not line.startswith(" "):
            k, v = line.split(":", 1)
            fields[k.strip()] = v.strip()
    return fields


def run(cmd, cwd):
    return subprocess.run(cmd, cwd=cwd, capture_output=True, text=True)


@check("before/ has no Claude config")
def _():
    assert not (BEFORE / ".claude").exists(), ".claude/ found in before/"
    assert not (BEFORE / "CLAUDE.md").exists(), "CLAUDE.md found in before/"


@check("settings.json parses and has allow, deny, hooks")
def _():
    s = json.loads((AFTER / ".claude/settings.json").read_text(encoding="utf-8"))
    perms = s["permissions"]
    assert perms["allow"] and perms["deny"], "allow/deny must not be empty"
    assert "PreToolUse" in s["hooks"], "no PreToolUse hook"
    return f"{len(perms['allow'])} allow, {len(perms['deny'])} deny"


@check("deny rules cover .env, rm -rf and force push")
def _():
    deny = json.loads((AFTER / ".claude/settings.json").read_text())["permissions"]["deny"]
    joined = "\n".join(deny)
    for needle in ("Read(./.env)", "rm -rf", "git push --force"):
        assert needle in joined, f"missing deny rule containing {needle!r}"


@check("every hook command points to an existing script")
def _():
    s = json.loads((AFTER / ".claude/settings.json").read_text())
    n = 0
    for groups in s["hooks"].values():
        for group in groups:
            for h in group["hooks"]:
                assert h["type"] == "command", "unexpected hook type"
                for tok in shlex.split(h["command"]):
                    if tok.endswith(".py") or tok.endswith(".sh"):
                        rel = tok.replace("${CLAUDE_PROJECT_DIR}", "").lstrip("/")
                        assert (AFTER / rel).is_file(), f"missing script: {rel}"
                        n += 1
    assert n, "no script referenced"
    return f"{n} script(s) found"


@check("hook tests pass (subprocess)")
def _():
    r = run([sys.executable, "-m", "unittest", "discover", "-s", ".claude/hooks", "-p", "test_*.py"], AFTER)
    assert r.returncode == 0, r.stderr[-400:]
    return r.stderr.strip().splitlines()[-1] if r.stderr.strip() else "OK"


@check("hook blocks migrations/ and .env, allows source files (live run)")
def _():
    hook = AFTER / ".claude/hooks/protect_paths.py"
    for path, code in (("migrations/001_init.sql", 2), (".env", 2), ("shelvanta/cli.py", 0)):
        payload = json.dumps({"tool_name": "Edit", "tool_input": {"file_path": path}})
        r = subprocess.run([sys.executable, str(hook)], input=payload, capture_output=True, text=True)
        assert r.returncode == code, f"{path}: expected exit {code}, got {r.returncode}"


@check("skills have name + description, name matches folder")
def _():
    dirs = sorted(p for p in (AFTER / ".claude/skills").iterdir() if p.is_dir())
    assert len(dirs) >= 2, "need at least 2 skills"
    for d in dirs:
        fm = frontmatter(d / "SKILL.md")
        assert fm.get("name") == d.name, f"{d.name}: name {fm.get('name')!r} != folder"
        assert fm.get("description"), f"{d.name}: empty description"
    return ", ".join(d.name for d in dirs)


@check("subagent has name + description and is read-only")
def _():
    fm = frontmatter(AFTER / ".claude/agents/reviewer.md")
    assert fm.get("name") and fm.get("description"), "name/description missing"
    assert "Write" not in fm.get("tools", ""), "reviewer must not be given Write"
    assert "Write" in fm.get("disallowedTools", ""), "reviewer must disallow Write/Edit"
    return fm["name"]


@check("CLAUDE.md has required sections")
def _():
    text = (AFTER / "CLAUDE.md").read_text(encoding="utf-8")
    for h in ("## Commands", "## Conventions", "## Do not touch", "## Done means"):
        assert h in text, f"missing section {h}"


@check("CLAUDE.md test command passes on after/ project")
def _():
    text = (AFTER / "CLAUDE.md").read_text(encoding="utf-8")
    m = re.search(r"- Test: `([^`]+)`", text)
    assert m, "no '- Test: `...`' line in CLAUDE.md"
    cmd = shlex.split(m.group(1))
    if cmd[0] == "python3":
        cmd[0] = sys.executable
    r = run(cmd, AFTER)
    assert r.returncode == 0, (r.stdout + r.stderr)[-400:]
    return r.stderr.strip().splitlines()[-1]


@check("protected paths named in CLAUDE.md exist in project")
def _():
    assert (AFTER / "migrations").is_dir(), "migrations/ missing"


def main():
    for name, ok, detail in RESULTS:
        print(f"{'PASS' if ok else 'FAIL'}  {name}" + (f"  [{detail}]" if detail else ""))
    failed = [n for n, ok, _ in RESULTS if not ok]
    print(f"\n{len(RESULTS) - len(failed)}/{len(RESULTS)} checks passed")
    for p in AFTER.rglob("__pycache__"):
        shutil.rmtree(p, ignore_errors=True)
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
