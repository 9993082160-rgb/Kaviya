from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import RedirectResponse


class LoginRequiredMiddleware(BaseHTTPMiddleware):
    PUBLIC_PATHS = {
        "/",
        "/login",
        "/register",
        "/api/login",
        "/api/register",
        "/health",
    }

    async def dispatch(self, request: Request, call_next):
        path = request.url.path

        if (
            path.startswith("/static/")
            or path in self.PUBLIC_PATHS
            or path.startswith("/docs")
            or path.startswith("/openapi")
        ):
            return await call_next(request)

        if request.session.get("user_id") is None:
            if path.startswith("/api/"):
                return await call_next(request)

            return RedirectResponse(
                url="/login",
                status_code=303,
            )

        return await call_next(request)