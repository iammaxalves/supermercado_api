from pydantic import BaseModel
from typing import Optional, Any

# Schema para atualização de Role
class UpdateRoleModel(BaseModel):
    name: str

    class Config:
        json_schema_extra = {
            "example": {
                "name": "System Administrator",
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
