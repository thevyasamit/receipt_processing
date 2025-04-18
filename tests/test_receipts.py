import pytest
from fastapi.testclient import TestClient
from app.main import app
from datetime import datetime


client = TestClient(app)


def test_valid_receipt_processing():
    """Test processing a valid receipt"""
    receipt = {
        "retailer": "M&M Corner Market",
        "purchaseDate": "2022-01-01",
        "purchaseTime": "13:01",
        "items": [
            {"shortDescription": "Mountain Dew 12PK", "price": "6.49"},
            {"shortDescription": "Emils Cheese Pizza", "price": "12.25"}
        ],
        "total": "18.74"
    }
    
    # Test POST endpoint
    response = client.post("/receipts/process", json=receipt)
    assert response.status_code == 200
    assert "id" in response.json()
    receipt_id = response.json()["id"]
    
    # Verify ID format
    assert len(receipt_id) > 0
    assert " " not in receipt_id  # No whitespace as per pattern
    
    # Test GET endpoint
    points_response = client.get(f"/receipts/{receipt_id}/points")
    assert points_response.status_code == 200
    assert "points" in points_response.json()
    assert isinstance(points_response.json()["points"], int)


def test_invalid_receipt_format():
    """Test processing an invalid receipt format"""
    invalid_receipts = [
        # Missing required fields
        {
            "retailer": "M&M Corner Market",
            "purchaseDate": "2022-01-01",
            "purchaseTime": "13:01",
            "items": []
        },
        # Invalid retailer format
        {
            "retailer": "M&M Corner Market!@#",
            "purchaseDate": "2022-01-01",
            "purchaseTime": "13:01",
            "items": [{"shortDescription": "Item", "price": "1.00"}],
            "total": "1.00"
        },
        # Invalid date format
        {
            "retailer": "M&M Corner Market",
            "purchaseDate": "2022/01/01",
            "purchaseTime": "13:01",
            "items": [{"shortDescription": "Item", "price": "1.00"}],
            "total": "1.00"
        },
        # Invalid time format
        {
            "retailer": "M&M Corner Market",
            "purchaseDate": "2022-01-01",
            "purchaseTime": "1:01 PM",
            "items": [{"shortDescription": "Item", "price": "1.00"}],
            "total": "1.00"
        },
        # Invalid price format
        {
            "retailer": "M&M Corner Market",
            "purchaseDate": "2022-01-01",
            "purchaseTime": "13:01",
            "items": [{"shortDescription": "Item", "price": "1"}],
            "total": "1.00"
        }
    ]
    
    for receipt in invalid_receipts:
        response = client.post("/receipts/process", json=receipt)
        assert response.status_code == 400
        assert "Please verify input" in response.json()["detail"]


def test_nonexistent_receipt():
    """Test getting points for a non-existent receipt"""
    response = client.get("/receipts/nonexistent-id/points")
    assert response.status_code == 404
    assert "No receipt found for that ID" in response.json()["detail"]


def test_points_calculation():
    """Test points calculation with various scenarios"""
    test_cases = [
        {
            "receipt": {
                "retailer": "Target",
                "purchaseDate": "2022-01-01",
                "purchaseTime": "13:01",
                "items": [
                    {"shortDescription": "Mountain Dew 12PK", "price": "6.49"},
                    {"shortDescription": "Emils Cheese Pizza", "price": "12.25"},
                    {"shortDescription": "Knorr Creamy Chicken", "price": "1.26"},
                    {"shortDescription": "Doritos Nacho Cheese", "price": "3.35"},
                    {"shortDescription": "   Klarbrunn 12-PK 12 FL OZ  ", "price": "12.00"}
                ],
                "total": "35.35"
            },
            "expected_points": 28
        },
        {
            "receipt": {
                "retailer": "M&M Corner Market",
                "purchaseDate": "2022-03-20",
                "purchaseTime": "14:33",
                "items": [
                    {"shortDescription": "Gatorade", "price": "2.25"},
                    {"shortDescription": "Gatorade", "price": "2.25"},
                    {"shortDescription": "Gatorade", "price": "2.25"},
                    {"shortDescription": "Gatorade", "price": "2.25"}
                ],
                "total": "9.00"
            },
            "expected_points": 109
        }
    ]
    
    for case in test_cases:
        # Process receipt
        response = client.post("/receipts/process", json=case["receipt"])
        assert response.status_code == 200
        receipt_id = response.json()["id"]
        
        # Get points
        points_response = client.get(f"/receipts/{receipt_id}/points")
        assert points_response.status_code == 200
        assert points_response.json()["points"] == case["expected_points"] 