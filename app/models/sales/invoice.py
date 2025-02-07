from beanie import Document
from pydantic import Field
from datetime import datetime
from beanie import PydanticObjectId
from typing import List

class Invoice(Document):
    customer_name: str = Field(..., max_length=100)  # Nome do cliente
    products: List[PydanticObjectId] = Field(...)  # Lista de produtos vendidos
    total_amount: float = Field(..., ge=0)  # Valor total da fatura
    created_at: datetime = Field(default_factory=datetime.utcnow)  # Data de criação
    updated_at: datetime = Field(default_factory=datetime.utcnow)  # Data de atualização

    class Config:
        json_schema_extra = {
            "example": {
                "customer_name": "João Silva",
                "products": ["60a3b3f3e1d5b9e7e9b1a3a7", "60a3b3f3e1d5b9e7e9b1a3b8"],
                "total_amount": 150.75
            }
        }

    class Settings:
        name = "invoices"  # Nome da coleção no MongoDB
