from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlalchemy.orm import Session

from ..auth import authenticate_user, create_user, get_user_by_email
from ..database import get_db
from ..schemas import LoginRequest, RegisterRequest


router = APIRouter(prefix="/api", tags=["Authentication"])


@router.post("/register")
def register(
    data: RegisterRequest,
    request: Request,
    db: Session = Depends(get_db),
):
    existing_user = get_user_by_email(db, data.email)

    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Email is already registered.",
        )

    user = create_user(
        db=db,
        name=data.name,
        email=data.email,
        password=data.password,
    )

    request.session["user_id"] = user.id
    request.session["user_name"] = user.name
    request.session["user_email"] = user.email

    return {
        "success": True,
        "message": "Registration successful.",
        "user": {
            "id": user.id,
            "name": user.name,
            "email": user.email,
        },
    }


@router.post("/login")
def login(
    data: LoginRequest,
    request: Request,
    db: Session = Depends(get_db),
):
    user = authenticate_user(
        db=db,
        email=data.email,
        password=data.password,
    )

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password.",
        )

    request.session["user_id"] = user.id
    request.session["user_name"] = user.name
    request.session["user_email"] = user.email

    return {
        "success": True,
        "message": "Login successful.",
        "user": {
            "id": user.id,
            "name": user.name,
            "email": user.email,
        },
    }


@router.post("/logout")
def logout(request: Request):
    request.session.clear()

    return {
        "success": True,
        "message": "Logged out successfully.",
    }