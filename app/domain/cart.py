from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from decimal import ROUND_HALF_UP, Decimal


class OutOfStockError(Exception):
    """Raised when adding an item with stock == 0."""


class ItemNotFoundError(Exception):
    """Raised when removing an item that is not in the cart."""


class DiscountError(Exception):
    """Raised when an invalid or already-applied discount code is used."""


DISCOUNT_CODES: dict[str, Decimal] = {
    "SAVE10": Decimal("0.10"),
    "SAVE20": Decimal("0.20"),
}


@dataclass
class Item:
    """A product that can be added to a cart.

    Attributes:
        id: Unique identifier.
        name: Display name.
        price: Unit price in euros.
        stock: Available quantity.
    """

    id: str
    name: str
    price: float
    stock: int


@dataclass
class Cart:
    """Shopping cart holding items and an optional discount.

    Attributes:
        id: Unique cart identifier.
        items: Ordered list of items currently in the cart.
        discount_code: Applied discount code, or None.
    """

    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    items: list[Item] = field(default_factory=list)
    discount_code: str | None = None

    def add_item(self, item: Item) -> None:
        """Add an item to the cart.

        Args:
            item: The item to add.

        Raises:
            OutOfStockError: If item.stock == 0.
        """
        if item.stock == 0:
            raise OutOfStockError(f"Item '{item.name}' is out of stock.")
        self.items.append(item)

    def remove_item(self, item_id: str) -> None:
        """Remove the first occurrence of an item by id.

        Args:
            item_id: The id of the item to remove.

        Raises:
            ItemNotFoundError: If no item with that id exists in the cart.
        """
        for i, item in enumerate(self.items):
            if item.id == item_id:
                self.items.pop(i)
                return
        raise ItemNotFoundError(f"Item '{item_id}' not found in cart.")

    def apply_discount(self, code: str) -> None:
        """Apply a discount code to the cart.

        Args:
            code: The discount code string.

        Raises:
            DiscountError: If the code is invalid or already applied.
        """
        if code not in DISCOUNT_CODES:
            raise DiscountError(f"Invalid discount code: '{code}'.")
        if self.discount_code is not None:
            raise DiscountError("A discount code has already been applied.")
        self.discount_code = code

    def total(self) -> float:
        """Return the cart total after any discount, rounded to 2 decimal places.

        Returns:
            Total price as a float.
        """
        raw = sum((Decimal(str(item.price)) for item in self.items), Decimal("0"))
        if self.discount_code and self.discount_code in DISCOUNT_CODES:
            rate = DISCOUNT_CODES[self.discount_code]
            raw = raw * (Decimal("1") - rate)
        return float(raw.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP))

    def is_empty(self) -> bool:
        """Return True if the cart contains no items.

        Returns:
            True when items list is empty.
        """
        return len(self.items) == 0
