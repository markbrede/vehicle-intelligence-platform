from datetime import datetime

from src.db import get_collection
from src.models import maintenance_event_schema


def main() -> None:
    vehicles = get_collection("vehicles")

    # Find the 4Runner by nickname
    vehicle = vehicles.find_one({"nickname": "Project 4Runner"})

    if not vehicle:
        print("No vehicle found with nickname 'Project 4Runner'. Insert vehicle first.")
        return

    vehicle_id = vehicle["_id"]

    maintenance_events = get_collection("maintenance_events")

    event = maintenance_event_schema(
        user_id="mark",
        vehicle_id=vehicle_id,
        date=datetime(2024, 11, 1),
        odometer=190_000,
        category="Oil Change",
        description="Engine oil and filter change",
        cost=89.99,
        vendor="Local shop",
        notes="Synthetic 5W-30, checked fluids",
    )

    result = maintenance_events.insert_one(event)
    print("Inserted maintenance event with ID:", result.inserted_id)


if __name__ == "__main__":
    main()
