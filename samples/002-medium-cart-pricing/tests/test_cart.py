import pytest

from cart import Cart


def test_add_and_quantity():
    cart = Cart()
    cart.add("TEA-001", 2)
    assert cart.quantity("TEA-001") == 2


def test_add_rejects_zero_quantity():
    cart = Cart()
    with pytest.raises(ValueError):
        cart.add("TEA-001", 0)


def test_add_unknown_sku_raises():
    cart = Cart()
    with pytest.raises(KeyError):
        cart.add("NOPE-999")


def test_remove():
    cart = Cart()
    cart.add("TEA-001", 2)
    cart.remove("TEA-001")
    assert cart.quantity("TEA-001") == 0


def test_subtotal_single_line():
    cart = Cart()
    cart.add("MUG-002", 2)
    assert cart.subtotal() == pytest.approx(25.00)


def test_line_items_are_sku_ordered():
    cart = Cart()
    cart.add("TIN-004")
    cart.add("MUG-002")
    assert [line[0] for line in cart.line_items()] == ["MUG-002", "TIN-004"]


def test_adding_the_same_sku_twice_accumulates():
    cart = Cart()
    cart.add("TEA-001", 2)
    cart.add("TEA-001", 3)
    assert cart.quantity("TEA-001") == 5


def test_customer_typed_sku_is_accepted():
    cart = Cart()
    cart.add(" tea-001 ", 1)
    assert cart.quantity("TEA-001") == 1


def test_mixed_case_and_canonical_are_the_same_line():
    cart = Cart()
    cart.add("TEA-001", 1)
    cart.add("tea-001", 1)
    assert len(cart.line_items()) == 1
    assert cart.quantity("TEA-001") == 2


def test_total_applies_volume_discount_at_the_boundary():
    # 5 tins at 5.00 plus 2 mugs at 12.50 = 50.00 exactly -> 5% off -> 47.50
    cart = Cart()
    cart.add("TIN-004", 5)
    cart.add("MUG-002", 2)
    assert cart.subtotal() == pytest.approx(50.00)
    assert cart.total() == pytest.approx(47.50)


def test_total_without_discount():
    cart = Cart()
    cart.add("MUG-002", 2)
    assert cart.total() == pytest.approx(25.00)
