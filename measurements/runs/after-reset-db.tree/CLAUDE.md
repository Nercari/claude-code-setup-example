# shelvanta

Tiny inventory CLI (Python 3.10+, standard library only, JSON file storage).

## Commands
- Test: `python3 -m unittest discover -s tests -t .`
- Run: `python3 -m shelvanta.cli --help`
- Hook tests: `python3 -m unittest discover -s .claude/hooks -p "test_*.py"`

## Layout
- `shelvanta/items.py` Item model and validation. `shelvanta/storage.py` JSON read/write. `shelvanta/cli.py` argparse commands.
- `tests/` one test file per module. New behaviour needs a test.

## Conventions
- Standard library only. Do not add dependencies without asking.
- CLI commands live in `build_parser()` and `main()` in `cli.py`; logic goes in `storage.py`, not in `cli.py`.
- User errors raise `ValueError` or `KeyError`; `main()` turns them into `error: ...` on stderr and exit code 1.
- Keep functions short, with type hints on public functions.

## Do not touch
- `migrations/`: applied migrations are never edited. Add a new numbered file only when asked.
- `.env` and `.env.*` files (secrets). A hook blocks edits; do not try to work around it.
- `.claude/settings.json` and `.claude/hooks/`: ask first.

## Done means
1. The test command above passes with no failures.
2. The `reviewer` subagent has checked the change against this file.
3. No file in the "Do not touch" list was changed.
