from __future__ import annotations

from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class BasePage:
    """Base class for all Page Objects.

    Provides common browser interaction methods with explicit waits.
    Never use time.sleep() — always rely on WebDriverWait.

    Attributes:
        driver: The Selenium WebDriver instance.
        wait: A WebDriverWait configured with a 10-second timeout.
    """

    def __init__(self, driver: webdriver.Chrome) -> None:
        """Initialise the page with a driver and default wait.

        Args:
            driver: An active Chrome WebDriver instance.
        """
        self.driver = driver
        self.wait = WebDriverWait(driver, timeout=10)

    def find(self, locator: tuple) -> WebElement:
        """Wait for an element to be present and return it.

        Args:
            locator: A (By, value) tuple identifying the element.

        Returns:
            The located WebElement.
        """
        return self.wait.until(EC.presence_of_element_located(locator))

    def click(self, locator: tuple) -> None:
        """Wait for an element to be clickable, then click it.

        Args:
            locator: A (By, value) tuple identifying the element.
        """
        self.wait.until(EC.element_to_be_clickable(locator)).click()

    def type_text(self, locator: tuple, text: str) -> None:
        """Clear a field and type text into it.

        Args:
            locator: A (By, value) tuple identifying the input field.
            text: The text to enter.
        """
        element = self.find(locator)
        element.clear()
        element.send_keys(text)

    def get_text(self, locator: tuple) -> str:
        """Return the visible text of an element.

        Args:
            locator: A (By, value) tuple identifying the element.

        Returns:
            The element's text content.
        """
        return self.find(locator).text

    def is_visible(self, locator: tuple) -> bool:
        """Check whether an element is visible without raising an exception.

        Args:
            locator: A (By, value) tuple identifying the element.

        Returns:
            True if visible, False if not found within the timeout.
        """
        try:
            return self.find(locator).is_displayed()
        except TimeoutException:
            return False
