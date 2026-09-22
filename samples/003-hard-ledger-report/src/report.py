"""Human-readable rendering of a parsed ledger."""


def format_row(entry):
    """One fixed-width row: date, description padded to 24, amount to cents."""
    return f"{entry.on.isoformat()}  {entry.description:<24}  {entry.amount:>10.2f}"


def format_table(entries):
    """Every entry as a row, in date order, newline-joined."""
    return "\n".join(format_row(entry) for entry in sorted(entries, key=lambda e: e.on))


def monthly_summary(entries):
    """Net amount per calendar month, chronologically ordered.

    Keys are "YYYY-MM"; values are rounded to cents. Input order does not
    matter. An empty ledger summarises to an empty dict.
    """
    months = {}
    for entry in entries:
        key = f"{entry.on.year:04d}-{entry.on.month:02d}"
        months[key] = months.get(key, 0.0) + entry.amount
    return {key: round(months[key], 2) for key in sorted(months)}
