from __future__ import annotations

import pytest

from app.domain.cart import Cart, DiscountError, Item, OutOfStockError


class TestCart:
    """Unit tests for the Cart domain model."""

    def test_add_item_increases_total(self, valid_item: Item) -> None:
        """Adding one item sets total to item price."""
        cart = Cart()
        cart.add_item(valid_item)
        assert cart.total() == valid_item.price

    def test_add_same_item_twice_doubles_total(self, valid_item: Item) -> None:
        """Adding the same item twice doubles the total."""
        cart = Cart()
        cart.add_item(valid_item)
        cart.add_item(valid_item)
        assert cart.total() == pytest.approx(valid_item.price * 2)

    def test_cannot_add_out_of_stock_item(self, out_of_stock_item: Item) -> None:
        """Adding an out-of-stock item raises OutOfStockError."""
        cart = Cart()
        with pytest.raises(OutOfStockError):
            cart.add_item(out_of_stock_item)

    def test_remove_item_decreases_total(
        self, valid_cart: Cart, valid_item: Item
    ) -> None:
        """Removing the only item resets total to zero."""
        valid_cart.remove_item(valid_item.id)
        assert valid_cart.total() == 0.0

    def test_apply_10_percent_discount(self, valid_cart: Cart) -> None:
        """SAVE10 reduces total by exactly 10%."""
        original = valid_cart.total()
        valid_cart.apply_discount("SAVE10")
        assert valid_cart.total() == pytest.approx(original * 0.9, rel=1e-2)

    def test_invalid_discount_code_raises(self, valid_cart: Cart) -> None:
        """An unknown discount code raises DiscountError."""
        with pytest.raises(DiscountError):
            valid_cart.apply_discount("INVALID")

    def test_empty_cart_total_is_zero(self) -> None:
        """A new cart has a total of 0.0."""
        assert Cart().total() == 0.0

    def test_is_empty_returns_true_on_new_cart(self) -> None:
        """is_empty() is True for a freshly created cart."""
        assert Cart().is_empty() is True
