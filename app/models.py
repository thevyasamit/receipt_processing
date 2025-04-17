from typing import Dict, Any
import uuid


# Simple in-memory storage for receipts keyed by ID
_storage: Dict[str, Dict[str, Any]] = {}


def save_receipt(receipt_data: Dict[str, Any], points: int) -> str:
    """
    Save a receipt entry with a generated ID; return the ID.
    """
    receipt_id = str(uuid.uuid4())
    _storage[receipt_id] = {
        "id": receipt_id,
        "data": receipt_data,
        "points": points
    }
    return receipt_id


def get_receipt(receipt_id: str) -> Dict[str, Any]:
    """
    Retrieve a stored receipt record by ID.
    Returns None if not found.
    """
    return _storage.get(receipt_id) 