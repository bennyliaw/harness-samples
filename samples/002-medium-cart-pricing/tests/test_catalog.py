import pytest

import catalog


def test_lookup_canonical_sku():
    assert catalog.lookup("TEA-001")["name"] == "Assam loose leaf, 100g"


def test_lookup_unknown_sku_returns_none():
    assert catalog.lookup("NOPE-999") is None


def test_unit_price_canonical_sku():
    assert catalog.unit_price("MUG-002") == pytest.approx(12.50)


def test_unit_price_unknown_sku_raises():
    with pytest.raises(KeyError):
        catalog.unit_price("NOPE-999")


def test_normalise_sku_strips_whitespace():
    assert catalog.normalise_sku("  TEA-001  ") == "TEA-001"


def test_normalise_sku_upper_cases():
    assert catalog.normalise_sku("tea-001") == "TEA-001"


def test_lookup_is_case_insensitive():
    assert catalog.lookup(" mug-002 ")["name"] == "Stoneware mug"
