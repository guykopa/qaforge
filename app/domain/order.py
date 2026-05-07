from __future__ import annotations

import uuid
from dataclasses import dataclass
from datetime import datetime, timezone
from enum import Enum

from app.domain.cart import Cart


class OrderError(Exception):
    """Raised when an order operation is invalid."""


class OrderStatus(str, Enum):
    """Possible states of an order."""

    PENDING = "PENDING"
    CONFIRMED = "CONFIRMED"
    CANCELLED = "CANCELLED"


@dataclass
class Order:
    """A purchase order created from a cart.

    Attributes:
        id: Unique order identifier.
        cart_id: Id of the cart this order was created from.
        status: Current order status.
        total: Order total in euros.
        created_at: UTC timestamp of creation.
    """

    id: str
    cart_id: str
    status: OrderStatus
    total: float
    created_at: datetime

    @classmethod
    def from_cart(cls, cart: Cart) -> "Order":
        """Create a new PENDING order from a cart.

        Args:
            cart: The cart to order from.

        Returns:
            A new Order with status PENDING.

        Raises:
            OrderError: If the cart is empty.
        """
        if cart.is_empty():
            raise OrderError("Cannot create an order from an empty cart.")
        return cls(
            id=str(uuid.uuid4()),
            cart_id=cart.id,
            status=OrderStatus.PENDING,
            total=cart.total(),
            created_at=datetime.now(tz=timezone.utc),
        )

    def confirm(self) -> None:
        """Confirm the order.

        Raises:
            OrderError: If the order is not in PENDING status.
        """
        if self.status != OrderStatus.PENDING:
            raise OrderError(
                f"Cannot confirm an order with status '{self.status}'."
            )
        self.status = OrderStatus.CONFIRMED

    def cancel(self) -> None:
        """Cancel the order.

        Raises:
            OrderError: If the order is already CANCELLED.
        """
        if self.status == OrderStatus.CANCELLED:
            raise OrderError("Order is already cancelled.")
        self.status = OrderStatus.CANCELLED
