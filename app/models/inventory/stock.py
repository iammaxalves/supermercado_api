from beanie import Document
from pydantic import Field
from datetime import datetime
from beanie import PydanticObjectId

class Stock(Document):
    product_id: PydanticObjectId = Field(...)  # Referência ao produto
    quantity: int = Field(..., ge=0)  # Quantidade em estoque
    location: str = Field(..., max_length=100)  # Localização do estoque
    created_at: datetime = Field(default_factory=datetime.utcnow)  # Data de criação
    updated_at: datetime = Field(default_factory=datetime.utcnow)  # Data de atualização

    class Config:
        json_schema_extra = {
            "example": {
                "product_id": "60a3b3f3e1d5b9e7e9b1a3a7",
                "quantity": 50,
                "location": "Warehouse A"
            }
        }

    class Settings:
        name = "stocks"  # Nome da coleção no MongoDB
