# app/middleware/logging.py
from fastapi import Request
from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)

async def add_security_headers(request: Request, call_next):
    response = await call_next(request)
    
    # CSP mais permissiva que permite o Swagger funcionar
    csp = (
        "default-src 'self'; "
        "script-src 'self' 'unsafe-inline' 'unsafe-eval' cdn.jsdelivr.net unpkg.com; "
        "style-src 'self' 'unsafe-inline' cdn.jsdelivr.net unpkg.com; "
        "img-src 'self' data: validator.swagger.io fastapi.tiangolo.com; "
        "font-src 'self' data:; "
        "connect-src 'self'"
    )

    
    # Adiciona cabeçalhos de segurança
    response.headers["Content-Security-Policy"] = csp
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    
    return response