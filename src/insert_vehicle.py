from src.db import get_collection
from src.models import vehicle_schema

def main():
    vehicles = get_collection("vehicles")

    vehicle = vehicle_schema(
        user_id="mark",
        year=2004,
        make="Toyota",
        model="4Runner V8",
        vin=None,
        nickname="Project 4Runner"
    )

    result = vehicles.insert_one(vehicle)
    print("Inserted vehicle with ID:", result.inserted_id)

if __name__ == "__main__":
    main()
