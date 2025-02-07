from pydantic import BaseModel
from typing import Optional, Any, List
from beanie import PydanticObjectId

# Schema para atualização de Invoice
class UpdateInvoiceModel(BaseModel):
    customer_name: str
    products: List[PydanticObjectId]
    total_amount: float

    class Config:
        json_schema_extra = {
            "example": {
                "customer_name": "Maria Oliveira",
                "products": ["60a3b3f3e1d5b9e7e9b1a3a7", "60a3b3f3e1d5b9e7e9b1a3b9"],
                "total_amount": 200.50
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
