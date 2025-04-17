from pydantic import BaseModel
from typing import List


class Item(BaseModel):
    shortDescription: str  # Descriptor of the item on the receipt
    price: str            # Price of the item


class ReceiptIn(BaseModel):
    retailer: str          # Name of retailer/store
    purchaseDate: str      # Date in YYYY-MM-DD format
    purchaseTime: str      # Time in HH:MM (24h) format
    items: List[Item]      # List of purchased items
    total: str             # Total amount charged


class ReceiptOut(BaseModel):
    id: str                # Generated receipt ID
    points: int            # Calculated points


class PointsOut(BaseModel):
    points: int            # Points for the receipt 