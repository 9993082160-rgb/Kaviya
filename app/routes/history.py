import json

from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import Recommendation


router = APIRouter(prefix="/api", tags=["History"])


@router.get("/history")
def get_history(
    request: Request,
    db: Session = Depends(get_db),
):
    user_id = request.session.get("user_id")

    if not user_id:
        return {
            "success": False,
            "message": "Please login first.",
            "items": [],
        }

    records = (
        db.query(Recommendation)
        .filter(Recommendation.user_id == int(user_id))
        .order_by(Recommendation.created_at.desc())
        .all()
    )

    items = []

    for record in records:
        try:
            result = json.loads(record.result)
        except json.JSONDecodeError:
            result = record.result

        items.append(
            {
                "id": record.id,
                "planner_type": record.planner_type,
                "input_data": json.loads(record.input_data),
                "result": result,
                "created_at": record.created_at.isoformat(),
            }
        )

    return {
        "success": True,
        "items": items,
    }