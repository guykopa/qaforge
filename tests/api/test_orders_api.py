from __future__ import annotations

from fastapi.testclient import TestClient


class TestOrdersAPI:
    """API tests for order endpoints."""

    def _create_cart_with_item(self, client: TestClient) -> str:
        """Helper: create a cart with one item and return cart_id."""
        cart_id = client.post("/cart").json()["id"]
        client.post(
            f"/cart/{cart_id}/items",
            json={"id": "item-001", "name": "Laptop", "price": 999.99, "stock": 10},
        )
        return cart_id

    def test_create_order_returns_201_with_pending_status(
        self, client: TestClient
    ) -> None:
        """POST /orders returns 201 and status PENDING."""
        cart_id = self._create_cart_with_item(client)
        response = client.post("/orders", json={"cart_id": cart_id})
        assert response.status_code == 201
        assert response.json()["status"] == "PENDING"
        assert "id" in response.json()

    def test_create_order_with_empty_cart_returns_422(
        self, client: TestClient
    ) -> None:
        """POST /orders with an empty cart returns 422."""
        cart_id = client.post("/cart").json()["id"]
        response = client.post("/orders", json={"cart_id": cart_id})
        assert response.status_code == 422

    def test_get_order_returns_correct_total(self, client: TestClient) -> None:
        """GET /orders/{id} returns the correct total."""
        cart_id = self._create_cart_with_item(client)
        order_id = client.post("/orders", json={"cart_id": cart_id}).json()["id"]
        response = client.get(f"/orders/{order_id}")
        assert response.status_code == 200
        assert response.json()["total"] == 999.99

    def test_cancel_order_changes_status_to_cancelled(
        self, client: TestClient
    ) -> None:
        """DELETE /orders/{id} transitions status to CANCELLED."""
        cart_id = self._create_cart_with_item(client)
        order_id = client.post("/orders", json={"cart_id": cart_id}).json()["id"]
        response = client.delete(f"/orders/{order_id}")
        assert response.status_code == 200
        assert response.json()["status"] == "CANCELLED"

    def test_get_nonexistent_order_returns_404(self, client: TestClient) -> None:
        """GET /orders/{id} with unknown id returns 404."""
        response = client.get("/orders/nonexistent-id")
        assert response.status_code == 404
