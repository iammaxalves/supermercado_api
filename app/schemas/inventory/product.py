from pydantic import BaseModel
from typing import Optional, Any

# Schema para atualização de Product
class UpdateProductModel(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    quantity: int

    class Config:
        json_schema_extra = {
            "example": {
                "name": "Laptop",
                "description": "High-performance laptop",
                "price": 1299.99,
                "quantity": 10
            }
        }

# Schema de resposta padrão
class Response(BaseModel):
    status_code: int
    response_type: str
    description: str
    data: Optional[Any]

    class Config:
        json_schema_extra = {
            "example": {
                "status_code": 200,
                "response_type": "success",
                "description": "Operation successful",
                "data": "Sample data",
            }
        }
