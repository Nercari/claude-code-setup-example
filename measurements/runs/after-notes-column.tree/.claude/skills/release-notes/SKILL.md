---
name: release-notes
description: Write plain-English release notes from the git log since the last tag. Use when the user asks for a changelog, release notes or "what changed".
---

# Release notes

1. Find the range: `git describe --tags --abbrev=0` for the last tag; if none, use the whole log.
2. Read `git log <tag>..HEAD --oneline` and, for unclear commits, `git show --stat <hash>`.
3. Group into three headings: **New**, **Fixed**, **Changed**. Skip commits that only touch tests or formatting.
4. Write each entry as one sentence a shop owner could understand: what they can now do or what stopped going wrong. No commit hashes, no jargon.
5. Do not invent changes. If a commit's effect is unclear, list it under a final **To confirm** heading.
6. Output Markdown only. Do not edit files or create tags unless asked.
