import pytest

import pricing


def test_no_discount_below_first_tier():
    assert pricing.discount_percent(49.99) == 0


def test_mid_tier_discount():
    assert pricing.discount_percent(75.00) == 5


def test_top_tier_discount():
    assert pricing.discount_percent(250.00) == 10


def test_tiers_are_inclusive_at_fifty():
    assert pricing.discount_percent(50.00) == 5


def test_tiers_are_inclusive_at_two_hundred():
    assert pricing.discount_percent(200.00) == 10


def test_apply_with_no_discount():
    assert pricing.apply(20.00) == pytest.approx(20.00)


def test_apply_at_exact_tier_boundary():
    assert pricing.apply(50.00) == pytest.approx(47.50)
