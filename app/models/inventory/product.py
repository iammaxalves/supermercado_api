from beanie import Document
from pydantic import Field
from datetime import datetime
from typing import Optional, Any

class Product(Document):
    name: str = Field(..., max_length=200, unique=True)  # Nome do produto
    description: str = Field(..., max_length=500)  # Descrição do produto
    price: float = Field(..., gt=0)  # Preço do produto
    quantity: int = Field(..., ge=0)  # Quantidade em estoque
    image_url: Optional[str] = None  # Novo campo para armazenar o URL da imagem
    created_at: datetime = Field(default_factory=datetime.utcnow)  # Data de criação
    updated_at: datetime = Field(default_factory=datetime.utcnow)  # Data de atualização

    class Config:
        json_schema_extra = {
            "example": {
                "name": "Laptop",
                "description": "High-performance laptop",
                "price": 1299.99,
                "quantity": 10,
                "image_url": None
            }
        }

    class Settings:
        name = "products"  # Nome da coleção no MongoDB
