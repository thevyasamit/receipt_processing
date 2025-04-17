from fastapi import APIRouter, HTTPException, status
from app.schemas import ReceiptIn, ReceiptOut, PointsOut
from app.services import calculate_points
from app.models import save_receipt, get_receipt
from typing import Dict


router = APIRouter()


@router.post(
    "/process",
    response_model=ReceiptOut,
    status_code=status.HTTP_200_OK
)
async def process_receipt(receipt: ReceiptIn):
    """
    Process a receipt and return its ID and points.
    """
    points = calculate_points(receipt)  # Compute loyalty points
    receipt_id = save_receipt(receipt.dict(), points)  # Store with generated ID
    return {"id": receipt_id, "points": points}


@router.get(
    "/{receipt_id}/points",
    response_model=PointsOut,
    status_code=status.HTTP_200_OK
)
async def get_points(receipt_id: str):
    """
    Retrieve points for a receipt by ID.
    """
    data = get_receipt(receipt_id)  # Fetch stored record
    if not data:
        # No record found → raise 404 Not Found
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Receipt not found"
        )
    # Return stored points
    return {"points": data["points"]} 