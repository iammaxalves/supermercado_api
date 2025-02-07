from fastapi import FastAPI, Depends, Security, HTTPException
from starlette.requests import Request 
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware
from fastapi.security import APIKeyHeader
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.openapi.utils import get_openapi
import secrets

from app.config.config import settings, initiate_database, close_mongo_connection
from app.middleware.auth import get_current_user
from app.middleware.csrf import CSRFMiddleware
from app.middleware.security import SecurityHeadersMiddleware, RateLimitMiddleware
from app.middleware.logging import add_security_headers, limiter

from app.utils.hmac_utils import generate_hmac
from app.routes.admin.gateway import router as gateway_router
from app.routes.admin.role import router as RoleRouter
from app.routes.admin.user import router as UserRouter
from app.routes.inventory.product import router as ProductRouter
from app.routes.inventory.stock import router as StockRouter
from app.routes.sales.invoice import router as InvoiceRouter
from app.routes.sales.order import router as OrderRouter

# Define o cabeçalho CSRF no Swagger
csrf_security = APIKeyHeader(name="X-CSRF-Token", auto_error=False)

app = FastAPI(
    title="Supermercado API",
    description="API para gerenciamento de usuários e permissões no supermercado",
    version="1.0.0",
    openapi_tags=[
        {"name": "Users", "description": "Operações relacionadas a usuários"},
        {"name": "Products", "description": "Gerenciamento de produtos"},
    ],
    dependencies=[Security(csrf_security)]
)

# Lista de rotas isentas de CSRF
exempt_routes = [
    "/api/users/login",
    "/api/users/register",
    "/docs",
    "/redoc",
    "/openapi.json"
]

# 1. Session Middleware (DEVE SER O PRIMEIRO)
app.add_middleware(
    SessionMiddleware,
    secret_key=settings.SECRET_KEY,
    session_cookie="session_id",
    max_age=86400,  # 24 horas
    same_site="lax",
    https_only=False  # Mude para True em produção
)

# 2. CORS (DEVE VIR ANTES DO CSRF)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*", "X-CSRF-Token"],
    expose_headers=["X-CSRF-Token"]
)

# 3. CSRF Middleware
app.add_middleware(
    CSRFMiddleware,
    secret_key=settings.SECRET_KEY,
    exempt_routes=exempt_routes
)

# Rota de teste para verificar o CSRF
@app.get("/api/csrf-token")
async def get_csrf_token(request: Request):
    if "csrf_token" not in request.session:
        request.session["csrf_token"] = secrets.token_urlsafe(32)
    
    return {
        "csrf_token": request.session["csrf_token"]
    }

# Modified test session route with error handling
@app.get("/test-session")
async def test_session(request: Request):
    try:
        if "csrf_token" not in request.session:
            request.session["csrf_token"] = secrets.token_urlsafe(32)
        
        session_data = dict(request.session)
        return {
            "session": session_data,
            "csrf_token": session_data.get("csrf_token")
        }
    except AssertionError as e:
        return {"error": "Session middleware not properly initialized", "details": str(e)}
    except Exception as e:
        return {"error": "Unexpected error", "details": str(e)}

@app.post("/send-message/")
async def send_message(message: str):
    # Gera o HMAC da mensagem
    hmac_generated = generate_hmac(message)
    
    # Aqui você faria a verificação, por exemplo, com outro sistema
    return {"message": message, "hmac": hmac_generated}

# Inicia e finaliza o banco de dados
@app.on_event("startup")
async def start_database():
    await initiate_database()

@app.on_event("shutdown")
async def shutdown_event():
    close_mongo_connection()

# Rota raiz
@app.get("/", tags=["Root"])
async def read_root():
    return {"message": "Welcome to the Supermarket API!"}

# Teste de sessão com geração de CSRF token
@app.get("/test-session")
async def test_session(request: Request):
    # Gera um novo token CSRF se não existir
    if "csrf_token" not in request.session:
        request.session["csrf_token"] = secrets.token_urlsafe(32)
    
    # Retorna detalhes da sessão para debug
    session_data = dict(request.session)
    print("Session Data:", session_data)
    
    return {
        "session": session_data,
        "csrf_token": session_data.get("csrf_token")
    }

@app.get("/docs", include_in_schema=False)
async def custom_swagger_ui_html(request: Request):
    # Garante que um token CSRF esteja presente na sessão
    if "csrf_token" not in request.session:
        request.session["csrf_token"] = secrets.token_urlsafe(32)
    
    return get_swagger_ui_html(
        openapi_url="/openapi.json",
        title="Supermercado API Docs",
        swagger_ui_parameters={"persistAuthorization": True}
    )

@app.get("/openapi.json", include_in_schema=False)
async def get_open_api_endpoint():
    return get_openapi(title="Supermercado API", version="1.0.0", routes=app.routes)

# Registro das Rotas
app.include_router(UserRouter, prefix="/api/users", tags=["Users"])
app.include_router(RoleRouter, prefix="/api/roles", tags=["Roles"], dependencies=[Depends(get_current_user)])
app.include_router(ProductRouter, prefix="/api/products", tags=["Products"], dependencies=[Depends(get_current_user)])
app.include_router(StockRouter, prefix="/api/stocks", tags=["Stocks"], dependencies=[Depends(get_current_user)])
app.include_router(InvoiceRouter, prefix="/api/invoices", tags=["Invoices"], dependencies=[Depends(get_current_user)])
app.include_router(OrderRouter, prefix="/api/orders", tags=["Orders"], dependencies=[Depends(get_current_user)])
app.include_router(gateway_router, prefix="/api/gateway", tags=["Gateway"], dependencies=[Depends(get_current_user)])
