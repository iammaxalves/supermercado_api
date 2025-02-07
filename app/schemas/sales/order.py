from pydantic import BaseModel
from typing import Optional, Any, List
from beanie import PydanticObjectId

# Schema para atualização de Order
class UpdateOrderModel(BaseModel):
    customer_name: Optional[str]
    products: Optional[List[PydanticObjectId]]
    total_amount: Optional[float]
    status: Optional[str]

    class Config:
        json_schema_extra = {
            "example": {
                "customer_name": "Ana Pereira",
                "products": ["60a3b3f3e1d5b9e7e9b1a3a7"],
                "total_amount": 150.00,
                "status": "shipped"
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
