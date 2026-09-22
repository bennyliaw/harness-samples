from datetime import date

import pytest

import ledger
import report

ENTRIES = [
    ledger.Entry(date(2025, 12, 20), "Gift", -80.00),
    ledger.Entry(date(2026, 1, 15), "Coffee beans", -24.50),
    ledger.Entry(date(2026, 1, 31), "Salary", 4200.00),
    ledger.Entry(date(2026, 2, 2), "Rent", -1850.00),
    ledger.Entry(date(2026, 2, 14), "Refund", 12.00),
]


def test_format_row():
    row = report.format_row(ENTRIES[1])
    assert row.startswith("2026-01-15")
    assert row.rstrip().endswith("-24.50")


def test_format_table_is_date_ordered():
    table = report.format_table(list(reversed(ENTRIES)))
    assert table.splitlines()[0].startswith("2025-12-20")


def test_format_table_has_a_row_per_entry():
    assert len(report.format_table(ENTRIES).splitlines()) == len(ENTRIES)


def test_monthly_summary_exists():
    assert callable(getattr(report, "monthly_summary", None)), (
        "report.monthly_summary is not implemented yet"
    )


def test_monthly_summary_nets_each_month():
    summary = report.monthly_summary(ENTRIES)
    assert summary["2026-01"] == pytest.approx(4175.50)
    assert summary["2026-02"] == pytest.approx(-1838.00)


def test_monthly_summary_keys_are_year_month():
    assert set(report.monthly_summary(ENTRIES)) == {"2025-12", "2026-01", "2026-02"}


def test_monthly_summary_is_chronologically_ordered_across_the_year_boundary():
    assert list(report.monthly_summary(ENTRIES)) == ["2025-12", "2026-01", "2026-02"]


def test_monthly_summary_of_empty_ledger():
    assert report.monthly_summary([]) == {}


def test_monthly_summary_rounds_to_cents():
    entries = [
        ledger.Entry(date(2026, 3, 1), "a", 0.1),
        ledger.Entry(date(2026, 3, 2), "b", 0.2),
    ]
    assert report.monthly_summary(entries)["2026-03"] == 0.3


def test_monthly_summary_accepts_unsorted_input():
    summary = report.monthly_summary(list(reversed(ENTRIES)))
    assert list(summary) == ["2025-12", "2026-01", "2026-02"]


def test_monthly_summary_handles_a_month_that_nets_to_zero():
    entries = [
        ledger.Entry(date(2026, 4, 1), "in", 100.00),
        ledger.Entry(date(2026, 4, 2), "out", -100.00),
    ]
    assert report.monthly_summary(entries) == {"2026-04": 0.0}


def test_end_to_end_summary_from_text():
    text = """# Q1
2026-01-31 | Salary | 4,200.00

2026-02-02 | Rent | -1,850.00
"""
    summary = report.monthly_summary(ledger.parse(text))
    assert summary == {"2026-01": 4200.00, "2026-02": -1850.00}
