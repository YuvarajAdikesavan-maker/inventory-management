"""
Tests for restocking order API endpoints.
"""
from datetime import date, timedelta

import pytest

from mock_data import restock_orders


@pytest.fixture(autouse=True)
def clear_restock_orders():
    """Restock orders live in a module-level list, so reset it around every test."""
    restock_orders.clear()
    yield
    restock_orders.clear()


def _forecasts(client):
    return {f["item_sku"]: f for f in client.get("/api/demand").json()}


class TestRestockOrdersEndpoints:
    """Test suite for restocking order endpoints."""

    def test_demand_forecasts_include_cost_and_lead_time(self, client):
        """Test that demand forecasts expose the fields restocking needs."""
        response = client.get("/api/demand")
        assert response.status_code == 200

        for forecast in response.json():
            assert isinstance(forecast["unit_cost"], (int, float))
            assert forecast["unit_cost"] > 0
            assert isinstance(forecast["lead_time_days"], int)
            assert forecast["lead_time_days"] > 0

    def test_get_restock_orders_initially_empty(self, client):
        """Test that no restock orders exist before any are submitted."""
        response = client.get("/api/restock-orders")
        assert response.status_code == 200
        assert response.json() == []

    def test_create_restock_order(self, client):
        """Test submitting a restock order."""
        forecasts = _forecasts(client)
        response = client.post("/api/restock-orders", json={
            "items": [
                {"sku": "WDG-001", "quantity": 150},
                {"sku": "GSK-203", "quantity": 100},
            ],
            "budget": 5000,
        })
        assert response.status_code == 201

        order = response.json()
        assert order["order_number"].startswith("RST-")
        assert order["status"] == "Submitted"
        assert order["budget"] == 5000
        assert len(order["items"]) == 2

        expected_total = 150 * forecasts["WDG-001"]["unit_cost"] + 100 * forecasts["GSK-203"]["unit_cost"]
        assert abs(order["total_cost"] - expected_total) < 0.01

    def test_restock_order_lead_time_is_slowest_item(self, client):
        """Test that lead time is the longest lead time among the items."""
        forecasts = _forecasts(client)
        response = client.post("/api/restock-orders", json={
            "items": [
                {"sku": "FLT-405", "quantity": 10},
                {"sku": "VLV-506", "quantity": 1},
            ],
            "budget": 10000,
        })
        assert response.status_code == 201

        order = response.json()
        expected_days = max(forecasts["FLT-405"]["lead_time_days"], forecasts["VLV-506"]["lead_time_days"])
        assert order["lead_time_days"] == expected_days
        assert order["submitted_date"] == date.today().isoformat()
        assert order["expected_delivery"] == (date.today() + timedelta(days=expected_days)).isoformat()

    def test_restock_order_uses_server_side_price(self, client):
        """Test that a client-supplied price is ignored."""
        forecasts = _forecasts(client)
        response = client.post("/api/restock-orders", json={
            "items": [{"sku": "WDG-001", "quantity": 10, "unit_cost": 0.01}],
            "budget": 1000,
        })
        assert response.status_code == 201

        item = response.json()["items"][0]
        assert item["unit_cost"] == forecasts["WDG-001"]["unit_cost"]

    def test_create_restock_order_empty_items(self, client):
        """Test that an order with no items is rejected."""
        response = client.post("/api/restock-orders", json={"items": [], "budget": 1000})
        assert response.status_code == 400
        assert "detail" in response.json()

    def test_create_restock_order_unknown_sku(self, client):
        """Test that an unknown SKU is rejected."""
        response = client.post("/api/restock-orders", json={
            "items": [{"sku": "NOPE-999", "quantity": 1}],
            "budget": 1000,
        })
        assert response.status_code == 400
        assert "unknown sku" in response.json()["detail"].lower()

    @pytest.mark.parametrize("quantity", [0, -5, 1_000_001])
    def test_create_restock_order_invalid_quantity(self, client, quantity):
        """Test that zero, negative or absurdly large quantities fail validation."""
        response = client.post("/api/restock-orders", json={
            "items": [{"sku": "WDG-001", "quantity": quantity}],
            "budget": 1000,
        })
        assert response.status_code == 422

    def test_create_restock_order_duplicate_sku(self, client):
        """Test that the same SKU cannot appear twice in one order."""
        response = client.post("/api/restock-orders", json={
            "items": [
                {"sku": "WDG-001", "quantity": 1},
                {"sku": "WDG-001", "quantity": 2},
            ],
            "budget": 1000,
        })
        assert response.status_code == 400
        assert "once" in response.json()["detail"].lower()

    @pytest.mark.parametrize("budget", ["NaN", "Infinity", -1])
    def test_create_restock_order_invalid_budget(self, client, budget):
        """Test that NaN, infinite or negative budgets cannot bypass the budget check."""
        # Sent as raw JSON because NaN/Infinity aren't valid values for the json= encoder
        body = '{"items": [{"sku": "WDG-001", "quantity": 1}], "budget": %s}' % budget
        response = client.post(
            "/api/restock-orders", content=body, headers={"Content-Type": "application/json"}
        )
        assert response.status_code == 400
        assert "budget" in response.json()["detail"].lower()
        assert client.get("/api/restock-orders").json() == []

    def test_create_restock_order_over_budget(self, client):
        """Test that an order above the budget is rejected and not stored."""
        response = client.post("/api/restock-orders", json={
            "items": [{"sku": "MTR-304", "quantity": 100}],
            "budget": 100,
        })
        assert response.status_code == 400
        assert "budget" in response.json()["detail"].lower()
        assert client.get("/api/restock-orders").json() == []

    def test_create_restock_order_missing_fields(self, client):
        """Test that a malformed request fails validation."""
        response = client.post("/api/restock-orders", json={"items": []})
        assert response.status_code == 422

    def test_get_restock_orders_newest_first(self, client):
        """Test that submitted orders are listed newest first."""
        for sku in ["WDG-001", "GSK-203"]:
            response = client.post("/api/restock-orders", json={
                "items": [{"sku": sku, "quantity": 1}],
                "budget": 1000,
            })
            assert response.status_code == 201

        orders = client.get("/api/restock-orders").json()
        assert len(orders) == 2
        assert orders[0]["items"][0]["sku"] == "GSK-203"
        assert orders[1]["items"][0]["sku"] == "WDG-001"

    def test_restock_orders_do_not_affect_customer_orders(self, client):
        """Test that restock orders stay out of the customer orders list."""
        before = len(client.get("/api/orders").json())
        client.post("/api/restock-orders", json={
            "items": [{"sku": "WDG-001", "quantity": 1}],
            "budget": 1000,
        })
        assert len(client.get("/api/orders").json()) == before
