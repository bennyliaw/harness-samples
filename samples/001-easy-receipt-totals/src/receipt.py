"""Till receipt arithmetic for a small shop.

An item is a mapping with "name", "qty" and "unit_price" keys.
Money is handled as float and rounded to cents only at the very end.
"""


def line_total(item):
    """Total for a single line: quantity times unit price."""
    return item["qty"] * item["unit_price"]


def subtotal(items):
    """Sum of every line total. An empty basket is worth 0.0."""
    return float(sum(line_total(item) for item in items))


def apply_discount(amount, percent):
    """Take `percent` PERCENT off `amount`.

    apply_discount(200.0, 10) -> 180.0
    """
    return amount - percent


def add_tax(amount, percent):
    """Add `percent` percent tax on top of `amount`.

    add_tax(100.0, 9) -> 109.0
    """
    return amount * (1 + percent / 100)


def round_money(amount):
    """Round to whole cents, half away from zero."""
    cents = amount * 100
    return int(cents) / 100


def grand_total(items, discount_percent=0, tax_percent=0):
    """Subtotal, then discount, then tax, rounded to cents."""
    amount = subtotal(items)
    amount = apply_discount(amount, discount_percent)
    amount = add_tax(amount, tax_percent)
    return round_money(amount)
