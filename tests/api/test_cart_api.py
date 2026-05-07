from __future__ import annotations

import pytest
from fastapi.testclient import TestClient


class TestCartAPI:
    """API tests for cart endpoints."""

    def test_create_cart_returns_201_with_id(self, client: TestClient) -> None:
        """POST /cart returns 201 and a cart id."""
        response = client.post("/cart")
        assert response.status_code == 201
        assert "id" in response.json()

    def test_add_item_returns_201_and_total(self, client: TestClient) -> None:
        """POST /cart/{id}/items returns 201 and updated total."""
        cart_id = client.post("/cart").json()["id"]
        response = client.post(
            f"/cart/{cart_id}/items",
            json={"id": "item-001", "name": "Laptop", "price": 999.99, "stock": 10},
        )
        assert response.status_code == 201
        assert response.json()["total"] == 999.99

    def test_add_out_of_stock_item_returns_409(self, client: TestClient) -> None:
        """POST /cart/{id}/items with stock=0 returns 409."""
        cart_id = client.post("/cart").json()["id"]
        response = client.post(
            f"/cart/{cart_id}/items",
            json={"id": "item-002", "name": "Mouse", "price": 29.99, "stock": 0},
        )
        assert response.status_code == 409

    def test_get_cart_returns_total(self, client: TestClient) -> None:
        """GET /cart/{id} returns cart with correct total."""
        cart_id = client.post("/cart").json()["id"]
        client.post(
            f"/cart/{cart_id}/items",
            json={"id": "item-001", "name": "Laptop", "price": 999.99, "stock": 10},
        )
        response = client.get(f"/cart/{cart_id}")
        assert response.status_code == 200
        assert response.json()["total"] == 999.99

    def test_apply_valid_discount_reduces_total(self, client: TestClient) -> None:
        """POST /cart/{id}/discount with SAVE10 reduces total by 10%."""
        cart_id = client.post("/cart").json()["id"]
        client.post(
            f"/cart/{cart_id}/items",
            json={"id": "item-001", "name": "Laptop", "price": 1000.00, "stock": 5},
        )
        response = client.post(
            f"/cart/{cart_id}/discount", json={"code": "SAVE10"}
        )
        assert response.status_code == 200
        assert response.json()["total"] == pytest.approx(900.00, rel=1e-2)

    def test_apply_invalid_discount_returns_422(self, client: TestClient) -> None:
        """POST /cart/{id}/discount with unknown code returns 422."""
        cart_id = client.post("/cart").json()["id"]
        response = client.post(
            f"/cart/{cart_id}/discount", json={"code": "INVALID"}
        )
        assert response.status_code == 422
