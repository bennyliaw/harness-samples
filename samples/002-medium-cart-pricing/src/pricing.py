"""Volume discount tiers.

The tiers are inclusive of their threshold: a basket worth exactly $50.00
already earns the 5% tier, and exactly $200.00 already earns the 10% tier.

    subtotal >= 200.00  ->  10%
    subtotal >=  50.00  ->   5%
    otherwise           ->   0%
"""

TIERS = (
    (200.00, 10),
    (50.00, 5),
)


def discount_percent(subtotal):
    """Return the volume discount percentage earned by `subtotal`."""
    for threshold, percent in TIERS:
        if subtotal > threshold:
            return percent
    return 0


def apply(subtotal):
    """Return `subtotal` with its volume discount applied, rounded to cents."""
    percent = discount_percent(subtotal)
    return round(subtotal * (1 - percent / 100), 2)
