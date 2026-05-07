from __future__ import annotations

import pytest
from fastapi.testclient import TestClient

from app.domain.order import OrderStatus
from app.domain.payment import PaymentStatus
from app.main import app, _carts, _orders, _payments


# Fixed seed data for deterministic results across all runs
_SEED_ITEM = {
    "id": "nr-item-001",
    "name": "Laptop Pro",
    "price": 1200.00,
    "stock": 5,
}
_VALID_CARD = "4111111111111111"
_DISCOUNT_CODE = "SAVE10"


@pytest.fixture()
def nr_client() -> TestClient:
    """Fresh TestClient with clean stores for each non-regression test."""
    _carts.clear()
    _orders.clear()
    _payments.clear()
    return TestClient(app)


class TestCriticalPaths:
    """Non-regression tests covering the three critical user paths.

    CP001: Add item → checkout → payment complete
    CP002: Discount code applied correctly to order total
    CP003: Order cancellation prevents payment
    """

    # ── CP001: Full purchase path ─────────────────────────────────────────────

    def test_cp001_add_item_to_cart(self, nr_client: TestClient) -> None:
        """CP001-a: A valid item can be added to a fresh cart."""
        cart_id = nr_client.post("/cart").json()["id"]
        response = nr_client.post(f"/cart/{cart_id}/items", json=_SEED_ITEM)
        assert response.status_code == 201
        assert response.json()["total"] == _SEED_ITEM["price"]

    def test_cp001_order_created_from_cart(self, nr_client: TestClient) -> None:
        """CP001-b: An order created from a loaded cart is PENDING."""
        cart_id = nr_client.post("/cart").json()["id"]
        nr_client.post(f"/cart/{cart_id}/items", json=_SEED_ITEM)
        response = nr_client.post("/orders", json={"cart_id": cart_id})
        assert response.status_code == 201
        assert response.json()["status"] == OrderStatus.PENDING.value

    def test_cp001_payment_completes_order(self, nr_client: TestClient) -> None:
        """CP001-c: A successful payment confirms the order."""
        cart_id = nr_client.post("/cart").json()["id"]
        nr_client.post(f"/cart/{cart_id}/items", json=_SEED_ITEM)
        order_id = nr_client.post("/orders", json={"cart_id": cart_id}).json()["id"]
        payment = nr_client.post(
            "/payment", json={"order_id": order_id, "card_number": _VALID_CARD}
        ).json()
        assert payment["status"] == PaymentStatus.SUCCESS.value
        order = nr_client.get(f"/orders/{order_id}").json()
        assert order["status"] == OrderStatus.CONFIRMED.value

    # ── CP002: Discount path ──────────────────────────────────────────────────

    def test_cp002_discount_reduces_total(self, nr_client: TestClient) -> None:
        """CP002-a: Applying SAVE10 reduces the cart total by 10%."""
        cart_id = nr_client.post("/cart").json()["id"]
        nr_client.post(f"/cart/{cart_id}/items", json=_SEED_ITEM)
        nr_client.post(f"/cart/{cart_id}/discount", json={"code": _DISCOUNT_CODE})
        total = nr_client.get(f"/cart/{cart_id}").json()["total"]
        assert total == pytest.approx(_SEED_ITEM["price"] * 0.9, rel=1e-2)

    def test_cp002_discounted_order_total_is_correct(
        self, nr_client: TestClient
    ) -> None:
        """CP002-b: The order total reflects the discounted cart total."""
        cart_id = nr_client.post("/cart").json()["id"]
        nr_client.post(f"/cart/{cart_id}/items", json=_SEED_ITEM)
        nr_client.post(f"/cart/{cart_id}/discount", json={"code": _DISCOUNT_CODE})
        discounted_total = nr_client.get(f"/cart/{cart_id}").json()["total"]
        order = nr_client.post("/orders", json={"cart_id": cart_id}).json()
        assert order["total"] == pytest.approx(discounted_total, rel=1e-2)

    # ── CP003: Cancellation path ──────────────────────────────────────────────

    def test_cp003_cancelled_order_blocks_payment(
        self, nr_client: TestClient
    ) -> None:
        """CP003: Attempting to pay a cancelled order returns 422."""
        cart_id = nr_client.post("/cart").json()["id"]
        nr_client.post(f"/cart/{cart_id}/items", json=_SEED_ITEM)
        order_id = nr_client.post("/orders", json={"cart_id": cart_id}).json()["id"]
        nr_client.delete(f"/orders/{order_id}")
        response = nr_client.post(
            "/payment", json={"order_id": order_id, "card_number": _VALID_CARD}
        )
        assert response.status_code == 422
