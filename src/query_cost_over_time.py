from __future__ import annotations

from datetime import datetime
from typing import Dict

from src.db import get_collection


def month_key(d: datetime) -> str:
    return f"{d.year}-{d.month:02d}"


def main() -> None:
    user_id = "mark"
    nickname = "Project 4Runner"

    vehicles = get_collection("vehicles")
    maintenance = get_collection("maintenance_events")
    expenses = get_collection("expenses")

    vehicle = vehicles.find_one({"user_id": user_id, "nickname": nickname})
    if not vehicle:
        print("Vehicle not found.")
        return

    vehicle_id = vehicle["_id"]

    monthly: Dict[str, float] = {}

    # maintenance
    for m in maintenance.find({"vehicle_id": vehicle_id}):
        key = month_key(m["date"])
        monthly[key] = monthly.get(key, 0.0) + float(m["cost"])

    # expenses
    for e in expenses.find({"vehicle_id": vehicle_id}):
        key = month_key(e["date"])
        monthly[key] = monthly.get(key, 0.0) + float(e["amount"])

    print("\n=== COST OVER TIME ===")
    print(f"Vehicle: {vehicle['year']} {vehicle['make']} {vehicle['model']}")
    print()

    cumulative = 0.0
    for month in sorted(monthly.keys()):
        cumulative += monthly[month]
        print(
            f"{month} | Monthly: ${monthly[month]:8.2f} | Cumulative: ${cumulative:8.2f}"
        )


if __name__ == "__main__":
    main()
