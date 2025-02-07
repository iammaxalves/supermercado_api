import secrets
from typing import List
from fastapi import FastAPI, Request, Response, HTTPException, status
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.middleware.sessions import SessionMiddleware

class CSRFMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, secret_key: str, exempt_routes: List[str] = None):
        super().__init__(app)
        self.secret_key = secret_key
        self.exempt_routes = set(exempt_routes or [])

    async def dispatch(self, request: Request, call_next):
        # Se a rota estiver na lista de isenção, pula a verificação CSRF
        if request.url.path in self.exempt_routes:
            return await call_next(request)

        # Métodos seguros (não modificam o estado do servidor)
        if request.method in ("GET", "HEAD", "OPTIONS"):
            return await call_next(request)


        # Chama a próxima etapa do request
        response = await call_next(request)

        # Gera um novo token CSRF para a próxima requisição
        new_token = generate_csrf_token(request.session)

        # Adiciona o novo token no cabeçalho da resposta
        response.headers["X-CSRF-Token"] = new_token

        return response

def generate_csrf_token(session: dict) -> str:
    """Gera um novo token CSRF e armazena na sessão"""
    token = secrets.token_urlsafe(32)
    session["csrf_token"] = token
    return token

# Criando a aplicação FastAPI
app = FastAPI()

# Adiciona suporte a sessão (necessário para armazenar o CSRF na sessão do usuário)
app.add_middleware(SessionMiddleware, secret_key="sua-chave-secreta")

# Adiciona o middleware CSRF
app.add_middleware(
    CSRFMiddleware,
    secret_key="sua-chave-secreta",
    exempt_routes=["/login", "/register"]  # Exemplo de rotas isentas de CSRF
)

# Rota de teste para obter o token CSRF
@app.get("/get-csrf-token")
async def get_csrf_token(request: Request):
    csrf_token = request.session.get("csrf_token")
    if not csrf_token:
        csrf_token = generate_csrf_token(request.session)
    return {"csrf_token": csrf_token}

# Rota protegida por CSRF
@app.post("/submit")
async def submit_data(request: Request):
    return {"message": "Dados enviados com sucesso!"}
