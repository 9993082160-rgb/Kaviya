from typing import Any

from pydantic import BaseModel, EmailStr, Field


class RegisterRequest(BaseModel):
    name: str = Field(min_length=2, max_length=100)
    email: EmailStr
    password: str = Field(min_length=6, max_length=100)


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class HomePlannerRequest(BaseModel):
    budget: float = Field(gt=0)
    room_type: str
    style: str
    location: str = ""


class PartyPlannerRequest(BaseModel):
    budget: float = Field(gt=0)
    event_type: str
    guests: int = Field(gt=0)
    location: str = ""


class JewelryPlannerRequest(BaseModel):
    budget: float = Field(gt=0)
    occasion: str
    jewelry_type: str
    metal: str = ""


class RecommendationResponse(BaseModel):
    success: bool
    planner_type: str
    recommendation: Any