---
trigger: always_on
description: Keep shell commands unchained so prefix-based auto-approval works reliably
---

# Terminal Command Execution

- Never chain multiple commands with `&&`, `;`, or `||` in a single `run_command` call—especially for `git` and `gh` commands. Run each command as its own separate `run_command` call so prefix-based "Always allow" approvals apply.
- Piping with `|` is fine when needed, though prefer native flags like `gh --json` / `gh --jq` when available.
- Avoid command substitutions (`$(...)`, backticks) and unnecessary shell variable expansions (`$VAR`) in `run_command` calls when literal values can be passed directly.
