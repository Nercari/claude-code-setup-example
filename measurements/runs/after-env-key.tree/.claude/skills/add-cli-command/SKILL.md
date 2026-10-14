---
name: add-cli-command
description: Add a new subcommand to the tidyshelf CLI with its storage logic and tests. Use when the user asks for a new command, flag or action such as "add a search command".
---

# Add a CLI command

Follow this order so the change stays small and tested.

1. Read `CLAUDE.md` conventions first.
2. Put the logic in `tidyshelf/storage.py` as a plain function that takes the db path. Raise `ValueError` or `KeyError` for user errors.
3. Register the subcommand in `build_parser()` in `tidyshelf/cli.py`, and handle it in `main()` by calling the storage function and printing one line per result.
4. Add tests: one for the storage function, one in `tests/test_cli.py` using the existing `run_cli` helper. Cover one success and one error case.
5. Run `python3 -m unittest discover -s tests -t .` and show the output.
6. Add one line about the command to `README.md`.

Do not add dependencies. Do not change `migrations/`.
