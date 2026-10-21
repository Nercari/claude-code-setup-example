# Review guide

## Hard stops
- Do not merge, close or edit nercari-control PR #97. Do not force-push. Do not push to main (AGENTS.md).
- Do not commit secrets or `.env` files (AGENTS.md hard stops).
- Do not edit `after/migrations/`. `after/CLAUDE.md` says applied migrations are never edited.
- Do not edit `after/.claude/settings.json` or `after/.claude/hooks/` without asking (`after/CLAUDE.md`).
- Do not remove `.cursor/hooks/merge-gate.mjs`. It denies `gh pr merge` and pushes to main or master.

## Fragile files
- `after/.claude/hooks/protect_paths.py`: blocks edits to `migrations/` and `.env`. It fails open on unreadable input by design.
- `after/.claude/settings.json`: deny rules for `.env`, `rm -rf` and force push. `check.py` tests them.
- `measurements/runs/`: stored run records that back the README claims. Do not edit by hand.
- `.cursor/hooks/merge-gate.mjs`, `.claude/settings.json`: added in commit 3fed7fc (merge gate).

## Tests that must pass
- `python3 check.py` (CI step "Setup checks (11)"). Run on 2026-10-21: 11/11 checks passed.
- `python3 -m unittest discover -s tests -t .` inside `after/` (from `after/CLAUDE.md`). Run by `check.py`.
