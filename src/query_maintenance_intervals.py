from __future__ import annotations

from typing import Dict, List
from statistics import mean

from src.db import get_collection


def main() -> None:
    user_id = "mark"
    nickname = "Project 4Runner"

    vehicles = get_collection("vehicles")
    maintenance = get_collection("maintenance_events")

    vehicle = vehicles.find_one({"user_id": user_id, "nickname": nickname})
    if not vehicle:
        print("Vehicle not found.")
        return

    vehicle_id = vehicle["_id"]

    events = list(maintenance.find({"vehicle_id": vehicle_id}).sort("odometer", 1))

    if len(events) < 2:
        print("Not enough maintenance history for interval analysis.")
        return

    by_category: Dict[str, List[int]] = {}

    for prev, curr in zip(events, events[1:]):
        if prev.get("odometer") is None or curr.get("odometer") is None:
            continue

        delta = curr["odometer"] - prev["odometer"]
        category = curr["category"]
        by_category.setdefault(category, []).append(delta)

    print("\n=== MAINTENANCE INTERVAL ANALYSIS ===")
    print(f"Vehicle: {vehicle['year']} {vehicle['make']} {vehicle['model']}")
    print()

    for category, intervals in by_category.items():
        avg_interval = mean(intervals)
        last_event = next(e for e in reversed(events) if e["category"] == category)
        next_due = last_event["odometer"] + avg_interval

        print(f"{category}")
        print(f"  Avg interval: {avg_interval:,.0f} miles")
        print(f"  Last service: {last_event['odometer']:,} miles")
        print(f"  Next due ~ : {next_due:,.0f} miles")
        print()


if __name__ == "__main__":
    main()
