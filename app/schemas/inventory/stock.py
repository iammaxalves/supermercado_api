from pydantic import BaseModel
from typing import Optional, Any
from beanie import PydanticObjectId

# Schema para atualização de Stock
class UpdateStockModel(BaseModel):
    product_id: PydanticObjectId
    quantity: int
    location: str

    class Config:
        json_schema_extra = {
            "example": {
                "product_id": "60a3b3f3e1d5b9e7e9b1a3a7",
                "quantity": 100,
                "location": "Warehouse B"
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
