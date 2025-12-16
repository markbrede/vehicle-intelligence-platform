from __future__ import annotations

from src.neo4j_connection import get_driver


def main() -> None:
    driver = get_driver()
    with driver.session() as session:
        result = session.run("RETURN 1 AS ok")
        record = result.single()

        if record is None:
            raise RuntimeError("Neo4j query returned no record")

        print("Neo4j connection test:", record["ok"])


if __name__ == "__main__":
    main()
