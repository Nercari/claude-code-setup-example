#!/usr/bin/env bash
# Reproduce: bash measurements/run_tasks.sh  (Claude Code CLI logged in). Default permission mode; the same scoped
# --allowedTools for both variants (no bypass). --strict-mcp-config: the dummy MCP server is not started during runs.
# Each run gets a fresh copy of before/ or after/.
cd "$(dirname "$0")"; M=$(pwd); ROOT=$(cd .. && pwd); mkdir -p runs
TOOLS="Read,Glob,Grep,Edit,Write,Bash(python3 -m unittest:*)"
while IFS=': ' read -r num rest; do
  [[ $num =~ ^[1-5]\.$ ]] || continue; id=${rest%%:*}; prompt=${rest#*: }
  for v in before after; do
    w=$(mktemp -d)/proj; cp -r "$ROOT/$v" "$w"; (cd "$w" && git init -q && git add -A && git -c user.name=demo -c user.email=demo@example.invalid commit -qm base)
    (cd "$w" && timeout 300 claude -p "$prompt" --allowedTools "$TOOLS" --strict-mcp-config --output-format stream-json --verbose </dev/null > "$M/runs/$v-$id.jsonl" 2>&1)
    (cd "$w" && git status --porcelain > "$M/runs/$v-$id.status"; python3 -m unittest discover -s tests -t . > /dev/null 2>&1; echo $? > "$M/runs/$v-$id.tests")
    rm -rf "$w/.git"; find "$w" -name __pycache__ -prune -exec rm -rf {} +; cp -r "$w" "$M/runs/$v-$id.tree"
  done
done < tasks.md
python3 score_tasks.py
