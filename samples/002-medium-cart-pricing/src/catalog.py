"""The product catalogue.

SKUs are canonically UPPER-CASE with surrounding whitespace stripped, e.g.
"TEA-001". Customers type them in any case, so every entry point into this
module is expected to normalise first.
"""

PRODUCTS = {
    "TEA-001": {"name": "Assam loose leaf, 100g", "unit_price": 8.50},
    "MUG-002": {"name": "Stoneware mug", "unit_price": 12.50},
    "POT-003": {"name": "Cast iron teapot", "unit_price": 64.00},
    "TIN-004": {"name": "Storage tin", "unit_price": 5.00},
}


def normalise_sku(sku):
    """Return the canonical form of a customer-supplied SKU.

    Canonical form is upper-case with surrounding whitespace removed:
    normalise_sku("  tea-001 ") -> "TEA-001"
    """
    return sku.strip()


def lookup(sku):
    """Return the product record for `sku`, or None if there is no such SKU."""
    return PRODUCTS.get(normalise_sku(sku))


def unit_price(sku):
    """Return the unit price for `sku`. Raises KeyError for an unknown SKU."""
    product = lookup(sku)
    if product is None:
        raise KeyError(sku)
    return product["unit_price"]
