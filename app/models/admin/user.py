from beanie import Document
from pydantic import Field, EmailStr
from datetime import datetime

class User(Document):
    username: str = Field(..., max_length=100, unique=True)  # Nome de usuário
    password: str = Field(..., min_length=8)  # Senha do usuário
    email: EmailStr = Field(..., unique=True)  # Email do usuário
    full_name: str = Field(..., max_length=200)  # Nome completo
    is_admin: bool = Field(default=False)  # Se é administrador
    is_active: bool = True 
    created_at: datetime = Field(default_factory=datetime.utcnow)  # Data de criação
    updated_at: datetime = Field(default_factory=datetime.utcnow)  # Data de atualização

    class Config:
        json_schema_extra = {
            "example": {
                "username": "john_doe",
                "email": "john.doe@example.com",
                "full_name": "John Doe",
                "is_active": True
            }
        }

    class Settings:
        name = "users"  # Nome da coleção no MongoDB
