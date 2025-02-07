from fastapi import APIRouter, Body, Request
from beanie import PydanticObjectId

from app.database.inventory.stock import (
    retrieve_stocks,
    retrieve_stock,
    add_stock,
    update_stock_data,
    delete_stock
)
from app.models.inventory.stock import Stock
from app.schemas.inventory.stock import Response, UpdateStockModel
from app.utils.response_utils import create_response
from app.utils.exceptions import NotFoundException

router = APIRouter()

# Endpoint para listar todos os estoques
@router.get("/", response_description="Stocks retrieved")
async def get_stocks(request: Request):
    stocks = await retrieve_stocks()
    if stocks:
        return create_response(
            request=request,
            data=stocks,
            description="Stocks data retrieved successfully"
        )
    raise NotFoundException("No stocks found")

# Endpoint para buscar um estoque por ID
@router.get("/{id}", response_description="Stock data retrieved")
async def get_stock_data(request: Request, id: PydanticObjectId):
    stock = await retrieve_stock(id)
    if stock:
        return create_response(
            request=request,
            data=stock,
            description="Stock data retrieved successfully"
        )
    raise NotFoundException("Stock doesn't exist")

# Endpoint para adicionar um novo registro de estoque
@router.post("/", response_description="Stock data added into the database")
async def add_stock_data(request: Request, stock: Stock = Body(...)):
    new_stock = await add_stock(stock)
    return create_response(
        request=request,
        data=new_stock,
        description="Stock created successfully"
    )

# Endpoint para atualizar um estoque
@router.put("/{id}", response_model=Response)
async def update_stock(request: Request, id: PydanticObjectId, req: UpdateStockModel = Body(...)):
    updated_stock = await update_stock_data(id, req.dict())
    if updated_stock:
        return create_response(
            request=request,
            data=updated_stock,
            description=f"Stock with ID: {id} updated successfully"
        )
    raise NotFoundException(f"Stock with ID: {id} not found")

# Endpoint para deletar um estoque
@router.delete("/{id}", response_description="Stock data deleted from the database")
async def delete_stock_data(request: Request, id: PydanticObjectId):
    deleted_stock = await delete_stock(id)
    if deleted_stock:
        return create_response(
            request=request,
            data=deleted_stock,
            description=f"Stock with ID: {id} removed"
        )
    raise NotFoundException(f"Stock with ID: {id} doesn't exist")
