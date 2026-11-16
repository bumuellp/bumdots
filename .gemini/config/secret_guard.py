#!/usr/bin/env python3
"""PreToolUse hook to enforce glob/regex blocks for secret files and commands."""

import fnmatch
import json
import os
import re
import shlex
import sys
from pathlib import Path

FILE_TOOLS = {"read_file", "view_file", "write_file", "edit_file"}

# Replaces read_file(**/.env*), read_file(**/*id_rsa*), and home dotdirs
DENIED_PATH_GLOBS = [
    "*/.env",
    "*/.env.*",
    "*/*id_rsa*",
    "*/*id_ed25519*",
    "*/.ssh",
    "*/.ssh/*",
    "*/.gnupg",
    "*/.gnupg/*",
    "*/.aws",
    "*/.aws/*",
    "*/.kube",
    "*/.kube/*",
    "*/.config/sops",
    "*/.config/sops/*",
    "*/age/keys.txt",
    "*/*.agekey",
    "*/*age*key*.txt",
    "*/.vault-token",
    "*/.config/gcloud/*",
    "*/.azure/*",
]

ALLOWED_PATH_EXCEPTIONS = [
    "*/.env.example",
    "*/.env.template",
    "*/tests/.env.test",
]

# Catches shell commands referencing .env*, id_rsa*, ~/.ssh, etc.
COMMAND_SECRET_RE = re.compile(
    r"(?:^|[/\s\"'=])(?:\.env(?:\.[A-Za-z0-9_-]+)?|.*id_rsa.*|.*id_ed25519.*|\.ssh|\.gnupg|\.aws|\.kube|\.config/sops|.*\.agekey|age/keys\.txt|\.vault-token)(?:$|[/\s\"'])"
)
COMMAND_ALLOW_EXCEPTIONS_RE = re.compile(r"\.env\.(?:example|template|test)\b")
COMMAND_SOPS_DECRYPT_RE = re.compile(
    r"(?:^|[;&|]\s*|\s)(?:sops\b.*\s(?:-d|--decrypt|decrypt|exec-env|exec-file)\b|age\b.*\s(?:-d|--decrypt)\b|age-keygen\b|SOPS_AGE_KEY)"
)


def is_denied_path(raw_path: str, cwd: str) -> bool:
    expanded = os.path.expanduser(raw_path)
    candidate = Path(expanded)
    if not candidate.is_absolute() and cwd:
        candidate = Path(cwd) / candidate
    resolved = str(candidate.resolve())

    if any(fnmatch.fnmatch(resolved, pat) for pat in ALLOWED_PATH_EXCEPTIONS):
        return False
    return any(fnmatch.fnmatch(resolved, pat) for pat in DENIED_PATH_GLOBS)


def is_denied_command(command_line: str) -> str | None:
    if COMMAND_SOPS_DECRYPT_RE.search(command_line):
        return "SOPS/age decryption or key inspection command is blocked."
    try:
        tokens = shlex.split(command_line)
    except ValueError:
        tokens = command_line.split()

    for token in tokens:
        if COMMAND_ALLOW_EXCEPTIONS_RE.search(token):
            continue
        if COMMAND_SECRET_RE.search(token):
            return f"Command references a protected secret path or pattern: {token}"

    # Also catch unquoted shell redirections or unsplit patterns
    cleaned = COMMAND_ALLOW_EXCEPTIONS_RE.sub("", command_line)
    if COMMAND_SECRET_RE.search(cleaned):
        return "Command references a protected secret path or pattern."
    return None


def main() -> None:
    payload = json.load(sys.stdin)
    tool_call = payload.get("toolCall", {})
    tool_name = tool_call.get("name", "")
    args = tool_call.get("args", {})
    cwd = payload.get("cwd", "")

    if tool_name in FILE_TOOLS:
        raw_path = args.get("Path") or args.get("path") or args.get("TargetFile") or ""
        if raw_path and is_denied_path(raw_path, cwd):
            print(json.dumps({
                "decision": "deny",
                "reason": f"Blocked by secret-guard hook: {raw_path}",
            }))
            return

    if tool_name == "run_command":
        cmd = args.get("CommandLine") or args.get("command") or ""
        if cmd:
            reason = is_denied_command(cmd)
            if reason:
                print(json.dumps({
                    "decision": "deny",
                    "reason": f"Blocked by secret-guard hook: {reason}",
                }))
                return

    # "allow" delegates to the next hook or default settings.json policy
    print(json.dumps({"decision": "allow"}))


if __name__ == "__main__":
    main()
