from datetime import datetime
from src.db import get_collection

def main() -> None:
    vehicles = get_collection("vehicles")

    # Missing required fields like year/make/model -> should fail validation
    bad_vehicle = {
        "user_id": "mark",
        "nickname": "Bad Vehicle",
        "created_at": datetime.utcnow(),
    }

    try:
        vehicles.insert_one(bad_vehicle)
        print("UNEXPECTED: insert succeeded (validator not enforcing?)")
    except Exception as e:
        print("Expected validation failure:")
        print(type(e).__name__, e)

if __name__ == "__main__":
    main()
