from __future__ import annotations

from selenium.webdriver.common.by import By

from tests.e2e.pages.base_page import BasePage


class CartPage(BasePage):
    """Page Object for the shopping cart page.

    Encapsulates all selectors and interactions for the cart UI.
    All selectors are defined as class-level constants — never hardcoded
    in test files.
    """

    ADD_TO_CART_BTN = (By.ID, "add-to-cart")
    REMOVE_ITEM_BTN = (By.CLASS_NAME, "remove-item")
    QUANTITY_INPUT = (By.NAME, "quantity")
    CART_TOTAL = (By.ID, "cart-total")
    DISCOUNT_INPUT = (By.ID, "discount-code")
    APPLY_DISCOUNT_BTN = (By.ID, "apply-discount")
    CHECKOUT_BTN = (By.ID, "proceed-to-checkout")
    EMPTY_CART_MSG = (By.ID, "empty-cart-message")

    def add_item(self, quantity: int = 1) -> None:
        """Set quantity and click the add-to-cart button.

        Args:
            quantity: Number of units to add (default 1).
        """
        self.type_text(self.QUANTITY_INPUT, str(quantity))
        self.click(self.ADD_TO_CART_BTN)

    def remove_item(self) -> None:
        """Click the remove button for the first item in the cart."""
        self.click(self.REMOVE_ITEM_BTN)

    def apply_discount(self, code: str) -> None:
        """Type a discount code and submit it.

        Args:
            code: The discount code string to apply.
        """
        self.type_text(self.DISCOUNT_INPUT, code)
        self.click(self.APPLY_DISCOUNT_BTN)

    def get_total(self) -> float:
        """Read and parse the cart total displayed on screen.

        Returns:
            The cart total as a float (euro symbol stripped).
        """
        text = self.get_text(self.CART_TOTAL)
        return float(text.replace("€", "").strip())

    def proceed_to_checkout(self) -> "CheckoutPage":  # noqa: F821
        """Click the checkout button and return the CheckoutPage.

        Returns:
            A CheckoutPage instance bound to the same driver.
        """
        from tests.e2e.pages.checkout_page import CheckoutPage

        self.click(self.CHECKOUT_BTN)
        return CheckoutPage(self.driver)

    def is_empty(self) -> bool:
        """Return True if the empty-cart message is visible.

        Returns:
            True when no items remain in the cart.
        """
        return self.is_visible(self.EMPTY_CART_MSG)
