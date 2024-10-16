from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse
from fastapi import Request
from fast_zero.security import get_current_user


class AuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # Executa algo antes de passar a requisição para a rota
        print("Processando requisição...")

        # Pode acessar cabeçalhos, modificar a requisição ou validar
        token = request.headers.get("Authorization")
        token = token.split(" ")[1]
        if not token:
            return JSONResponse({"error": "Token não encontrado"}, status_code=403)
        
        user = get_current_user(token)
        request.state.user = user

        # Chamando a próxima parte da requisição (a rota correspondente)
        response = await call_next(request)
        return response
