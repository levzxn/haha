from fastapi.responses import JSONResponse
from tortoise.transactions import in_transaction
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from authentication_microservice.security import get_current_user

class TransactionMiddleware(BaseHTTPMiddleware):
    async def dispatch(self,request: Request, call_next):
        async with in_transaction() as connection:
            request.state.connection = connection  
            response = await call_next(request)
            return response

class DeleteRequestMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        if request.method in ("DELETE","PUT","PATCH"):
            token = request.headers.get("Authorization")
            token = token.split(" ")[1]
            if not token:
                return JSONResponse({"error": "Token não encontrado"}, status_code=403)
            user = await get_current_user(token)
            request.state.user = user
           
        response = await call_next(request)
        return response
