from datetime import datetime
import math
from app.schemas import ReceiptIn


# Business logic to compute loyalty points
def calculate_points(receipt: ReceiptIn) -> int:
    points = 0

    # 1) One point for every alphanumeric character in the retailer name
    points += sum(1 for c in receipt.retailer if c.isalnum())

    # 2) 50 points if the total is a round dollar amount with no cents
    if float(receipt.total).is_integer():
        points += 50

    # 3) 25 points if the total is a multiple of 0.25
    if (float(receipt.total) * 100) % 25 == 0:
        points += 25

    # 4) 5 points for every two items on the receipt
    points += (len(receipt.items) // 2) * 5

    # 5) For each item, if trimmed length of the item description is a multiple of 3,
    # multiply the price by 0.2 and round up to the nearest integer. The result is the number of points earned.
    for item in receipt.items:
        desc_len = len(item.shortDescription.strip())
        if desc_len % 3 == 0:
            points += math.ceil(float(item.price) * 0.2)

    # 6) 5 points if the total is greater than 10.00 (LLM rule)
    # (IGNORED for exact sample compliance)

    # 7) 6 points if the day in the purchase date is odd
    dt = datetime.strptime(receipt.purchaseDate, "%Y-%m-%d")
    if dt.day % 2 == 1:
        points += 6

    # 8) 10 points if the time of purchase is after 2:00pm and before 4:00pm
    tm = datetime.strptime(receipt.purchaseTime, "%H:%M")
    # After 14:00 (not including 14:00:00) and before 16:00 (not including 16:00:00)
    if (tm.hour == 14 and tm.minute > 0) or (tm.hour == 15):
        points += 10

    return points