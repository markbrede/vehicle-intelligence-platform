from datetime import datetime
from typing import Optional, Dict, Any
from bson import ObjectId


def vehicle_schema(
    user_id: str,
    year: int,
    make: str,
    model: str,
    vin: Optional[str] = None,
    nickname: Optional[str] = None,
) -> Dict[str, Any]:
    """The vehicle schema document to store in mongo."""
    return {
        "user_id": user_id,  # logical owner (for now just "mark")
        "year": year,
        "make": make,
        "model": model,
        "vin": vin,
        "nickname": nickname,
        "created_at": datetime.utcnow(),
    }


def maintenance_event_schema(
    user_id: str,
    vehicle_id: Any,           # expect this to be the _id from the vehicles collection
    date: datetime,
    odometer: Optional[int],
    category: str,             # like "Oil Change", "Brakes", "Inspection"
    description: str,
    cost: float,
    vendor: Optional[str] = None,
    notes: Optional[str] = None,
) -> Dict[str, Any]:
    """The maintenance event schema to store in mongo."""
    return {
        "user_id": user_id,
        "vehicle_id": vehicle_id,
        "date": date,
        "odometer": odometer,
        "category": category,
        "description": description,
        "cost": cost,
        "vendor": vendor,
        "notes": notes,
        "created_at": datetime.utcnow(),
    }

def expense_schema(
    user_id: str,
    vehicle_id: ObjectId,
    date: datetime,
    category: str,
    amount: float,
    vendor: Optional[str] = None,
    description: Optional[str] = None,
    odometer: Optional[int] = None,
) -> Dict[str, Any]:
    """The expense event schema to store in mongo."""
    return {
        "user_id": user_id,
        "vehicle_id": vehicle_id,
        "date": date,
        "category": category,       # Like "Fuel", "Insurance", "Registration"
        "amount": amount,
        "vendor": vendor,
        "description": description,
        "odometer": odometer,
        "created_at": datetime.utcnow(),
    }
