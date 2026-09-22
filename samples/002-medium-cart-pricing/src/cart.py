"""A shopping cart, keyed by canonical SKU."""

import catalog
import pricing


class Cart:
    def __init__(self):
        self._items = {}

    def add(self, sku, qty=1):
        """Add `qty` of `sku` to the cart.

        Adding a SKU that is already in the cart increases its quantity;
        it does not replace it. Raises KeyError for an unknown SKU.
        """
        if qty <= 0:
            raise ValueError("qty must be positive")
        catalog.unit_price(sku)  # validate before mutating
        key = catalog.normalise_sku(sku)
        self._items[key] = self._items.get(key, 0) + qty

    def remove(self, sku):
        """Remove a SKU from the cart entirely. Unknown SKUs are ignored."""
        self._items.pop(catalog.normalise_sku(sku), None)

    def quantity(self, sku):
        """Quantity of `sku` currently in the cart (0 if absent)."""
        return self._items.get(catalog.normalise_sku(sku), 0)

    def line_items(self):
        """(sku, qty, unit_price, line_total) for each line, SKU order."""
        lines = []
        for sku in sorted(self._items):
            qty = self._items[sku]
            price = catalog.unit_price(sku)
            lines.append((sku, qty, price, round(qty * price, 2)))
        return lines

    def subtotal(self):
        """Sum of every line total, before any discount."""
        return round(sum(line[3] for line in self.line_items()), 2)

    def total(self):
        """Subtotal with the volume discount applied."""
        return pricing.apply(self.subtotal())
