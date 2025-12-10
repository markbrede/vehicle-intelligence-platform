from datetime import datetime

from bson import ObjectId

from src.db import get_collection
from src.models import expense_schema



def main() -> None:
    expenses = get_collection("expenses")

    # 4RUNNER ObjectId from the vehicles collection
    vehicle_id = ObjectId("6939c28d61aa4ccbd80730b8")

    doc = expense_schema(
        user_id="mark",
        vehicle_id=vehicle_id,
        date=datetime(2024, 11, 5),
        category="Fuel",
        amount=72.35,
        vendor="Costco Gas",
        description="Full tank before Utah trip",
        odometer=198500,
    )

    result = expenses.insert_one(doc)
    print("Inserted expense with ID:", result.inserted_id)


if __name__ == "__main__":
    main()
