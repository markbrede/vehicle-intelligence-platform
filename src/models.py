from datetime import datetime
from typing import Optional, Dict, Any


def vehicle_schema(
    user_id: str,
    year: int,
    make: str,
    model: str,
    vin: Optional[str] = None,
    nickname: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Create the canonical vehicle document I store in MongoDB.
    """
    return {
        "user_id": user_id,  # logical owner (for now just "mark")
        "year": year,
        "make": make,
        "model": model,
        "vin": vin,
        "nickname": nickname,
        "created_at": datetime.utcnow(),
    }
