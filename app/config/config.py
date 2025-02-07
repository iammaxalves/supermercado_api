# app/config/config.py
from typing import Optional
from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic_settings import BaseSettings
from app.models.admin.role import Role
from app.models.admin.user import User
from app.models.inventory.product import Product
from app.models.inventory.stock import Stock
from app.models.sales.invoice import Invoice
from app.models.sales.order import Order
import bleach
import os


# Classe para carregar configurações do ambiente
class Settings(BaseSettings):
    DATABASE_URL: Optional[str] = None  # URL do banco de dados
    SECRET_KEY: str  # Chave secreta para JWT
    TOKEN_EXPIRE_MINUTES: int  # Tempo de expiração do token
    HMAC_SECRET_KEY: str
    class Config:
        env_file = ".env.dev"  # Indica o arquivo de variáveis de ambiente

# Criar uma instância global para acesso às configurações
settings = Settings()

# Classe para gerenciar a conexão com o banco de dados
class DataBase:
    client: AsyncIOMotorClient = None  # Inicializa o cliente MongoDB como None

# Cria uma instância do banco
db = DataBase()

# Função para obter a conexão com o banco
def get_database() -> AsyncIOMotorClient:
    return db.client

def sanitize_input(user_input: str) -> str:
    """Sanitiza entradas do usuário para evitar XSS."""
    return bleach.clean(user_input)

# Função para iniciar a conexão com o MongoDB e configurar o Beanie
async def initiate_database():
    try:
        db.client = AsyncIOMotorClient(
            settings.DATABASE_URL,
            serverSelectionTimeoutMS=5000,  # Timeout para seleção do servidor
            connectTimeoutMS=10000  # Timeout para conexão
        )  # Conecta ao MongoDB
        
        # Verifica se a conexão está funcionando
        await db.client.server_info()
        
        # Modelos que serão usados no banco
        document_models = [Role, User, Product, Stock, Invoice, Order]
        
        # Inicializa o Beanie com os modelos
        await init_beanie(
            database=db.client.get_default_database(),
            document_models=document_models
        )
        print("Database connection established successfully")
    except Exception as e:
        print(f"Error connecting to database: {str(e)}")
        raise

# Função para fechar a conexão com o banco
def close_mongo_connection():
    if db.client:
        db.client.close()