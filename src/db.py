import os
from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()

MONGODB_URI = os.getenv("MONGODB_URI")
MONGODB_DB = os.getenv("MONGODB_DB", "vehicle_intel")

if not MONGODB_URI:
    raise RuntimeError("MONGODB_URI is not set in .env")

_client = MongoClient(MONGODB_URI)
_db = _client[MONGODB_DB]


def get_db():
    """Return the main application database."""
    return _db


def get_collection(name: str):
    """Helper to get a collection by name."""
    return _db[name]
