# Claude Code setup: before and after

Sample deliverable for a "set up Claude Code for your project" gig. The project is a small fictional inventory tool called **tidyshelf** (Python, three modules, nine tests). All data is invented.

## The problem

Out of the box, Claude Code knows nothing about your project. It guesses the test command, may edit files you never want touched (old database migrations, secrets files), asks permission for every harmless command, and has no checklist for "is this finished?". You end up repeating the same instructions in every session.

## What was added (folder `after/`)

| Piece | What it does | Why it matters |
|---|---|---|
| `CLAUDE.md` | Stack, exact commands, conventions, a "do not touch" list, and a definition of done | Claude starts every session already knowing how your project works and when it may say "done" |
| `.claude/settings.json` permissions | Test, lint and read-only git commands are pre-approved. Reading `.env`, `rm -rf` and force-push are denied | Fewer permission prompts for safe work, a hard stop for dangerous work |
| `.claude/hooks/protect_paths.py` (+ tests) | Before any file edit, blocks changes inside `migrations/` and to `.env` files, and tells Claude why | A rule enforced by code, not a request Claude can forget. `.env.example` stays editable |
| Skill `add-cli-command` | A fixed recipe for adding a command: logic, parser, tests, README | New features come out the same way every time |
| Skill `release-notes` | Turns the git log into plain-English notes, with an "unsure" list instead of guesses | Changelogs you can paste to customers |
| Subagent `reviewer` | Read-only reviewer that runs the tests and checks the change against `CLAUDE.md` | A second look before work counts as finished. It cannot edit files |

`before/` is the same project with none of this, for comparison.

## How to verify

    python samples/c1_claude_code_setup/check.py

It prints PASS or FAIL for each check and exits with an error if any fail. It checks that the JSON is valid, every hook script exists, the hook's own tests pass, the hook really blocks `migrations/` and `.env` when run, the skills and subagent have the required name and description, and that the test command written in `CLAUDE.md` actually passes on the project. Python standard library only.

## Honest limits

- This does not guarantee fewer bugs. It reduces repeated mistakes and makes risky actions harder; it does not replace reading the results.
- The hook guards Claude's file-edit tools. It does not inspect shell commands, so a shell command that rewrites a protected file is not caught by this hook. The deny rules in `settings.json` cover only the specific commands listed.
- I checked the file formats against the current Claude Code documentation, but I did not run a live Claude Code session in this sample. The check script proves the files are well formed and the hook logic works, not how the model behaves.
- Rules in `CLAUDE.md` are guidance the model follows most of the time; only the permissions and the hook are enforced by the program.
- Your real project needs its own paths, commands and rules; this is a worked example, not a template to paste.
