from __future__ import annotations

import os
from dotenv import load_dotenv
from neo4j import GraphDatabase, Driver

load_dotenv()

NEO4J_URI_RAW = os.getenv("NEO4J_URI")
NEO4J_USER_RAW = os.getenv("NEO4J_USER")
NEO4J_PASSWORD_RAW = os.getenv("NEO4J_PASSWORD")

if not NEO4J_URI_RAW or not NEO4J_USER_RAW or not NEO4J_PASSWORD_RAW:
    raise RuntimeError("Neo4j environment variables not set")

# Type-narrowed (now guaranteed to be str)
NEO4J_URI: str = NEO4J_URI_RAW
NEO4J_USER: str = NEO4J_USER_RAW
NEO4J_PASSWORD: str = NEO4J_PASSWORD_RAW

_driver: Driver = GraphDatabase.driver(
    NEO4J_URI,
    auth=(NEO4J_USER, NEO4J_PASSWORD),
)


def get_driver() -> Driver:
    return _driver
