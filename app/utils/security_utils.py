# app/utils/security_utils.py
from bson import ObjectId
from fastapi import HTTPException, status
import re
from html import escape


def sanitize_input(input_data: dict) -> dict:
    """
    Sanitiza entradas para prevenir NoSQL Injection e XSS.
    Remove ou escapa caracteres especiais.
    """
    sanitized_data = {}
    for key, value in input_data.items():
        if isinstance(value, str):
            # Prevenção de NoSQL Injection
            sanitized_value = value.replace("$", "").replace("{", "").replace("}", "")
            
            # Prevenção de XSS
            sanitized_value = escape(sanitized_value)
            sanitized_value = re.sub(r'<script.*?>.*?</script>', '', sanitized_value, flags=re.I | re.S)
            sanitized_value = re.sub(r' on\w+=".*?"', '', sanitized_value, flags=re.I)
            
            sanitized_data[key] = sanitized_value.strip()
        else:
            sanitized_data[key] = value
    return sanitized_data


def validate_object_id(id: str) -> ObjectId:
    """
    Valida se o ID é um ObjectId válido do MongoDB.
    """
    if not ObjectId.is_valid(id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid ID format"
        )
    return ObjectId(id)