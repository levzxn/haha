from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse
from fastapi import Request,HTTPException
from DOEMApi.security import get_current_user
from http import HTTPStatus


class AuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        token = request.headers.get("Authorization")
        token = token.split(" ")[1]
        if not token:
            return JSONResponse({"error": "Token não encontrado"}, status_code=403)
        user = get_current_user(token)
        request.state.user = user
        response = await call_next(request)
        return response
