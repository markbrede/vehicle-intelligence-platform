from __future__ import annotations

from src.neo4j_connection import get_driver


def main() -> None:
    driver = get_driver()
    vehicle_nickname = "Project 4Runner"

    with driver.session() as session:
        print("\n=== NEO4J: VEHICLE EVENT TIMELINE (maintenance + expenses) ===")
        result = session.run(
            """
            MATCH (v:Vehicle {nickname: $nickname})

            CALL (v) {
              MATCH (v)-[:HAS_MAINTENANCE]->(m:MaintenanceEvent)
              WHERE m.date IS NOT NULL
              RETURN collect({
                type:"maintenance",
                date:m.date,
                category:m.category,
                amount:m.cost,
                desc:m.description
              }) AS maint
            }

            CALL (v) {
              MATCH (v)-[:HAS_EXPENSE]->(e:Expense)
              WHERE e.date IS NOT NULL
              RETURN collect({
                type:"expense",
                date:e.date,
                category:e.category,
                amount:e.amount,
                desc:e.description
              }) AS exp
            }

            WITH (maint + exp) AS events
            UNWIND events AS ev
            RETURN ev.type AS type, ev.date AS date, ev.category AS category, ev.amount AS amount, ev.desc AS desc
            ORDER BY date ASC
            """,
            nickname=vehicle_nickname,
        )

        rows = list(result)
        for r in rows:
            amt = r["amount"]
            amt_str = f"${amt:,.2f}" if isinstance(amt, (int, float)) else str(amt)
            print(
                f"{r['date']} | {r['type']:<11s} | {r['category']:<15s} | {amt_str:<10s} | {r['desc']}"
            )

        print("\n=== NEO4J: SPEND BY CATEGORY (maintenance + expenses) ===")
        result2 = session.run(
            """
            MATCH (v:Vehicle {nickname: $nickname})

            CALL (v) {
              MATCH (v)-[:HAS_MAINTENANCE]->(m:MaintenanceEvent)
              WHERE m.category IS NOT NULL AND m.cost IS NOT NULL
              RETURN collect({category:m.category, amount: toFloat(m.cost)}) AS maint_items
            }

            CALL (v) {
              MATCH (v)-[:HAS_EXPENSE]->(e:Expense)
              WHERE e.category IS NOT NULL AND e.amount IS NOT NULL
              RETURN collect({category:e.category, amount: toFloat(e.amount)}) AS exp_items
            }

            WITH (maint_items + exp_items) AS items
            UNWIND items AS it
            RETURN it.category AS category, sum(it.amount) AS total
            ORDER BY total DESC
            """,
            nickname=vehicle_nickname,
        )

        for r in result2:
            print(f"- {r['category']:<20s} ${float(r['total']):,.2f}")

        print("\n=== NEO4J: GRAPH SHAPE COUNTS ===")
        result3 = session.run(
            """
            MATCH (v:Vehicle {nickname: $nickname})
            OPTIONAL MATCH (v)-[:HAS_MAINTENANCE]->(m:MaintenanceEvent)
            OPTIONAL MATCH (v)-[:HAS_EXPENSE]->(e:Expense)
            RETURN count(DISTINCT v) AS vehicles,
                   count(DISTINCT m) AS maintenance_events,
                   count(DISTINCT e) AS expenses
            """,
            nickname=vehicle_nickname,
        )
        rec = result3.single()
        if rec:
            print(
                f"vehicles={rec['vehicles']} | maintenance_events={rec['maintenance_events']} | expenses={rec['expenses']}"
            )


if __name__ == "__main__":
    main()
