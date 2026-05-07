from __future__ import annotations

from selenium import webdriver

from tests.e2e.pages.cart_page import CartPage


class TestCheckoutFlow:
    """E2E Selenium tests for the complete checkout user journey."""

    def test_complete_purchase_journey(
        self, driver: webdriver.Chrome, base_url: str
    ) -> None:
        """Happy path: add item → fill address → pay → confirm order."""
        driver.get(f"{base_url}/products")
        cart_page = CartPage(driver)
        cart_page.add_item(quantity=1)

        checkout_page = cart_page.proceed_to_checkout()
        checkout_page.fill_address(
            street="1 Rue de Rivoli",
            city="Paris",
            zip_code="75001",
        )
        checkout_page.fill_payment(card_number="4111111111111111")

        confirmation_page = checkout_page.confirm()
        assert confirmation_page.is_success()
        assert confirmation_page.get_order_number() is not None

    def test_guest_checkout_option_is_visible(
        self, driver: webdriver.Chrome, base_url: str
    ) -> None:
        """Guest checkout option must be shown on the checkout page."""
        driver.get(f"{base_url}/products")
        cart_page = CartPage(driver)
        cart_page.add_item(quantity=1)
        checkout_page = cart_page.proceed_to_checkout()
        assert checkout_page.is_guest_option_visible()

    def test_declined_card_shows_error(
        self, driver: webdriver.Chrome, base_url: str
    ) -> None:
        """A declined card must show an error on the confirmation page."""
        driver.get(f"{base_url}/products")
        cart_page = CartPage(driver)
        cart_page.add_item(quantity=1)

        checkout_page = cart_page.proceed_to_checkout()
        checkout_page.fill_address(
            street="10 Rue du Commerce",
            city="Lyon",
            zip_code="69002",
        )
        checkout_page.fill_payment(card_number="4000000000000002")

        confirmation_page = checkout_page.confirm()
        assert confirmation_page.is_error()
