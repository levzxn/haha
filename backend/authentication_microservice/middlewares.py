from tortoise.transactions import in_transaction
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware

class TransactionMiddleware(BaseHTTPMiddleware):
    async def dispatch(self,request: Request, call_next):
        async with in_transaction() as connection:
            request.state.db_connection = connection  
            response = await call_next(request)
            return response
