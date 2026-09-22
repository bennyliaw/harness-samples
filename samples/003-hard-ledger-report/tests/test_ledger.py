from datetime import date

import pytest

import ledger

SIMPLE = """2026-01-15 | Coffee beans | -24.50
2026-01-31 | Salary | 4200.00"""

MESSY = """# January
2026-01-15 | Coffee beans | -24.50

2026-01-31 | Salary | 4,200.00
   
# February
2026-02-02 | Rent | -1,850.00
2026-02-14 | Refund | +12.00
"""


def test_parse_line_basic():
    entry = ledger.parse_line("2026-01-15 | Coffee beans | -24.50")
    assert entry.on == date(2026, 1, 15)
    assert entry.description == "Coffee beans"
    assert entry.amount == pytest.approx(-24.50)


def test_parse_line_tolerates_loose_spacing():
    entry = ledger.parse_line("  2026-01-15|Coffee beans|  -24.50  ")
    assert entry.description == "Coffee beans"
    assert entry.amount == pytest.approx(-24.50)


def test_parse_line_rejects_missing_field():
    with pytest.raises(ValueError):
        ledger.parse_line("2026-01-15 | -24.50")


def test_parse_line_rejects_empty_description():
    with pytest.raises(ValueError):
        ledger.parse_line("2026-01-15 |  | -24.50")


def test_parse_simple_ledger():
    assert len(ledger.parse(SIMPLE)) == 2


def test_balance():
    assert ledger.balance(ledger.parse(SIMPLE)) == pytest.approx(4175.50)


def test_balance_of_empty_ledger():
    assert ledger.balance([]) == pytest.approx(0.0)


def test_parse_line_accepts_thousands_separators():
    assert ledger.parse_line("2026-01-31 | Salary | 4,200.00").amount == pytest.approx(4200.00)


def test_parse_line_accepts_explicit_plus():
    assert ledger.parse_line("2026-02-14 | Refund | +12.00").amount == pytest.approx(12.00)


def test_parse_skips_blank_and_comment_lines():
    entries = ledger.parse(MESSY)
    assert len(entries) == 4
    assert [e.description for e in entries] == ["Coffee beans", "Salary", "Rent", "Refund"]


def test_parse_of_messy_ledger_balances():
    assert ledger.balance(ledger.parse(MESSY)) == pytest.approx(2337.50)


def test_parse_of_empty_text():
    assert ledger.parse("") == []
