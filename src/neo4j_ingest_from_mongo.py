from __future__ import annotations

from datetime import datetime
from typing import Any, Dict, List, Optional

from bson import ObjectId

from src.db import get_collection
from src.neo4j_connection import get_driver


def _iso(dt: Any) -> Optional[str]:
    # Mongo stores datetimes as BSON datetime -> comes back as Python datetime
    if isinstance(dt, datetime):
        # store as ISO string for easy display/filtering in Neo4j
        return dt.replace(microsecond=0).isoformat()
    return None


def main() -> None:
    user_id = "mark"
    nickname = "Project 4Runner"

    vehicles_col = get_collection("vehicles")
    maint_col = get_collection("maintenance_events")
    exp_col = get_collection("expenses")

    vehicle = vehicles_col.find_one({"user_id": user_id, "nickname": nickname})
    if not vehicle:
        print(f"Vehicle not found for user_id={user_id}, nickname={nickname}")
        return

    vehicle_id: ObjectId = vehicle["_id"]

    # Pull related docs
    maint_docs: List[Dict[str, Any]] = list(
        maint_col.find({"vehicle_id": vehicle_id}).sort("date", 1)
    )
    exp_docs: List[Dict[str, Any]] = list(
        exp_col.find({"vehicle_id": vehicle_id}).sort("date", 1)
    )

    driver = get_driver()

    with driver.session() as session:
        # Vehicle node
        session.run(
            """
            MERGE (v:Vehicle {vehicle_id: $vehicle_id})
            SET v.user_id = $user_id,
                v.year = $year,
                v.make = $make,
                v.model = $model,
                v.nickname = $nickname
            """,
            vehicle_id=str(vehicle_id),
            user_id=vehicle.get("user_id"),
            year=vehicle.get("year"),
            make=vehicle.get("make"),
            model=vehicle.get("model"),
            ts_nickname=vehicle.get("nickname"),
            nickname=vehicle.get("nickname"),
        )

        # Maintenance events
        for d in maint_docs:
            event_id = str(d["_id"])
            session.run(
                """
                MERGE (m:MaintenanceEvent {event_id: $event_id})
                SET m.user_id = $user_id,
                    m.date = $date,
                    m.odometer = $odometer,
                    m.category = $category,
                    m.description = $description,
                    m.cost = $cost,
                    m.vendor = $vendor,
                    m.notes = $notes
                WITH m
                MATCH (v:Vehicle {vehicle_id: $vehicle_id})
                MERGE (v)-[:HAS_MAINTENANCE]->(m)
                """,
                event_id=event_id,
                vehicle_id=str(vehicle_id),
                user_id=d.get("user_id"),
                date=_iso(d.get("date")),
                odometer=d.get("odometer"),
                category=d.get("category"),
                description=d.get("description"),
                cost=float(d.get("cost", 0.0)),
                vendor=d.get("vendor"),
                notes=d.get("notes"),
            )

        # Expense events
        for d in exp_docs:
            event_id = str(d["_id"])
            session.run(
                """
                MERGE (e:Expense {event_id: $event_id})
                SET e.user_id = $user_id,
                    e.date = $date,
                    e.odometer = $odometer,
                    e.category = $category,
                    e.amount = $amount,
                    e.vendor = $vendor,
                    e.description = $description
                WITH e
                MATCH (v:Vehicle {vehicle_id: $vehicle_id})
                MERGE (v)-[:HAS_EXPENSE]->(e)
                """,
                event_id=event_id,
                vehicle_id=str(vehicle_id),
                user_id=d.get("user_id"),
                date=_iso(d.get("date")),
                odometer=d.get("odometer"),
                category=d.get("category"),
                amount=float(d.get("amount", 0.0)),
                vendor=d.get("vendor"),
                description=d.get("description"),
            )

        # Quick counts to confirm ingest
        res = session.run(
            """
            MATCH (v:Vehicle {vehicle_id: $vehicle_id})
            OPTIONAL MATCH (v)-[:HAS_MAINTENANCE]->(m:MaintenanceEvent)
            OPTIONAL MATCH (v)-[:HAS_EXPENSE]->(e:Expense)
            RETURN v.nickname AS nickname,
                   count(DISTINCT m) AS maintenance_count,
                   count(DISTINCT e) AS expense_count
            """,
            vehicle_id=str(vehicle_id),
        )
        record = res.single()
        if record:
            print("Neo4j ingest complete.")
            print(
                f"Vehicle: {record['nickname']} | maintenance={record['maintenance_count']} | expenses={record['expense_count']}"
            )
        else:
            print("Neo4j ingest complete, but did not find vehicle node back.")

    # Optional: driver.close() if you want, but leaving open is fine for a CLI script.


if __name__ == "__main__":
    main()
