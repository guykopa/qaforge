from __future__ import annotations

import pytest

from app.domain.cart import Cart
from app.domain.order import Order, OrderError, OrderStatus


class TestOrder:
    """Unit tests for the Order domain model."""

    def test_create_order_from_valid_cart(self, valid_cart: Cart) -> None:
        """An order created from a non-empty cart has PENDING status."""
        order = Order.from_cart(valid_cart)
        assert order.status == OrderStatus.PENDING

    def test_order_total_matches_cart_total(self, valid_cart: Cart) -> None:
        """The order total equals the cart total at creation time."""
        order = Order.from_cart(valid_cart)
        assert order.total == valid_cart.total()

    def test_cannot_create_order_from_empty_cart(self, empty_cart: Cart) -> None:
        """Creating an order from an empty cart raises OrderError."""
        with pytest.raises(OrderError):
            Order.from_cart(empty_cart)

    def test_confirm_changes_status_to_confirmed(self, valid_cart: Cart) -> None:
        """confirm() transitions a PENDING order to CONFIRMED."""
        order = Order.from_cart(valid_cart)
        order.confirm()
        assert order.status == OrderStatus.CONFIRMED

    def test_cancel_changes_status_to_cancelled(self, valid_cart: Cart) -> None:
        """cancel() transitions a PENDING order to CANCELLED."""
        order = Order.from_cart(valid_cart)
        order.cancel()
        assert order.status == OrderStatus.CANCELLED

    def test_cancel_already_cancelled_order_raises(self, valid_cart: Cart) -> None:
        """Cancelling an already-cancelled order raises OrderError."""
        order = Order.from_cart(valid_cart)
        order.cancel()
        with pytest.raises(OrderError):
            order.cancel()
