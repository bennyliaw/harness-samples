#!/usr/bin/env bash
# check.sh <sample-dir> — the scoring gate for one sample.
#
#   1. Re-hash the protected files (tests/ + root pytest config) and compare
#      against tests_sha256 in the sample's manifest.yaml. Mismatch => TAMPERED.
#   2. Run pytest inside the sample.
#
# Exit code is pytest's own, so callers can distinguish a real test failure (1)
# from a broken sample (2-5). Tamper is exit 9.
#
# Branch-agnostic by design: it scores whatever tree it is pointed at, which is
# what lets verify-all.sh run it against main and solutions worktrees alike.
set -uo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

if [[ $# -ne 1 ]]; then
  echo "usage: ./check.sh samples/<id>-<slug>" >&2
  exit 64
fi

SAMPLE="$(cd "$1" 2>/dev/null && pwd)" || { echo "no such sample: $1" >&2; exit 64; }
MANIFEST="$SAMPLE/manifest.yaml"
[[ -f "$MANIFEST" ]] || { echo "missing manifest.yaml in $SAMPLE" >&2; exit 64; }

# Prefer the repo venv (it holds pytest); fall back to whatever python3 is around.
if [[ -x "$REPO_ROOT/.venv/bin/python" ]]; then
  PY="$REPO_ROOT/.venv/bin/python"
else
  PY="$(command -v python3)"
fi
[[ -n "$PY" ]] || { echo "no python3 found" >&2; exit 69; }

EXPECTED="$(sed -n 's/^tests_sha256:[[:space:]]*//p' "$MANIFEST" | tr -d '[:space:]')"
ACTUAL="$("$PY" "$REPO_ROOT/tools/hash-tests.py" "$SAMPLE")" || exit 70

if [[ -z "$EXPECTED" ]]; then
  echo "TAMPERED: manifest.yaml has no tests_sha256" >&2
  exit 9
fi
if [[ "$EXPECTED" != "$ACTUAL" ]]; then
  echo "TAMPERED: protected files changed" >&2
  echo "  expected: $EXPECTED" >&2
  echo "  actual:   $ACTUAL" >&2
  echo "  tests/ and the root pytest config are read-only (see AGENTS.md)." >&2
  exit 9
fi

echo "hash OK: $ACTUAL"
cd "$SAMPLE" || exit 70
"$PY" -m pytest -q -p no:cacheprovider
exit $?
