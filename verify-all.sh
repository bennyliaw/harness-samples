#!/usr/bin/env bash
# verify-all.sh — the maintainer gate. NOT for agents under test.
#
# For every sample, asserts the pair that makes this suite meaningful:
#
#     main       -> pytest exits exactly 1   (fails as shipped)
#     solutions  -> pytest exits exactly 0   (passes with the reference fix)
#
# Exactly 1 matters. Exit 5 means pytest collected no tests, and 2/3/4 mean a
# collection or internal error — a sample that errors is BROKEN, not "failing
# as shipped", and would score any harness as a failure for free.
#
# The solutions tree is materialised as a throwaway git worktree, so your
# working copy is never checked out to another branch.
set -uo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SOLUTIONS_REF="${SOLUTIONS_REF:-solutions}"

cd "$REPO_ROOT" || exit 70

if ! git rev-parse --verify --quiet "$SOLUTIONS_REF" >/dev/null; then
  echo "error: ref '$SOLUTIONS_REF' does not exist" >&2
  exit 70
fi

WORKTREE="$(mktemp -d "${TMPDIR:-/tmp}/harness-solutions.XXXXXX")"
cleanup() { git worktree remove --force "$WORKTREE" >/dev/null 2>&1 || rm -rf "$WORKTREE"; }
trap cleanup EXIT

git worktree add --detach --quiet "$WORKTREE" "$SOLUTIONS_REF" || exit 70
# The worktree has no .venv of its own; point its check.sh at this one.
ln -s "$REPO_ROOT/.venv" "$WORKTREE/.venv" 2>/dev/null || true

fail=0
for sample_dir in "$REPO_ROOT"/samples/*/; do
  sample="$(basename "$sample_dir")"
  printf '\n=== %s ===\n' "$sample"

  "$REPO_ROOT/check.sh" "$sample_dir" >/dev/null 2>&1
  main_rc=$?
  "$WORKTREE/check.sh" "$WORKTREE/samples/$sample" >/dev/null 2>&1
  sol_rc=$?

  if [[ $main_rc -eq 1 ]]; then
    echo "  main      exit $main_rc  OK (fails as shipped)"
  else
    echo "  main      exit $main_rc  WRONG (want exactly 1; 5=no tests collected, 2-4=error, 9=tampered)"
    fail=1
  fi

  if [[ $sol_rc -eq 0 ]]; then
    echo "  solutions exit $sol_rc  OK (passes with reference fix)"
  else
    echo "  solutions exit $sol_rc  WRONG (want exactly 0)"
    fail=1
  fi
done

printf '\n'
if [[ $fail -eq 0 ]]; then
  echo "ALL SAMPLES VERIFIED: 1 on main, 0 on $SOLUTIONS_REF"
else
  echo "VERIFICATION FAILED"
fi
exit $fail
