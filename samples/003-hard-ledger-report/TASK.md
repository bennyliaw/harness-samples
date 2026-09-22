# 003 — Ledger summary report

Two modules:

- `src/ledger.py` — parses a plain-text ledger into `Entry` records
- `src/report.py` — renders parsed entries for a human

There are two pieces of work here, and they meet in the last test.

**1. The parser does not yet handle real ledger files.** It copes with a clean
file, but the ones people actually keep have blank lines, `#` comment headings,
thousands separators in amounts, and an explicit `+` on credits. The module
docstring already says all four are supported; the code does not do it.

**2. `report.monthly_summary(entries)` does not exist. Write it.** It takes
entries and returns the net amount per calendar month:

    {"2025-12": -80.0, "2026-01": 4175.5, "2026-02": -1838.0}

Keys are `"YYYY-MM"`. The result is ordered chronologically, including across a
year boundary, regardless of what order the entries arrive in. Amounts are
rounded to cents. An empty ledger summarises to an empty dict.

**Your task:** make the test suite pass by changing files under `src/`.

See `AGENTS.md` at the repo root for the rules. In short: fix `src/`, never
`tests/`, standard library only.
