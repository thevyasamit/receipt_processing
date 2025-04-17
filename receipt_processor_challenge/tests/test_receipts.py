import pytest
from fastapi.testclient import TestClient
from app.main import app


client = TestClient(app)


def test_process_and_get_points():
    # Example payload matching api.yml spec
    receipt = {
        "retailer": "M&M Corner Market",
        "purchaseDate": "2022-03-20",
        "purchaseTime": "14:33",
        "items": [
            {"shortDescription": "Mountain Dew 12PK", "price": 6.49},
            {"shortDescription": "Emils Cheese Pizza", "price": 12.25}
        ],
        "total": 18.00
    }
    # 1) POST should return 200 OK and a points field
    post_resp = client.post("/receipts/process", json=receipt)
    assert post_resp.status_code == 200
    assert "points" in post_resp.json()
    pts = post_resp.json()["points"]

    # 2) GET should return 200 OK and the same points
    get_resp = client.get(f"/receipts/{receipt['retailer']}/points")
    assert get_resp.status_code == 200
    assert get_resp.json()["points"] == pts 