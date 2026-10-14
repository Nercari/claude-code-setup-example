# Claude Code setup example — measured, fictional demo by Nercari

[![checks](https://github.com/Nercari/claude-code-setup-example/actions/workflows/checks.yml/badge.svg)](https://github.com/Nercari/claude-code-setup-example/actions/workflows/checks.yml)
[![Live demo](https://img.shields.io/badge/live%20demo-nercari.github.io-blue)](https://nercari.github.io/claude-code-setup-example/)
[![llms.txt](https://img.shields.io/badge/llms.txt-ready-green)](./llms.txt)

**What a buyer gets:** `CLAUDE.md`, safe permissions (allow/deny), hooks that block risky edits, project skills, a read-only reviewer subagent, an MCP config, and a pull request with a short written guide.

> Fictional demo only. Shelvanta is not a real product and is not client work. Numbers below come from reproducible local runs dated **2026-10-14**.

## Did the setup stop risky edits?

Same 5 prompts (`measurements/tasks.md`) run with Claude Code on a fresh copy of `before/` (no setup) and `after/` (this setup). Same model, same scoped tool list, default permission mode, no bypass.

| | before/ (no setup) | after/ (setup) | How to reproduce |
|---|---|---|---|
| Risky requests that changed a protected file (`.env`, applied migration) | **2 of 2** | **0 of 2** | see `measurements/` run logs |
| Edits blocked by the hook | 0 | 2 (both on `migrations/001_init.sql`) | hook subprocess in `check.py` |
| `.env` request | file created with the key | refused, citing the CLAUDE.md rule | same |

Static setup checks: `python3 check.py` → **11/11** (settings parse, deny rules cover `.env` / `rm -rf` / force push, hook tests pass, live hook block, skills and subagent valid, CLAUDE.md test command passes).

The setup's value here is **safety**, not speed. There is no time-saved claim.

## Live demo

[nercari.github.io/claude-code-setup-example](https://nercari.github.io/claude-code-setup-example/) — Shelvanta landing page with schema, sitemap, robots (AI crawlers allowed) and `llms.txt`.

## What's in this repo?

- `before/` and `after/` — the sample CLI without and with the setup
- `check.py` — the 11 CI checks
- `measurements/` — prompts, run logs and scoring
- `docs/pages/` — the GitHub Pages site
- `llms.txt` — machine-readable summary for AI crawlers

## FAQ

### Will this make Claude Code faster?
Not the claim this demo makes. The measured win is that risky edits to protected paths were blocked while normal edits still went through.

### Is Shelvanta a real app?
No. It is a small fictional inventory CLI built so the setup and the measurements can be public.

### Does the hook replace human review?
No. Hooks enforce the deny list you choose. A reviewer still owns the merge.

## Order / related

**Order a setup:** [Fiverr gig](https://www.fiverr.com/nercari/PLACEHOLDER-claude-code-setup) · [Claude skill examples](https://github.com/Nercari/claude-skill-examples) · [SEO/GEO/AEO audit](https://github.com/Nercari/seo-geo-aeo-audit-demo) · [Nercari profile](https://github.com/Nercari/Nercari)

Delivery-only. No video calls, voice or face content.
