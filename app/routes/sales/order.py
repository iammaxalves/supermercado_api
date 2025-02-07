from fastapi import APIRouter, Body, Request
from beanie import PydanticObjectId

from app.database.sales.order import (
    retrieve_orders,
    retrieve_order,
    add_order,
    update_order_data,
    delete_order
)
from app.models.sales.order import Order
from app.schemas.sales.order import Response, UpdateOrderModel
from app.utils.response_utils import create_response
from app.utils.exceptions import NotFoundException

router = APIRouter()

# Endpoint para listar todos os pedidos
@router.get("/", response_description="Orders retrieved")
async def get_orders(request: Request):
    orders = await retrieve_orders()
    if orders:
        return create_response(
            request=request,
            data=orders,
            description="Orders data retrieved successfully"
        )
    raise NotFoundException("No orders found")

# Endpoint para buscar um pedido por ID
@router.get("/{id}", response_description="Order data retrieved")
async def get_order_data(request: Request, id: PydanticObjectId):
    order = await retrieve_order(id)
    if order:
        return create_response(
            request=request,
            data=order,
            description="Order data retrieved successfully"
        )
    raise NotFoundException("Order doesn't exist")

# Endpoint para adicionar um novo pedido
@router.post("/", response_description="Order data added into the database")
async def add_order_data(request: Request, order: Order = Body(...)):
    new_order = await add_order(order)
    return create_response(
        request=request,
        data=new_order,
        description="Order created successfully"
    )

# Endpoint para atualizar um pedido
@router.put("/{id}", response_model=Response)
async def update_order(request: Request, id: PydanticObjectId, req: UpdateOrderModel = Body(...)):
    updated_order = await update_order_data(id, req.dict())
    if updated_order:
        return create_response(
            request=request,
            data=updated_order,
            description=f"Order with ID: {id} updated successfully"
        )
    raise NotFoundException(f"Order with ID: {id} not found")

# Endpoint para deletar um pedido
@router.delete("/{id}", response_description="Order data deleted from the database")
async def delete_order_data(request: Request, id: PydanticObjectId):
    deleted_order = await delete_order(id)
    if deleted_order:
        return create_response(
            request=request,
            data=deleted_order,
            description=f"Order with ID: {id} removed"
        )
    raise NotFoundException(f"Order with ID: {id} doesn't exist")
