from __future__ import annotations

from fastapi.testclient import TestClient


class TestPaymentAPI:
    """API tests for payment endpoints."""

    def _create_order(self, client: TestClient) -> str:
        """Helper: create a cart with one item, create an order, return order_id."""
        cart_id = client.post("/cart").json()["id"]
        client.post(
            f"/cart/{cart_id}/items",
            json={"id": "item-001", "name": "Laptop", "price": 999.99, "stock": 10},
        )
        return client.post("/orders", json={"cart_id": cart_id}).json()["id"]

    def test_process_valid_payment_returns_201_success(
        self, client: TestClient
    ) -> None:
        """POST /payment with a valid card returns 201 and status SUCCESS."""
        order_id = self._create_order(client)
        response = client.post(
            "/payment",
            json={"order_id": order_id, "card_number": "4111111111111111"},
        )
        assert response.status_code == 201
        assert response.json()["status"] == "SUCCESS"

    def test_process_declined_card_returns_declined(
        self, client: TestClient
    ) -> None:
        """POST /payment with a declined card returns status DECLINED."""
        order_id = self._create_order(client)
        response = client.post(
            "/payment",
            json={"order_id": order_id, "card_number": "4000000000000002"},
        )
        assert response.status_code == 201
        assert response.json()["status"] == "DECLINED"

    def test_get_payment_returns_correct_amount(self, client: TestClient) -> None:
        """GET /payment/{id} returns the correct amount."""
        order_id = self._create_order(client)
        payment_id = client.post(
            "/payment",
            json={"order_id": order_id, "card_number": "4111111111111111"},
        ).json()["id"]
        response = client.get(f"/payment/{payment_id}")
        assert response.status_code == 200
        assert response.json()["amount"] == 999.99

    def test_refund_payment_returns_refunded_status(
        self, client: TestClient
    ) -> None:
        """POST /payment/{id}/refund returns status REFUNDED."""
        order_id = self._create_order(client)
        payment_id = client.post(
            "/payment",
            json={"order_id": order_id, "card_number": "4111111111111111"},
        ).json()["id"]
        response = client.post(f"/payment/{payment_id}/refund")
        assert response.status_code == 200
        assert response.json()["status"] == "REFUNDED"

    def test_get_nonexistent_payment_returns_404(self, client: TestClient) -> None:
        """GET /payment/{id} with unknown id returns 404."""
        response = client.get("/payment/nonexistent-id")
        assert response.status_code == 404
