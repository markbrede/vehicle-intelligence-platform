from __future__ import annotations

from datetime import datetime
from typing import Any, Dict, List, Tuple

from bson import ObjectId

from src.db import get_collection


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

    vehicle_id: ObjectId = vehicle["_id"]

    # --- Monthly totals for maintenance ---
    maintenance_monthly_pipeline = [
        {"$match": {"vehicle_id": vehicle_id}},
        {
            "$group": {
                "_id": {"year": {"$year": "$date"}, "month": {"$month": "$date"}},
                "total": {"$sum": "$cost"},
                "count": {"$sum": 1},
            }
        },
        {"$sort": {"_id.year": 1, "_id.month": 1}},
    ]

    # --- Monthly totals for expenses ---
    expenses_monthly_pipeline = [
        {"$match": {"vehicle_id": vehicle_id}},
        {
            "$group": {
                "_id": {"year": {"$year": "$date"}, "month": {"$month": "$date"}},
                "total": {"$sum": "$amount"},
                "count": {"$sum": 1},
            }
        },
        {"$sort": {"_id.year": 1, "_id.month": 1}},
    ]

    maint_monthly = list(maintenance.aggregate(maintenance_monthly_pipeline))
    exp_monthly = list(expenses.aggregate(expenses_monthly_pipeline))

    # Merge monthly totals (maintenance + expenses) in Python for clean display
    monthly: Dict[str, Dict[str, float]] = {}

    def key(doc: Dict[str, Any]) -> str:
        y = doc["_id"]["year"]
        m = doc["_id"]["month"]
        return f"{y}-{m:02d}"

    for d in maint_monthly:
        k = key(d)
        monthly.setdefault(k, {"maintenance": 0.0, "expenses": 0.0})
        monthly[k]["maintenance"] += float(d["total"])

    for d in exp_monthly:
        k = key(d)
        monthly.setdefault(k, {"maintenance": 0.0, "expenses": 0.0})
        monthly[k]["expenses"] += float(d["total"])

    print("\n=== PIPELINE: MONTHLY TOTALS ===")
    print(
        f"Vehicle: {vehicle.get('year')} {vehicle.get('make')} {vehicle.get('model')} ({vehicle.get('nickname')})"
    )
    print(f"Vehicle _id: {vehicle_id}")
    print()

    cumulative = 0.0
    for month in sorted(monthly.keys()):
        m = monthly[month]["maintenance"]
        e = monthly[month]["expenses"]
        month_total = m + e
        cumulative += month_total
        print(
            f"{month} | Maint: ${m:8.2f} | Exp: ${e:8.2f} | Month: ${month_total:8.2f} | Cumulative: ${cumulative:8.2f}"
        )

    # --- Totals by category (maintenance) ---
    maint_by_cat_pipeline = [
        {"$match": {"vehicle_id": vehicle_id}},
        {
            "$group": {
                "_id": "$category",
                "total": {"$sum": "$cost"},
                "count": {"$sum": 1},
            }
        },
        {"$sort": {"total": -1}},
    ]

    # --- Totals by category (expenses) ---
    exp_by_cat_pipeline = [
        {"$match": {"vehicle_id": vehicle_id}},
        {
            "$group": {
                "_id": "$category",
                "total": {"$sum": "$amount"},
                "count": {"$sum": 1},
            }
        },
        {"$sort": {"total": -1}},
    ]

    maint_by_cat = list(maintenance.aggregate(maint_by_cat_pipeline))
    exp_by_cat = list(expenses.aggregate(exp_by_cat_pipeline))

    print("\n=== PIPELINE: MAINTENANCE BY CATEGORY ===")
    maint_total = 0.0
    for row in maint_by_cat:
        maint_total += float(row["total"])
        print(f"- {row['_id']:<20s} ${float(row['total']):8.2f}  (n={row['count']})")

    print("\n=== PIPELINE: EXPENSES BY CATEGORY ===")
    exp_total = 0.0
    for row in exp_by_cat:
        exp_total += float(row["total"])
        print(f"- {row['_id']:<20s} ${float(row['total']):8.2f}  (n={row['count']})")

    print("\n=== PIPELINE: GRAND TOTALS ===")
    print(f"Maintenance total: ${maint_total:,.2f}")
    print(f"Expenses total:    ${exp_total:,.2f}")
    print(f"Grand total:       ${maint_total + exp_total:,.2f}")


if __name__ == "__main__":
    main()
