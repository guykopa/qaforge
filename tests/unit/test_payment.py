from __future__ import annotations

import pytest

from app.domain.cart import Cart
from app.domain.order import Order, OrderStatus
from app.domain.payment import Payment, PaymentError, PaymentStatus


class TestPayment:
    """Unit tests for the Payment domain model."""

    def test_valid_card_produces_success_status(
        self, valid_cart: Cart, valid_card: str
    ) -> None:
        """A valid card produces a SUCCESS payment."""
        order = Order.from_cart(valid_cart)
        payment = Payment.process(order, valid_card)
        assert payment.status == PaymentStatus.SUCCESS

    def test_declined_card_produces_declined_status(
        self, valid_cart: Cart, declined_card: str
    ) -> None:
        """A declined card produces a DECLINED payment."""
        order = Order.from_cart(valid_cart)
        payment = Payment.process(order, declined_card)
        assert payment.status == PaymentStatus.DECLINED

    def test_successful_payment_confirms_order(
        self, valid_cart: Cart, valid_card: str
    ) -> None:
        """A successful payment transitions the order to CONFIRMED."""
        order = Order.from_cart(valid_cart)
        Payment.process(order, valid_card)
        assert order.status == OrderStatus.CONFIRMED

    def test_refund_changes_status_to_refunded(
        self, valid_cart: Cart, valid_card: str
    ) -> None:
        """Refunding a successful payment sets status to REFUNDED."""
        order = Order.from_cart(valid_cart)
        payment = Payment.process(order, valid_card)
        payment.refund()
        assert payment.status == PaymentStatus.REFUNDED

    def test_cannot_pay_cancelled_order(
        self, valid_cart: Cart, valid_card: str
    ) -> None:
        """Processing payment on a cancelled order raises PaymentError."""
        order = Order.from_cart(valid_cart)
        order.cancel()
        with pytest.raises(PaymentError):
            Payment.process(order, valid_card)
