import json
from typing import Any

from google import genai

from ..config import settings
from .catalog import (
    HOME_CATALOG,
    JEWELRY_CATALOG,
    PARTY_CATALOG,
    SHOPPING_CATALOG,
)

def _fallback(planner_type: str, data: dict[str, Any]) -> dict[str, Any]:
    budget = float(data.get("budget", 0))

    if planner_type == "home":
        catalog = HOME_CATALOG
        requested_style = data.get("style", "").lower()

        matches = [
            item
            for item in catalog
            if item["min_budget"] <= budget <= item["max_budget"]
            and (
                not requested_style
                or requested_style in item["style"].lower()
            )
        ]

        if not matches:
            matches = [
                item
                for item in catalog
                if item["min_budget"] <= budget <= item["max_budget"]
            ]

    elif planner_type == "party":
        catalog = PARTY_CATALOG
        event_type = data.get("event_type", "").lower()

        matches = [
            item
            for item in catalog
            if item["min_budget"] <= budget <= item["max_budget"]
            and (
                not event_type
                or event_type in item["event_type"].lower()
            )
        ]

        if not matches:
            matches = [
                item
                for item in catalog
                if item["min_budget"] <= budget <= item["max_budget"]
            ]

    else:
        catalog = JEWELRY_CATALOG
        jewelry_type = data.get("jewelry_type", "").lower()
        metal = data.get("metal", "").lower()

        matches = [
            item
            for item in catalog
            if item["min_budget"] <= budget <= item["max_budget"]
            and (
                not jewelry_type
                or jewelry_type in item["jewelry_type"].lower()
            )
            and (
                not metal
                or metal in item["metal"].lower()
            )
        ]

        if not matches:
            matches = [
                item
                for item in catalog
                if item["min_budget"] <= budget <= item["max_budget"]
            ]

    if not matches:
        matches = catalog[:1]

    return {
        "source": "local_fallback",
        "message": (
            "Gemini is not configured or unavailable. "
            "Here is a budget-based recommendation from the "
            "PocketSmart catalog."
        ),
        "items": matches,
        "budget": budget,
    }


def _gemini_client():
    if not settings.gemini_api_key:
        return None

    return genai.Client(
        api_key=settings.gemini_api_key,
    )


def generate_recommendation(
    planner_type: str,
    data: dict[str, Any],
    image_bytes: bytes | None = None,
    image_mime_type: str | None = None,
) -> dict[str, Any]:

    client = _gemini_client()

    if client is None:
        return _fallback(planner_type, data)

    prompt = f"""
You are PocketSmart AI, a smart budget and recommendation assistant.

Planner type:
{planner_type}

User data:
{json.dumps(data, indent=2)}

Give practical recommendations that respect the user's budget.

Return valid JSON with this structure:

{{
    "summary": "short recommendation summary",
    "budget": number,
    "recommendations": [
        {{
            "name": "item name",
            "category": "category",
            "estimated_cost": number,
            "reason": "why it fits"
        }}
    ],
    "tips": [
        "budget saving tip"
    ]
}}

Do not include markdown fences.
"""

    try:
        contents: list[Any] = [prompt]

        if image_bytes and image_mime_type:
            contents.append(
                {
                    "mime_type": image_mime_type,
                    "data": image_bytes,
                }
            )

        response = client.models.generate_content(
            model=settings.gemini_model,
            contents=contents,
        )

        text = (response.text or "").strip()

        if text.startswith("```"):
            text = text.replace("```json", "")
            text = text.replace("```", "")
            text = text.strip()

        result = json.loads(text)

        return {
            "source": "gemini",
            **result,
        }

    except Exception:
        return _fallback(planner_type, data)