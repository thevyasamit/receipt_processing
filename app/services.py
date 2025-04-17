from datetime import datetime
import math
from app.schemas import ReceiptIn


# Business logic to compute loyalty points
def calculate_points(receipt: ReceiptIn) -> int:
    points = 0

    # 1) One point per alphanumeric character in retailer name
    for c in receipt.retailer:
        if c.isalnum():
            points += 1

    # 2) 50 points if total is a round dollar amount
    if float(receipt.total).is_integer():
        points += 50

    # 3) 25 points if total is a multiple of 0.25
    if (float(receipt.total) * 100) % 25 == 0:
        points += 25

    # 4) 5 points for every two items on the receipt
    points += (len(receipt.items) // 2) * 5

    # 5) For each item, if trimmed description length % 3 == 0, add ceil(price * 0.2)
    for item in receipt.items:
        desc_len = len(item.shortDescription.strip())
        if desc_len % 3 == 0:
            points += math.ceil(float(item.price) * 0.2)

    # 6) 5 points if total > $10.00 (LLM-generated bonus)
    if float(receipt.total) > 10.00:
        points += 5

    # 7) 6 points if purchase date's day is odd
    dt = datetime.strptime(receipt.purchaseDate, "%Y-%m-%d")
    if dt.day % 2 == 1:
        points += 6

    # 8) 10 points if purchase time is after 2pm and before 4pm
    tm = datetime.strptime(receipt.purchaseTime, "%H:%M")
    if 14 <= tm.hour < 16:
        points += 10

    return points 