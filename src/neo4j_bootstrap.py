from __future__ import annotations

from src.neo4j_connection import get_driver

from typing import LiteralString


CONSTRAINTS: list[LiteralString] = [
    "CREATE CONSTRAINT vehicle_id IF NOT EXISTS FOR (v:Vehicle) REQUIRE v.vehicle_id IS UNIQUE",
    "CREATE CONSTRAINT maintenance_id IF NOT EXISTS FOR (m:MaintenanceEvent) REQUIRE m.event_id IS UNIQUE",
    "CREATE CONSTRAINT expense_id IF NOT EXISTS FOR (e:Expense) REQUIRE e.event_id IS UNIQUE",
    "CREATE INDEX vehicle_user_id IF NOT EXISTS FOR (v:Vehicle) ON (v.user_id)",
    "CREATE INDEX maintenance_category IF NOT EXISTS FOR (m:MaintenanceEvent) ON (m.category)",
    "CREATE INDEX expense_category IF NOT EXISTS FOR (e:Expense) ON (e.category)",
]



def main() -> None:
    driver = get_driver()
    with driver.session() as session:
        # wipe all nodes/relationships so you can re-run ingestion cleanly
        session.run("MATCH (n) DETACH DELETE n")

        for q in CONSTRAINTS:
            session.run(q)

    print("Neo4j bootstrap complete: cleared graph, ensured constraints/indexes.")


if __name__ == "__main__":
    main()
