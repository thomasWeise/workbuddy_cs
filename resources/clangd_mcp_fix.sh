#!/usr/bin/env bash
# Idempotent fix for the clangd-mcp 1.x `check_file` tool.
#
# Old code:  cmd = [clangd, "--check", file_path]
# Fixed code: cmd = [clangd, f"--check={file_path}"]
#
# clangd 22+ requires `--check=<file>`; a bare positional file is rejected.
# If the buggy line is not present (e.g. a newer clangd-mcp already contains
# a fix or uses different code), this script makes no changes and exits 0.
#
# Optional overrides:
#   PYTHON_BIN=/path/to/python          interpreter used to locate the package
#   CLANGD_MCP_SERVER_PY=/path/server.py  patch a specific file directly

set -euo pipefail

echo "$(date +'%0Y-%0m-%0d %0R:%0S'): Welcome to the cland-MCP fix file." &&\

PYTHON_BIN="${PYTHON_BIN:-/home/user/venv/bin/python}"
SERVER_PY="${CLANGD_MCP_SERVER_PY:-}"

if [[ -z "$SERVER_PY" ]]; then
    if [[ ! -x "$PYTHON_BIN" ]]; then
        echo "Python interpreter not found: $PYTHON_BIN" >&2
        exit 1
    fi
    SERVER_PY="$("$PYTHON_BIN" - <<'PY'
import importlib.util
import os
import sys

spec = importlib.util.find_spec("clangd_mcp")
if spec is None:
    sys.exit(0)
if spec.submodule_search_locations:
    package_dir = next(iter(spec.submodule_search_locations))
    root = os.path.dirname(package_dir.rstrip(os.sep))
else:
    root = os.path.dirname(spec.origin)
print(os.path.join(root, "server.py"))
PY
)"
fi

if [[ -z "$SERVER_PY" || ! -f "$SERVER_PY" ]]; then
    echo "clangd-mcp server.py not found; nothing to do."
    exit 0
fi

BUGGY='cmd = [clangd, "--check", file_path]'
FIXED='cmd = [clangd, f"--check={file_path}"]'

if ! grep -Fq -- "$BUGGY" "$SERVER_PY"; then
    if grep -Fq -- "$FIXED" "$SERVER_PY"; then
        echo "clangd-mcp already contains the fixed --check=<file> invocation; nothing to do."
    else
        echo "clangd-mcp code layout does not match the known buggy version; nothing to do."
    fi
    exit 0
fi

if [[ ! -x "$PYTHON_BIN" ]]; then
    echo "Python interpreter not found: $PYTHON_BIN" >&2
    exit 1
fi


"$PYTHON_BIN" - "$SERVER_PY" "$BUGGY" "$FIXED" <<'PY'
import os
import sys
import tempfile

path, old, new = sys.argv[1:4]
with open(path, encoding="utf-8") as fh:
    text = fh.read()

count = text.count(old)
if count != 1:
    raise SystemExit(
        f"Expected exactly one occurrence of the buggy line, found {count}; "
        f"leaving {path} unchanged."
    )

text = text.replace(old, new)
directory = os.path.dirname(os.path.abspath(path))
fd, tmp_path = tempfile.mkstemp(prefix=".clangd-mcp-fix-", dir=directory)
try:
    with os.fdopen(fd, "w", encoding="utf-8") as fh:
        fh.write(text)
    os.chmod(tmp_path, os.stat(path).st_mode)
    os.replace(tmp_path, path)
except BaseException:
    if os.path.exists(tmp_path):
        os.unlink(tmp_path)
    raise
PY

if ! grep -Fq -- "$FIXED" "$SERVER_PY" || grep -Fq -- "$BUGGY" "$SERVER_PY"; then
    echo "Patch verification failed for $SERVER_PY" >&2
    exit 1
fi

echo "Patched $SERVER_PY"

echo "$(date +'%0Y-%0m-%0d %0R:%0S'): Done with the cland-MCP fix." &&\
