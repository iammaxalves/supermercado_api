from beanie import Document, PydanticObjectId
from pydantic import Field
from typing import List
from datetime import datetime

class Role(Document):
    name: str = Field(..., max_length=100, unique=True)  # Nome do papel
    users: List[PydanticObjectId] = []  # Lista de usuários associados
    created_at: datetime = Field(default_factory=datetime.utcnow)  # Data de criação
    updated_at: datetime = Field(default_factory=datetime.utcnow)  # Data de atualização

    class Config:
        json_schema_extra = {
            "example": {
                "name": "System Administrator"
            }
        }

    class Settings:
        name = "roles"  # Nome da coleção no MongoDB
