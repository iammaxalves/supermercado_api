from fastapi import APIRouter, Body, Request
from beanie import PydanticObjectId
from app.database.admin.role import (
    retrieve_roles,
    retrieve_role,
    add_role,
    update_role_data,
    delete_role
)
from app.models.admin.role import Role
from app.schemas.admin.role import Response, UpdateRoleModel
from app.utils.response_utils import create_response
from app.utils.exceptions import NotFoundException

router = APIRouter()

# Endpoint para listar todos os papéis (Roles)
@router.get("/", response_description="Roles retrieved")
async def get_roles(request: Request):
    roles = await retrieve_roles()
    if roles:
        return create_response(
            request=request,
            data=roles,
            description="Roles data retrieved successfully"
        )
    raise NotFoundException("No roles found")

# Endpoint para buscar um papel (Role) por ID
@router.get("/{id}", response_description="Role data retrieved")
async def get_role_data(request: Request, id: PydanticObjectId):
    role = await retrieve_role(id)
    if role:
        return create_response(
            request=request,
            data=role,
            description="Role data retrieved successfully"
        )
    raise NotFoundException("Role doesn't exist")

# Endpoint para adicionar um novo papel (Role)
@router.post("/", response_description="Role data added into the database")
async def add_role_data(request: Request, role: Role = Body(...)):
    new_role = await add_role(role)
    return create_response(
        request=request,
        data=new_role,
        description="Role created successfully"
    )

# Endpoint para atualizar um papel (Role)
@router.put("/{id}", response_model=Response)
async def update_role(request: Request, id: PydanticObjectId, req: UpdateRoleModel = Body(...)):
    updated_role = await update_role_data(id, req.dict())
    if updated_role:
        return create_response(
            request=request,
            data=updated_role,
            description=f"Role with ID: {id} updated successfully"
        )
    raise NotFoundException(f"Role with ID: {id} not found")

# Endpoint para deletar um papel (Role)
@router.delete("/{id}", response_description="Role data deleted from the database")
async def delete_role_data(request: Request, id: PydanticObjectId):
    deleted_role = await delete_role(id)
    if deleted_role:
        return create_response(
            request=request,
            data=deleted_role,
            description=f"Role with ID: {id} removed"
        )
    raise NotFoundException(f"Role with ID: {id} doesn't exist")
