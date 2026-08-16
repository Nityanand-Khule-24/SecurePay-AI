from fastapi.testclient import TestClient

from backend.app.main import app


client = TestClient(app)


# =========================================================
# TEST DASHBOARD
# =========================================================

def test_dashboard():

    response = client.get(
        "/prediction/dashboard"
    )

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "success"

    assert "dashboard" in data


# =========================================================
# TEST ANALYTICS
# =========================================================

def test_analytics_summary():

    response = client.get(
        "/prediction/analytics/summary"
    )

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "success"

    assert "analytics" in data


# =========================================================
# TEST RISK DISTRIBUTION
# =========================================================

def test_risk_distribution():

    response = client.get(
        "/prediction/analytics/risk-distribution"
    )

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "success"

    assert "risk_distribution" in data


# =========================================================
# TEST ALERTS
# =========================================================

def test_alerts():

    response = client.get(
        "/prediction/alerts"
    )

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "success"

    assert "alerts" in data


# =========================================================
# TEST UNRESOLVED ALERTS
# =========================================================

def test_unresolved_alerts():

    response = client.get(
        "/prediction/alerts/unresolved"
    )

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "success"

    assert "alerts" in data

# =========================================================
# TEST COMPLETE TRANSACTION PROCESSING
# =========================================================

def test_process_transaction():

    payload = {
        "type": "TRANSFER",
        "amount": 5000.0,
        "sender_id": "C_PYTEST_SENDER_001",
        "receiver_id": "C_PYTEST_RECEIVER_001",
        "oldbalanceorg": 10000.0,
        "newbalanceorig": 5000.0,
        "oldbalancedest": 2000.0,
        "newbalancedest": 7000.0,
        "created_at": "2026-08-16T12:00:00"
    }

    response = client.post(
        "/prediction/process",
        json=payload
    )

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "success"

    assert "transaction_id" in data
    assert "prediction" in data
    assert "fraud_probability" in data
    assert "risk_level" in data
    assert "decision" in data
    assert "action" in data
    assert "alert" in data

    assert data["prediction"] in [0, 1]

    assert 0.0 <= data["fraud_probability"] <= 1.0

    assert data["risk_level"] in [
        "LOW",
        "MEDIUM",
        "HIGH"
    ]

    assert data["decision"] in [
        "SAFE",
        "REVIEW",
        "BLOCK"
    ]

    assert isinstance(
        data["alert"],
        bool
    )