from __future__ import annotations

from pymongo.collection import Collection

from src.db import get_collection


def ensure_indexes(col: Collection, specs: list[tuple[str, int]], name: str) -> None:
    col.create_index(specs, name=name)
    print(f"Ensured index on {col.name}: {name} {specs}")


def main() -> None:
    vehicles = get_collection("vehicles")
    maintenance = get_collection("maintenance_events")
    expenses = get_collection("expenses")

    # Find vehicle by (user_id, nickname)
    ensure_indexes(vehicles, [("user_id", 1), ("nickname", 1)], "user_nickname")

    # Timeline queries are per vehicle by date
    ensure_indexes(maintenance, [("vehicle_id", 1), ("date", -1)], "vehicle_date_desc")
    ensure_indexes(expenses, [("vehicle_id", 1), ("date", -1)], "vehicle_date_desc")

    # Category rollups are totals by category per vehicle
    ensure_indexes(
        maintenance, [("vehicle_id", 1), ("category", 1)], "vehicle_category"
    )
    ensure_indexes(expenses, [("vehicle_id", 1), ("category", 1)], "vehicle_category")

    print("Done.")


if __name__ == "__main__":
    main()
