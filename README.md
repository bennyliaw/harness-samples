# harness-samples

Small Python repos with failing `pytest` suites, for smoke-testing coding-agent
harnesses on identical inputs.

The point is comparison. Strands, Claude Code, Aider, a local model behind
Ollama — each one gets the same three tasks, the same tests, and the same
binary scoring gate, so what you learn is about the harness rather than about
whichever task you happened to hand it that evening.

Public and MIT-licensed so the samples can be used as shared inputs by anyone
doing the same thing.

## Try it

```bash
git clone https://github.com/bennyliaw/harness-samples
cd harness-samples
python3 -m venv .venv && ./.venv/bin/pip install pytest

./check.sh samples/001-easy-receipt-totals   # red, as shipped
```

Then point a harness at a sample directory, hand it that sample's `TASK.md`,
and run `check.sh` again. Green means the harness solved it.

## The samples

| id | difficulty | shape |
|---|---|---|
| `001-easy-receipt-totals` | easy | one file, two logic bugs in money arithmetic |
| `002-medium-cart-pricing` | medium | three modules, three interacting bugs — two surface in a module that is itself correct |
| `003-hard-ledger-report` | hard | a function that does not exist yet, plus parser edge cases in a second module |

Every sample is standard-library only. No dependency puzzles, no network: the
work is the code.

Each sample holds:

```
samples/<id>-<slug>/
  TASK.md         the prompt you hand the agent
  manifest.yaml   id, difficulty, success command, protected-file hash
  conftest.py     puts src/ on sys.path — protected, not to be edited
  src/            the code under test; this is what the agent changes
  tests/          the specification; read-only
```

`AGENTS.md` at the repo root states the rules every sample shares, and is meant
to be readable by the agent under test.

## Scoring

```bash
./check.sh samples/002-medium-cart-pricing
```

`check.sh` does two things: it re-hashes the protected files and compares them
with `tests_sha256` in the manifest, then runs `pytest`. Exit code is pytest's
own, except `9`, which means the protected files moved.

Protected means everything under `tests/` plus any pytest configuration at the
sample root (`conftest.py`, `pytest.ini`, `pyproject.toml`, `setup.cfg`,
`tox.ini`) — an agent that can add `addopts` or a root `conftest.py` can make
pytest green without fixing anything.

**This is a tripwire, not a sandbox.** `manifest.yaml` is a file in the repo
like any other, and an agent determined to cheat can edit the recorded hash
too. That is not worth defending against: a harness that does it has simply
produced no signal, which you will see in the diff.

## Reference solutions

They live on the **`solutions` branch**, which is `main` plus changes under
`src/` — nothing else differs. They are not on `main`, because an agent that
runs `ls` or `grep -r` would find them by accident.

The branch is public and therefore fetchable. For a smoke test you are driving
yourself that is acceptable; for a graded benchmark it would not be.

To check the suite itself is still sound:

```bash
./verify-all.sh
```

That is the maintainer gate, not something to run against an agent. It
materialises `solutions` as a temporary git worktree and asserts, per sample,
that pytest exits **exactly 1** on `main` and **exactly 0** on `solutions`.
Exactly 1 is the point: exit 5 means no tests were collected and 2–4 mean a
collection or internal error, so a sample that is merely *broken* would
otherwise read as "failing as shipped" and would fail every harness for free.

## Adding a sample

1. `mkdir -p samples/<NNN>-<difficulty>-<slug>/{src,tests}` and copy any
   existing `conftest.py` — it just puts `src/` on `sys.path`.
2. Write `src/` in its working form first, and `tests/` against it. Get it
   green. It is much easier to introduce a bug into working code than to write
   tests against code you have not run.
3. Write `TASK.md`: what the agent is being asked for, in the voice of someone
   handing over a small job. State the contract; do not name the bug.
4. Commit that working state **on `solutions`**.
5. Back on `main`, break it — or, for a feature sample, delete the function.
   Leave the docstrings describing the intended behaviour: they are the spec,
   and removing them turns the task into mind-reading.
6. Keep some tests green. An all-red suite gives the agent no anchor and is a
   poor imitation of a real repo.
7. Make failures *assertion* failures. A `SyntaxError` in `src/`, or a
   `from src.mod import thing_that_does_not_exist` at the top of a test module,
   errors the whole module at collection — pytest then exits 2, not 1, and
   `verify-all.sh` will reject it. For a missing function, import the module
   and reach for the attribute inside the test body.
8. Write `manifest.yaml`, then:
   `./.venv/bin/python tools/hash-tests.py --update samples/<your-sample>`
9. `./verify-all.sh` and confirm the 1/0 pair.

Keeping the branches in step: `solutions` is only ever `main` plus `src/`
changes. After anything lands on `main` — a new sample, a reworded `TASK.md`,
an edited test — do `git checkout solutions && git merge main`, re-run
`tools/hash-tests.py --update` if a test moved, and re-run `verify-all.sh`.

## Licence

MIT. See `LICENSE`.
