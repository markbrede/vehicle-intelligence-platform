from __future__ import annotations

from typing import Dict

from bson import ObjectId

from src.db import get_collection


def main() -> None:
    user_id = "mark"
    nickname = "Project 4Runner"

    vehicles = get_collection("vehicles")
    vehicle = vehicles.find_one({"user_id": user_id, "nickname": nickname})

    if not vehicle:
        print(f"No vehicle found for user_id={user_id!r} nickname={nickname!r}")
        return

    vehicle_id: ObjectId = vehicle["_id"]

    maint_cursor = get_collection("maintenance_events").find({"vehicle_id": vehicle_id})
    exp_cursor = get_collection("expenses").find({"vehicle_id": vehicle_id})

    maintenance_total = 0.0
    expense_total = 0.0

    maint_by_category: Dict[str, float] = {}
    exp_by_category: Dict[str, float] = {}

    maint_count = 0
    exp_count = 0

    for e in maint_cursor:
        maint_count += 1
        cost = float(e.get("cost", 0.0))
        maintenance_total += cost
        cat = e.get("category") or "Uncategorized"
        maint_by_category[cat] = maint_by_category.get(cat, 0.0) + cost

    for x in exp_cursor:
        exp_count += 1
        amt = float(x.get("amount", 0.0))
        expense_total += amt
        cat = x.get("category") or "Uncategorized"
        exp_by_category[cat] = exp_by_category.get(cat, 0.0) + amt

    grand_total = maintenance_total + expense_total

    print("=== TOTAL COST SUMMARY ===")
    print(
        f"Vehicle: {vehicle.get('year')} {vehicle.get('make')} {vehicle.get('model')} ({vehicle.get('nickname')})"
    )
    print(f"Vehicle _id: {vehicle_id}")
    print()
    print(f"Maintenance events: {maint_count:>3d} | Total: ${maintenance_total:,.2f}")
    print(f"Expenses:          {exp_count:>3d} | Total: ${expense_total:,.2f}")
    print("-" * 48)
    print(f"GRAND TOTAL:             ${grand_total:,.2f}")
    print()

    if maint_by_category:
        print("=== MAINTENANCE BY CATEGORY ===")
        for cat, total in sorted(
            maint_by_category.items(), key=lambda kv: kv[1], reverse=True
        ):
            print(f"- {cat:<20s} ${total:,.2f}")
        print()

    if exp_by_category:
        print("=== EXPENSES BY CATEGORY ===")
        for cat, total in sorted(
            exp_by_category.items(), key=lambda kv: kv[1], reverse=True
        ):
            print(f"- {cat:<20s} ${total:,.2f}")


if __name__ == "__main__":
    main()
