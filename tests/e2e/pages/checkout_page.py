from __future__ import annotations

from selenium.webdriver.common.by import By

from tests.e2e.pages.base_page import BasePage


class CheckoutPage(BasePage):
    """Page Object for the checkout page.

    Covers address entry, payment form, and order confirmation trigger.
    """

    STREET_INPUT = (By.ID, "street")
    CITY_INPUT = (By.ID, "city")
    ZIP_INPUT = (By.ID, "zip-code")
    CARD_INPUT = (By.ID, "card-number")
    CONFIRM_BTN = (By.ID, "confirm-order")
    GUEST_OPTION = (By.ID, "guest-checkout")

    def fill_address(self, street: str, city: str, zip_code: str) -> None:
        """Fill in the delivery address fields.

        Args:
            street: Street address line.
            city: City name.
            zip_code: Postal code.
        """
        self.type_text(self.STREET_INPUT, street)
        self.type_text(self.CITY_INPUT, city)
        self.type_text(self.ZIP_INPUT, zip_code)

    def fill_payment(self, card_number: str) -> None:
        """Enter the payment card number.

        Args:
            card_number: Full 16-digit card number string.
        """
        self.type_text(self.CARD_INPUT, card_number)

    def confirm(self) -> "ConfirmationPage":  # noqa: F821
        """Click the confirm button and return the ConfirmationPage.

        Returns:
            A ConfirmationPage instance bound to the same driver.
        """
        from tests.e2e.pages.confirmation_page import ConfirmationPage

        self.click(self.CONFIRM_BTN)
        return ConfirmationPage(self.driver)

    def is_guest_option_visible(self) -> bool:
        """Check whether the guest checkout option is displayed.

        Returns:
            True if the guest checkout element is visible.
        """
        return self.is_visible(self.GUEST_OPTION)
