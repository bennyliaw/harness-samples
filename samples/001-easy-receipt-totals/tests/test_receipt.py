import pytest

from receipt import (
    add_tax,
    apply_discount,
    grand_total,
    line_total,
    round_money,
    subtotal,
)

BASKET = [
    {"name": "tea", "qty": 3, "unit_price": 3.33},
    {"name": "mug", "qty": 1, "unit_price": 12.50},
]


def test_line_total():
    assert line_total({"name": "tea", "qty": 3, "unit_price": 3.33}) == pytest.approx(9.99)


def test_line_total_zero_quantity():
    assert line_total({"name": "tea", "qty": 0, "unit_price": 3.33}) == pytest.approx(0.0)


def test_subtotal():
    assert subtotal(BASKET) == pytest.approx(22.49)


def test_subtotal_empty_basket():
    assert subtotal([]) == pytest.approx(0.0)


def test_add_tax():
    assert add_tax(100.0, 9) == pytest.approx(109.0)


def test_add_tax_zero_percent():
    assert add_tax(100.0, 0) == pytest.approx(100.0)


def test_apply_discount_takes_a_percentage():
    assert apply_discount(200.0, 10) == pytest.approx(180.0)


def test_apply_discount_zero_percent_changes_nothing():
    assert apply_discount(200.0, 0) == pytest.approx(200.0)


def test_apply_discount_full():
    assert apply_discount(200.0, 100) == pytest.approx(0.0)


def test_round_money_rounds_up_at_half():
    assert round_money(10.689) == pytest.approx(10.69)


def test_round_money_leaves_exact_cents_alone():
    assert round_money(10.25) == pytest.approx(10.25)


def test_grand_total_plain():
    assert grand_total(BASKET) == pytest.approx(22.49)


def test_grand_total_with_tax_is_rounded_not_truncated():
    # 9.99 + 7% = 10.6893 -> 10.69
    basket = [{"name": "tea", "qty": 3, "unit_price": 3.33}]
    assert grand_total(basket, tax_percent=7) == pytest.approx(10.69)


def test_grand_total_with_discount_and_tax():
    # 100.00 - 10% = 90.00, +9% tax = 98.10
    basket = [{"name": "kettle", "qty": 1, "unit_price": 100.00}]
    assert grand_total(basket, discount_percent=10, tax_percent=9) == pytest.approx(98.10)
