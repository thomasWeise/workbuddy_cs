#!/usr/bin/env bash
# Replace the clangd --check invocation in clangd_mcp/server.py with the
# attached-value form required by clangd 22. No-ops if the file or the
# original line is absent. If the file is not writable, owner write
# permission is temporarily added and the original mode is restored.

echo "$(date +'%0Y-%0m-%0d %0R:%0S'): Welcome to the clangd MCP server fixer script."

TARGET="/home/user/venv/lib/python3.14/site-packages/clangd_mcp/server.py"
OLD='cmd = [clangd, "--check", file_path]'

[ -f "$TARGET" ] || exit 0
grep -qF -- "$OLD" "$TARGET" || exit 0

PERMS_CHANGED=0
ORIG_MODE=""

restore_perms() {
  if [ "$PERMS_CHANGED" -eq 1 ]; then
    chmod "$ORIG_MODE" "$TARGET" 2>/dev/null || true
  fi
}
trap restore_perms EXIT

if [ ! -w "$TARGET" ]; then
  ORIG_MODE=$(stat -c '%a' "$TARGET")
  chmod u+w "$TARGET"
  PERMS_CHANGED=1
fi

sed -i 's|cmd = \[clangd, "--check", file_path\]|cmd = [clangd, f"--check={file_path}"]|' "$TARGET"

echo "$(date +'%0Y-%0m-%0d %0R:%0S'): Done with the clangd MCP server fixer script."
