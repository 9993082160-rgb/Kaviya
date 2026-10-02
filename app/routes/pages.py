from pathlib import Path

from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates


BASE_DIR = Path(__file__).resolve().parents[2]

templates = Jinja2Templates(
    directory=str(BASE_DIR / "templates")
)

router = APIRouter()


@router.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={},
    )


@router.get("/register", response_class=HTMLResponse)
async def register_page(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="register.html",
        context={},
    )


@router.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="login.html",
        context={},
    )


@router.get("/dashboard", response_class=HTMLResponse)
async def dashboard_page(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="dashboard.html",
        context={},
    )


@router.get("/home-planner", response_class=HTMLResponse)
async def home_planner_page(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="home_planner.html",
        context={},
    )


@router.get("/party-planner", response_class=HTMLResponse)
async def party_planner_page(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="party_planner.html",
        context={},
    )


@router.get("/jewelry-planner", response_class=HTMLResponse)
async def jewelry_planner_page(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="jewelry_planner.html",
        context={},
    )
@router.get("/shopping", response_class=HTMLResponse)
async def shopping_page(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="shopping.html",
        context={},
    )

@router.get("/history", response_class=HTMLResponse)
async def history_page(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="history.html",
        context={},
    )
    