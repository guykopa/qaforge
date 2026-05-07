from __future__ import annotations

from selenium.webdriver.common.by import By

from tests.e2e.pages.base_page import BasePage


class ConfirmationPage(BasePage):
    """Page Object for the order confirmation page.

    Provides assertions about whether the purchase succeeded
    and exposes the generated order number.
    """

    SUCCESS_MSG = (By.ID, "order-success")
    ORDER_NUMBER = (By.ID, "order-number")
    ERROR_MSG = (By.ID, "order-error")

    def is_success(self) -> bool:
        """Return True if the success confirmation message is visible.

        Returns:
            True when the order completed successfully.
        """
        return self.is_visible(self.SUCCESS_MSG)

    def get_order_number(self) -> str | None:
        """Return the order number displayed on the confirmation page.

        Returns:
            The order number string, or None if the element is not present.
        """
        try:
            return self.get_text(self.ORDER_NUMBER)
        except Exception:
            return None

    def is_error(self) -> bool:
        """Return True if an error message is visible on the page.

        Returns:
            True when the order failed (e.g. payment declined).
        """
        return self.is_visible(self.ERROR_MSG)
