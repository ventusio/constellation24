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
