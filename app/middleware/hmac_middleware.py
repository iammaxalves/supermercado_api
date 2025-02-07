from fastapi import Request, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware
from app.utils.hmac_utils import generate_hmac

class HMACMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        """
        Middleware para validar HMAC nas requisições.
        """
        # Obtém o HMAC do cabeçalho da requisição
        received_hmac = request.headers.get("X-HMAC-Signature")
        
        if not received_hmac:
            raise HTTPException(status_code=403, detail="HMAC Signature missing")

        # Criamos a mensagem com base no método e URL da requisição
        message = f"{request.method} {request.url.path}"

        # Geramos o HMAC esperado
        expected_hmac = generate_hmac(message)

        # Comparação segura dos HMACs
        if not hmac.compare_digest(received_hmac, expected_hmac):
            raise HTTPException(status_code=403, detail="Invalid HMAC Signature")

        return await call_next(request)
