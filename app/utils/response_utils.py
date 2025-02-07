from starlette.requests import Request
from starlette.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_204_NO_CONTENT, HTTP_404_NOT_FOUND
from typing import Any

def create_response(request: Request, data: Any = None, description: str = "Operation successful") -> dict:
    # Determina o código de status com base no método HTTP
    if request.method == "POST":
        status_code = HTTP_201_CREATED if data else HTTP_204_NO_CONTENT
    elif request.method in {"PUT", "PATCH"}:
        status_code = HTTP_200_OK
    elif request.method == "DELETE":
        status_code = HTTP_204_NO_CONTENT if data is None else HTTP_200_OK
    else:  # GET e outros casos
        status_code = HTTP_200_OK if data else HTTP_404_NOT_FOUND
    
    # Retorna o dicionário padronizado
    response_type = "success" if status_code < 400 else "error"
    return {
        "status_code": status_code,
        "response_type": response_type,
        "description": description,
        "data": data,
    }
