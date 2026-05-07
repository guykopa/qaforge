from __future__ import annotations

from selenium import webdriver

from tests.e2e.pages.cart_page import CartPage


class TestPaymentScenarios:
    """E2E Selenium tests for payment-specific scenarios."""

    def test_successful_payment_shows_order_number(
        self, driver: webdriver.Chrome, base_url: str
    ) -> None:
        """A successful payment must display a non-empty order number."""
        driver.get(f"{base_url}/products")
        cart_page = CartPage(driver)
        cart_page.add_item(quantity=1)

        checkout_page = cart_page.proceed_to_checkout()
        checkout_page.fill_address(
            street="5 Avenue Montaigne",
            city="Paris",
            zip_code="75008",
        )
        checkout_page.fill_payment(card_number="4111111111111111")

        confirmation_page = checkout_page.confirm()
        order_number = confirmation_page.get_order_number()
        assert order_number is not None
        assert len(order_number) > 0

    def test_expired_card_shows_error(
        self, driver: webdriver.Chrome, base_url: str
    ) -> None:
        """An expired card must result in an error on the confirmation page."""
        driver.get(f"{base_url}/products")
        cart_page = CartPage(driver)
        cart_page.add_item(quantity=1)

        checkout_page = cart_page.proceed_to_checkout()
        checkout_page.fill_address(
            street="3 Place Bellecour",
            city="Lyon",
            zip_code="69002",
        )
        checkout_page.fill_payment(card_number="4000000000000069")

        confirmation_page = checkout_page.confirm()
        assert confirmation_page.is_error()
