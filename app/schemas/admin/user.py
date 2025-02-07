# app/schemas/admin/user.py
from pydantic import BaseModel, EmailStr, Field
from typing import Optional, Any
from bson import ObjectId

# Schema para criação de usuário
class UserCreate(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=8)
    username: str = Field(..., min_length=3)
    full_name: str
    is_admin: bool = False

    class Config:
        json_schema_extra = {
            "example": {
                "email": "john.doe@example.com",
                "password": "strongpass123",
                "username": "john_doe",
                "full_name": "John Doe",
                "is_admin": False
            }
        }

# Schema para resposta de usuário (sem dados sensíveis)
class UserResponse(BaseModel):
    id: str
    email: EmailStr
    username: str
    full_name: str
    is_admin: bool

    class Config:
        json_schema_extra = {
            "example": {
                "id": "507f1f77bcf86cd799439011",
                "email": "john.doe@example.com",
                "username": "john_doe",
                "full_name": "John Doe",
                "is_admin": False
            }
        }
class UpdateUserModel(BaseModel):
    email: Optional[EmailStr] = None
    username: Optional[str] = None
    full_name: Optional[str] = None
    password: Optional[str] = Field(None, min_length=8)
    is_admin: Optional[bool] = None
    is_active: Optional[bool] = None  # Campo adicionado ao schema de atualização
    
    class Config:
        json_schema_extra = {
            "example": {
                "email": "johndoe@example.com",
                "username": "johndoe",
                "full_name": "John Doe",
                "password": "newpassword",
                "is_admin": False,
                "is_active": True
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