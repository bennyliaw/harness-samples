# Rules for every sample in this suite

These rules apply to **all** samples. Each sample's `TASK.md` tells you what to
build; this file tells you how the game is scored.

## The contract

1. **Success = `pytest` passes.** Nothing else counts. Not "the code looks right",
   not "the tests are wrong" — a green pytest run on the sample's own tests.
2. **`tests/` is read-only.** Do not edit, delete, rename, move, skip, or `xfail`
   anything under `tests/`. Do not add new files there.
3. **The test harness config is read-only too**: `conftest.py`, `pytest.ini`,
   `pyproject.toml`, `setup.cfg` at the sample root. No `addopts`, no
   `collect_ignore`, no monkeypatching the runner.
4. **Fix the source, not the scoreboard.** All your changes belong in `src/`.
5. **Read the failures before you change anything.** The tests are the spec.
6. **Stay inside the sample directory.** Do not touch other samples, the repo
   root, or anything outside the repo.
7. **Standard library only.** No new dependencies, no network access. If your
   solution needs `pip install`, it is the wrong solution.

## How your work is checked

`check.sh <sample>` re-hashes the protected files and compares them against
`tests_sha256` in the sample's `manifest.yaml`. If the hash moved, the run is
recorded as **TAMPERED** and fails regardless of what pytest says.

This is a tripwire, not a sandbox. The manifest is a file in the repo and you
could edit that too. Doing so is not clever; it just means the sample produced
no signal about the harness under test, which is the entire reason this suite
exists.

## Expected end state

- `./check.sh samples/<id>-<slug>` exits 0.
- `git diff` touches only files under `samples/<id>-<slug>/src/`.
