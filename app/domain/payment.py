from __future__ import annotations

import uuid
from dataclasses import dataclass
from enum import Enum

from app.domain.order import Order, OrderStatus


class PaymentError(Exception):
    """Raised when a payment operation is invalid."""


class PaymentStatus(str, Enum):
    """Possible states of a payment."""

    SUCCESS = "SUCCESS"
    DECLINED = "DECLINED"
    REFUNDED = "REFUNDED"


# Test card numbers and their forced outcomes
_DECLINED_CARDS: frozenset[str] = frozenset(
    ["4000000000000002", "4000000000000069"]
)


@dataclass
class Payment:
    """A payment transaction linked to an order.

    Attributes:
        id: Unique payment identifier.
        order_id: Id of the order being paid.
        amount: Amount charged in euros.
        status: Current payment status.
        card_last4: Last 4 digits of the card used.
    """

    id: str
    order_id: str
    amount: float
    status: PaymentStatus
    card_last4: str

    @classmethod
    def process(cls, order: Order, card_number: str) -> "Payment":
        """Process a payment for a confirmed or pending order.

        Args:
            order: The order to pay for.
            card_number: Full card number string.

        Returns:
            A Payment with status SUCCESS or DECLINED.

        Raises:
            PaymentError: If the order is already cancelled.
        """
        if order.status == OrderStatus.CANCELLED:
            raise PaymentError("Cannot pay for a cancelled order.")

        card_last4 = card_number[-4:]
        if card_number in _DECLINED_CARDS:
            status = PaymentStatus.DECLINED
        else:
            status = PaymentStatus.SUCCESS
            order.confirm()

        return cls(
            id=str(uuid.uuid4()),
            order_id=order.id,
            amount=order.total,
            status=status,
            card_last4=card_last4,
        )

    def refund(self) -> None:
        """Refund a successful payment.

        Raises:
            PaymentError: If the payment was not successful.
        """
        if self.status != PaymentStatus.SUCCESS:
            raise PaymentError(
                f"Cannot refund a payment with status '{self.status}'."
            )
        self.status = PaymentStatus.REFUNDED
