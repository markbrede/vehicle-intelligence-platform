from __future__ import annotations

from datetime import datetime
from typing import Any, Dict, List, Optional

from bson import ObjectId

from src.db import get_collection


def _as_date(d: Any) -> Optional[datetime]:
    # I am having atlas stores datetimes as bson datetime -> comes back as python datetime
    if isinstance(d, datetime):
        return d
    return None


def main() -> None:
    user_id = "mark"
    nickname = "Project 4Runner"

    vehicles = get_collection("vehicles")
    vehicle = vehicles.find_one({"user_id": user_id, "nickname": nickname})

    if not vehicle:
        print(f"No vehicle found for user_id={user_id!r} nickname={nickname!r}")
        return

    vehicle_id: ObjectId = vehicle["_id"]

    print("=== VEHICLE ===")
    print(f"_id:        {vehicle_id}")
    print(f"user_id:    {vehicle.get('user_id')}")
    print(f"year/make:  {vehicle.get('year')} {vehicle.get('make')}")
    print(f"model:      {vehicle.get('model')}")
    print(f"nickname:   {vehicle.get('nickname')}")
    print()

    maintenance_events = list(
        get_collection("maintenance_events")
        .find({"vehicle_id": vehicle_id})
        .sort("date", 1)
    )
    expenses = list(
        get_collection("expenses").find({"vehicle_id": vehicle_id}).sort("date", 1)
    )

    print(f"=== MAINTENANCE EVENTS ({len(maintenance_events)}) ===")
    if not maintenance_events:
        print("(none)")
    for e in maintenance_events:
        date = _as_date(e.get("date"))
        odom = e.get("odometer")
        cat = e.get("category")
        desc = e.get("description")
        cost = e.get("cost")
        vendor = e.get("vendor")
        print(
            f"- {date.date() if date else e.get('date')} | {cat} | ${cost:.2f} | odo={odom} | {vendor or ''} | {desc}"
        )
    print()

    print(f"=== EXPENSES ({len(expenses)}) ===")
    if not expenses:
        print("(none)")
    for x in expenses:
        date = _as_date(x.get("date"))
        odom = x.get("odometer")
        cat = x.get("category")
        amt = x.get("amount")
        vendor = x.get("vendor")
        desc = x.get("description")
        print(
            f"- {date.date() if date else x.get('date')} | {cat} | ${amt:.2f} | odo={odom} | {vendor or ''} | {desc or ''}"
        )
    print()

    # Combined timeline
    timeline: List[Dict[str, Any]] = []

    for e in maintenance_events:
        timeline.append(
            {
                "kind": "maintenance",
                "date": e.get("date"),
                "amount": float(e.get("cost", 0.0)),
                "label": e.get("category"),
                "details": e.get("description"),
            }
        )

    for x in expenses:
        timeline.append(
            {
                "kind": "expense",
                "date": x.get("date"),
                "amount": float(x.get("amount", 0.0)),
                "label": x.get("category"),
                "details": x.get("description"),
            }
        )

    timeline.sort(key=lambda r: (r["date"] is None, r["date"]))

    print(f"=== COMBINED TIMELINE ({len(timeline)}) ===")
    if not timeline:
        print("(none)")
        return

    for row in timeline:
        date = _as_date(row["date"])
        d_str = date.date().isoformat() if date else str(row["date"])
        amt = row["amount"]
        print(
            f"- {d_str} | {row['kind']:11s} | {row['label']:<15s} | ${amt:,.2f} | {row.get('details') or ''}"
        )


if __name__ == "__main__":
    main()
