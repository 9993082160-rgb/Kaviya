from pathlib import Path

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from starlette.middleware.sessions import SessionMiddleware

from .config import settings
from .database import Base, engine
from .middleware import LoginRequiredMiddleware

from .routes import auth
from .routes import history
from .routes import pages
from .routes import planners


BASE_DIR = Path(__file__).resolve().parent.parent


Base.metadata.create_all(bind=engine)


app = FastAPI(
    title="PocketSmart AI",
    description="Smart Budget & Recommendation Assistant",
    version="1.0.0",
)


app.add_middleware(LoginRequiredMiddleware)

app.add_middleware(
    SessionMiddleware,
    secret_key=settings.session_secret,
    https_only=settings.cookie_secure,
    same_site="lax",
)

app.mount(
    "/static",
    StaticFiles(directory=str(BASE_DIR / "static")),
    name="static",
)


app.include_router(pages.router)
app.include_router(auth.router)
app.include_router(planners.router)
app.include_router(history.router)


@app.get("/health")
def health():
    return {
        "status": "ok",
        "app": "PocketSmart AI",
    }