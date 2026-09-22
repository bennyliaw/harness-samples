"""Parsing for a plain-text ledger.

One entry per line, pipe-separated:

    2026-01-15 | Coffee beans | -24.50

Amounts may be written with thousands separators ("1,250.00") and with a
leading "+". Blank lines and lines whose first non-space character is "#" are
comments and carry no entry.
"""

from dataclasses import dataclass
from datetime import date


@dataclass(frozen=True)
class Entry:
    on: date
    description: str
    amount: float


def parse_line(line):
    """Parse one ledger line into an Entry.

    Raises ValueError if the line is not a well-formed entry.
    """
    parts = [part.strip() for part in line.split("|")]
    if len(parts) != 3:
        raise ValueError(f"malformed ledger line: {line!r}")
    on_text, description, amount_text = parts
    if not description:
        raise ValueError(f"entry has no description: {line!r}")
    return Entry(
        on=date.fromisoformat(on_text),
        description=description,
        amount=float(amount_text.replace(",", "")),
    )


def parse(text):
    """Parse a whole ledger into a list of Entry, in file order.

    Blank lines and "#" comment lines are skipped.
    """
    entries = []
    for line in text.splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        entries.append(parse_line(line))
    return entries


def balance(entries):
    """Net of every entry amount, rounded to cents. Empty ledger is 0.0."""
    return round(sum(entry.amount for entry in entries), 2)
