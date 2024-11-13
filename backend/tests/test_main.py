import pytest


def test_root(client):
    response = client.get("/")
    assert response.status_code == 200


def test_create_report(client):
    # Create a test point
    test_point = {"lat": 45.5231, "lng": -122.6765}

    response = client.post("/report", json=test_point)
    assert response.status_code == 200

    data = response.json()
    assert data["id"] is not None
    assert data["location"]["lat"] == test_point["lat"]
    assert data["location"]["lng"] == test_point["lng"]
    assert data["timestamp"] is not None


def test_get_report(client):
    # First create a report
    test_point = {"lat": 45.5231, "lng": -122.6765}
    create_response = client.post("/report", json=test_point)
    report_id = create_response.json()["id"]

    # Then retrieve it
    response = client.get(f"/report/{report_id}")
    assert response.status_code == 200

    data = response.json()
    assert data["id"] == report_id
    assert data["location"]["lat"] == test_point["lat"]
    assert data["location"]["lng"] == test_point["lng"]
    assert data["timestamp"] is not None


def test_get_all_reports(client):
    # Create multiple reports
    points = [{"lat": 45.5231, "lng": -122.6765}, {"lat": 40.7128, "lng": -74.0060}]

    created_ids = []
    for point in points:
        response = client.post("/report", json=point)
        created_ids.append(response.json()["id"])

    # Get all reports
    response = client.get("/reports")
    assert response.status_code == 200

    data = response.json()
    assert len(data) == len(points)

    # Verify our created reports are in the response
    received_ids = [report["id"] for report in data]
    for created_id in created_ids:
        assert created_id in received_ids


@pytest.fixture
def admin_headers():
    return {"X-Admin-Key": "test_key"}


@pytest.fixture
def invalid_admin_headers():
    return {"X-Admin-Key": "wrong_key"}


def test_delete_all_reports_unauthorized(client):
    response = client.delete("/admin/reports")
    assert response.status_code == 403


def test_delete_all_reports_wrong_key(client, invalid_admin_headers):
    response = client.delete("/admin/reports", headers=invalid_admin_headers)
    assert response.status_code == 403


def test_delete_all_reports(client, admin_headers):
    # First create some reports
    points = [{"lat": 45.5231, "lng": -122.6765}, {"lat": 40.7128, "lng": -74.0060}]
    for point in points:
        client.post("/report", json=point)

    # Delete all reports
    response = client.delete("/admin/reports", headers=admin_headers)
    assert response.status_code == 200
    assert response.json()["message"].startswith("Deleted")
    assert "2" in response.json()["message"]

    # Verify reports are gone
    response = client.get("/reports")
    assert len(response.json()) == 0


def test_create_mock_reports_unauthorized(client):
    payload = {"location": {"lat": 45.5231, "lng": -122.6765}, "amount": 5}
    response = client.post("/admin/reports", json=payload)
    assert response.status_code == 403


def test_create_mock_reports(client, admin_headers):
    center_point = {"lat": 45.5231, "lng": -122.6765}
    response = client.post("/admin/reports", params={"amount": 5}, json=center_point, headers=admin_headers)
    assert response.status_code == 200

    data = response.json()
    assert len(data) == 5

    # Check that points are within reasonable distance
    center_lat = center_point["lat"]
    center_lng = center_point["lng"]
    for report in data:
        assert abs(report["location"]["lat"] - center_lat) < 0.5
        assert abs(report["location"]["lng"] - center_lng) < 0.5
