from __future__ import annotations

from selenium import webdriver

from tests.e2e.pages.cart_page import CartPage


class TestCartInteractions:
    """E2E Selenium tests for cart page interactions."""

    def test_add_item_updates_total(
        self, driver: webdriver.Chrome, base_url: str
    ) -> None:
        """Adding an item to the cart must display a non-zero total."""
        driver.get(f"{base_url}/products")
        cart_page = CartPage(driver)
        cart_page.add_item(quantity=1)
        assert cart_page.get_total() > 0

    def test_remove_item_empties_cart(
        self, driver: webdriver.Chrome, base_url: str
    ) -> None:
        """Removing the only item must show the empty-cart message."""
        driver.get(f"{base_url}/products")
        cart_page = CartPage(driver)
        cart_page.add_item(quantity=1)
        cart_page.remove_item()
        assert cart_page.is_empty()

    def test_discount_code_reduces_total(
        self, driver: webdriver.Chrome, base_url: str
    ) -> None:
        """Applying SAVE10 must lower the displayed total."""
        driver.get(f"{base_url}/products")
        cart_page = CartPage(driver)
        cart_page.add_item(quantity=1)
        total_before = cart_page.get_total()
        cart_page.apply_discount("SAVE10")
        assert cart_page.get_total() < total_before
