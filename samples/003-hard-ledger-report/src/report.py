"""Human-readable rendering of a parsed ledger."""


def format_row(entry):
    """One fixed-width row: date, description padded to 24, amount to cents."""
    return f"{entry.on.isoformat()}  {entry.description:<24}  {entry.amount:>10.2f}"


def format_table(entries):
    """Every entry as a row, in date order, newline-joined."""
    return "\n".join(format_row(entry) for entry in sorted(entries, key=lambda e: e.on))
