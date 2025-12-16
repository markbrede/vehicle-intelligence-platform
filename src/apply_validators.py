from __future__ import annotations

from src.db import get_db

def apply_validator(collection: str, validator: dict) -> None:
    db = get_db()

    cmd = {
        "collMod": collection,
        "validator": validator,
        "validationLevel": "moderate",  # enforce on inserts/updates, but allow existing docs
        "validationAction": "error",  # reject invalid writes
    }

    result = db.command(cmd)
    print(f"Applied validator to {collection}: ok={result.get('ok')}")

    # Print summary if present
    if "warnings" in result:
        print("warnings:", result["warnings"])


def main() -> None:
    # VEHICLES
    vehicles_validator = {
        "$jsonSchema": {
            "bsonType": "object",
            "required": ["user_id", "year", "make", "model", "created_at"],
            "properties": {
                "user_id": {"bsonType": "string", "minLength": 1},
                "year": {"bsonType": "int", "minimum": 1886, "maximum": 2100},
                "make": {"bsonType": "string", "minLength": 1},
                "model": {"bsonType": "string", "minLength": 1},
                "vin": {"bsonType": ["string", "null"]},
                "nickname": {"bsonType": ["string", "null"]},
                "created_at": {"bsonType": "date"},
            },
            "additionalProperties": True,
        }
    }

    # MAINTENANCE EVENTS
    maintenance_validator = {
        "$jsonSchema": {
            "bsonType": "object",
            "required": [
                "user_id",
                "vehicle_id",
                "date",
                "category",
                "description",
                "cost",
                "created_at",
            ],
            "properties": {
                "user_id": {"bsonType": "string", "minLength": 1},
                "vehicle_id": {"bsonType": "objectId"},
                "date": {"bsonType": "date"},
                "odometer": {"bsonType": ["int", "null"], "minimum": 0},
                "category": {"bsonType": "string", "minLength": 1},
                "description": {"bsonType": "string", "minLength": 1},
                "cost": {"bsonType": "double", "minimum": 0},
                "vendor": {"bsonType": ["string", "null"]},
                "notes": {"bsonType": ["string", "null"]},
                "created_at": {"bsonType": "date"},
            },
            "additionalProperties": True,
        }
    }

    # EXPENSES
    expenses_validator = {
        "$jsonSchema": {
            "bsonType": "object",
            "required": [
                "user_id",
                "vehicle_id",
                "date",
                "category",
                "amount",
                "created_at",
            ],
            "properties": {
                "user_id": {"bsonType": "string", "minLength": 1},
                "vehicle_id": {"bsonType": "objectId"},
                "date": {"bsonType": "date"},
                "category": {"bsonType": "string", "minLength": 1},
                "amount": {"bsonType": "double", "minimum": 0},
                "vendor": {"bsonType": ["string", "null"]},
                "description": {"bsonType": ["string", "null"]},
                "odometer": {"bsonType": ["int", "null"], "minimum": 0},
                "created_at": {"bsonType": "date"},
            },
            "additionalProperties": True,
        }
    }

    apply_validator("vehicles", vehicles_validator)
    apply_validator("maintenance_events", maintenance_validator)
    apply_validator("expenses", expenses_validator)

    print("Done.")


if __name__ == "__main__":
    main()
