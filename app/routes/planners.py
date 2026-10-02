import json

from fastapi import APIRouter, Depends, File, Form, Request, UploadFile
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import Recommendation

from ..schemas import (
    HomePlannerRequest,
    JewelryPlannerRequest,
    PartyPlannerRequest,
)
from ..services.gemini_service import generate_recommendation
from ..services.catalog import SHOPPING_CATALOG

router = APIRouter(prefix="/api", tags=["Planners"])


def _require_user_id(request):
    user_id = request.session.get("user_id")

    if not user_id:
        return None

    return int(user_id)


@router.post("/generate-home")
def generate_home(
    data: HomePlannerRequest,
    request: Request,
    db: Session = Depends(get_db),
):
    user_id = _require_user_id(request)

    if not user_id:
        return {
            "success": False,
            "message": "Please login first.",
        }

    input_data = data.model_dump()

    result = generate_recommendation(
        planner_type="home",
        data=input_data,
    )

    recommendation = Recommendation(
        user_id=user_id,
        planner_type="home",
        input_data=json.dumps(input_data),
        result=json.dumps(result),
    )

    db.add(recommendation)
    db.commit()

    return {
        "success": True,
        "planner_type": "home",
        "recommendation": result,
    }


@router.post("/generate-party")
def generate_party(
    data: PartyPlannerRequest,
    request: Request,
    db: Session = Depends(get_db),
):
    user_id = _require_user_id(request)

    if not user_id:
        return {
            "success": False,
            "message": "Please login first.",
        }

    input_data = data.model_dump()

    result = generate_recommendation(
        planner_type="party",
        data=input_data,
    )

    recommendation = Recommendation(
        user_id=user_id,
        planner_type="party",
        input_data=json.dumps(input_data),
        result=json.dumps(result),
    )

    db.add(recommendation)
    db.commit()

    return {
        "success": True,
        "planner_type": "party",
        "recommendation": result,
    }


@router.post("/generate-jewelry")
async def generate_jewelry(
    request: Request,
    budget: float = Form(...),
    occasion: str = Form(...),
    jewelry_type: str = Form(...),
    metal: str = Form(""),
    image: UploadFile | None = File(None),
    db: Session = Depends(get_db),
):
    user_id = _require_user_id(request)

    if not user_id:
        return {
            "success": False,
            "message": "Please login first.",
        }

    image_bytes = None
    image_mime_type = None

    if image:
        image_bytes = await image.read()
        image_mime_type = image.content_type

    input_data = {
        "budget": budget,
        "occasion": occasion,
        "jewelry_type": jewelry_type,
        "metal": metal,
        "has_image": bool(image_bytes),
    }

    result = generate_recommendation(
        planner_type="jewelry",
        data=input_data,
        image_bytes=image_bytes,
        image_mime_type=image_mime_type,
    )

    recommendation = Recommendation(
        user_id=user_id,
        planner_type="jewelry",
        input_data=json.dumps(input_data),
        result=json.dumps(result),
    )

    db.add(recommendation)
    db.commit()

    return {
        "success": True,
        "planner_type": "jewelry",
        "recommendation": result,
    }
@router.post("/shopping")
def shopping(
    request: Request,
    category: str,
    budget: float,
    platform: str = "",
):
    category = category.lower().strip()
    platform = platform.lower().strip()

    matches = [
        item
        for item in SHOPPING_CATALOG
        if item["price"] <= budget
        and (
            not category
            or category in item["category"].lower()
            or category in item["name"].lower()
        )
        and (
            not platform
            or platform == item["platform"].lower()
        )
    ]

    return {
        "success": True,
        "items": matches,
        "budget": budget,
    }