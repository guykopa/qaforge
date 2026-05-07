from __future__ import annotations

import pytest
from dotenv import load_dotenv
from fastapi.testclient import TestClient

from app.domain.cart import Cart, Item
from app.main import app, _carts, _orders, _payments

load_dotenv()


# ── Domain fixtures ───────────────────────────────────────────────────────────

@pytest.fixture()
def valid_item() -> Item:
    """A regular in-stock item."""
    return Item(id="item-001", name="Laptop", price=999.99, stock=10)


@pytest.fixture()
def out_of_stock_item() -> Item:
    """An item with zero stock."""
    return Item(id="item-002", name="Mouse", price=29.99, stock=0)


@pytest.fixture()
def valid_cart(valid_item: Item) -> Cart:
    """A cart pre-loaded with one valid item."""
    cart = Cart()
    cart.add_item(valid_item)
    return cart


@pytest.fixture()
def empty_cart() -> Cart:
    """A freshly created cart with no items."""
    return Cart()


@pytest.fixture()
def valid_discount_code() -> str:
    """A working 10% discount code."""
    return "SAVE10"


@pytest.fixture()
def invalid_discount_code() -> str:
    """A discount code that does not exist."""
    return "INVALID"


@pytest.fixture()
def valid_card() -> str:
    """Visa test card — always succeeds."""
    return "4111111111111111"


@pytest.fixture()
def declined_card() -> str:
    """Test card — always declined."""
    return "4000000000000002"


@pytest.fixture()
def expired_card() -> str:
    """Test card — always declined (expired)."""
    return "4000000000000069"


# ── API fixtures ──────────────────────────────────────────────────────────────

@pytest.fixture()
def client() -> TestClient:
    """A fresh TestClient with clean in-memory stores."""
    _carts.clear()
    _orders.clear()
    _payments.clear()
    return TestClient(app)


# ── E2E fixtures ──────────────────────────────────────────────────────────────

@pytest.fixture()
def base_url() -> str:
    """Base URL of the running application for E2E tests.

    Override with APP_BASE_URL=http://app:8000 when Selenium runs inside Docker
    (the service name 'app' is resolved by Docker's internal DNS).
    """
    import os
    return os.environ.get("APP_BASE_URL", "http://localhost:8000")


@pytest.fixture()
def driver():
    """Chrome WebDriver, local or remote depending on SELENIUM_REMOTE_URL.

    Set SELENIUM_REMOTE_URL=http://localhost:4444/wd/hub to run against
    a Selenium standalone container (e.g. docker compose up selenium-chrome).
    Leave unset to launch Chrome locally via webdriver-manager.
    """
    import os

    from selenium import webdriver
    from selenium.webdriver.chrome.options import Options
    from selenium.webdriver.chrome.service import Service

    options = Options()
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    remote_url = os.environ.get("SELENIUM_REMOTE_URL")
    if remote_url:
        # Headed mode — visible in noVNC at http://localhost:7900
        drv = webdriver.Remote(command_executor=remote_url, options=options)
    else:
        options.add_argument("--headless=new")
        try:
            from webdriver_manager.chrome import ChromeDriverManager
            service = Service(ChromeDriverManager().install())
            drv = webdriver.Chrome(service=service, options=options)
        except Exception:
            drv = webdriver.Chrome(options=options)

    yield drv
    drv.quit()
