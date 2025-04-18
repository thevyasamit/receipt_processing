from pydantic import BaseModel, Field, field_validator
from typing import List
from datetime import datetime


class Item(BaseModel):
    shortDescription: str = Field(..., pattern=r"^[\w\s\-]+$")  # Descriptor of the item on the receipt
    price: str = Field(..., pattern=r"^\d+\.\d{2}$")           # Price of the item


class ReceiptIn(BaseModel):
    retailer: str = Field(..., pattern=r"^[\w\s\-&]+$")        # Name of retailer/store
    purchaseDate: str = Field(...)                             # Date in YYYY-MM-DD format
    purchaseTime: str = Field(...)                             # Time in HH:MM (24h) format
    items: List[Item] = Field(..., min_length=1)               # List of purchased items
    total: str = Field(..., pattern=r"^\d+\.\d{2}$")          # Total amount charged

    @field_validator("purchaseDate")
    @classmethod
    def validate_date(cls, v: str) -> str:
        try:
            datetime.strptime(v, "%Y-%m-%d")
            return v
        except ValueError:
            raise ValueError("Invalid date format. Expected YYYY-MM-DD")

    @field_validator("purchaseTime")
    @classmethod
    def validate_time(cls, v: str) -> str:
        try:
            datetime.strptime(v, "%H:%M")
            return v
        except ValueError:
            raise ValueError("Invalid time format. Expected HH:MM")

    @field_validator("items")
    @classmethod
    def validate_items(cls, v: List[Item]) -> List[Item]:
        if not v:
            raise ValueError("At least one item is required")
        return v


class ReceiptOut(BaseModel):
    id: str = Field(..., pattern=r"^\S+$")                     # Generated receipt ID


class PointsOut(BaseModel):
    points: int                                                # Points for the receipt 