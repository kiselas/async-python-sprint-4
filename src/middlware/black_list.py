from fastapi import Request, status
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.types import ASGIApp


class BlackListMiddleware(BaseHTTPMiddleware):
    def __init__(
            self,
            app: ASGIApp,
            black_list: list,
    ) -> None:
        super().__init__(app)
        self.black_list: list = black_list

    async def dispatch(self, request: Request, call_next):
        ip: str = request.headers.get("X-REAL-IP")
        if ip in self.black_list:
            return JSONResponse(
                {"error": "Access denied"},
                status_code=status.HTTP_403_FORBIDDEN,
            )

        response = await call_next(request)

        return response
