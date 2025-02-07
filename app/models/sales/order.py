from beanie import Document
from pydantic import Field
from typing import List, Optional
from datetime import datetime

class Order(Document):
    customer_name: str = Field(..., max_length=100)  # Nome do cliente
    status: str = Field(default="pending", max_length=50)  # Status do pedido
    products: List[str] = Field(default=[])  # Lista de produtos
    total_amount: float = Field(..., ge=0)  # Valor total do pedido
    created_at: datetime = Field(default_factory=datetime.utcnow)  # Data de criação
    updated_at: datetime = Field(default_factory=datetime.utcnow)  # Data de atualização

    class Settings:
        name = "orders"  # Nome da coleção no MongoDB
