from fastapi import APIRouter, Body, Request
from beanie import PydanticObjectId

from app.database.sales.invoice import (
    retrieve_invoices,
    retrieve_invoice,
    add_invoice,
    update_invoice_data,
    delete_invoice
)
from app.models.sales.invoice import Invoice
from app.schemas.sales.invoice import Response, UpdateInvoiceModel
from app.utils.response_utils import create_response
from app.utils.exceptions import NotFoundException

router = APIRouter()

# Endpoint para listar todas as faturas
@router.get("/", response_description="Invoices retrieved")
async def get_invoices(request: Request):
    invoices = await retrieve_invoices()
    if invoices:
        return create_response(
            request=request,
            data=invoices,
            description="Invoices data retrieved successfully"
        )
    raise NotFoundException("No invoices found")

# Endpoint para buscar uma fatura por ID
@router.get("/{id}", response_description="Invoice data retrieved")
async def get_invoice_data(request: Request, id: PydanticObjectId):
    invoice = await retrieve_invoice(id)
    if invoice:
        return create_response(
            request=request,
            data=invoice,
            description="Invoice data retrieved successfully"
        )
    raise NotFoundException("Invoice doesn't exist")

# Endpoint para adicionar uma nova fatura
@router.post("/", response_description="Invoice data added into the database")
async def add_invoice_data(request: Request, invoice: Invoice = Body(...)):
    new_invoice = await add_invoice(invoice)
    return create_response(
        request=request,
        data=new_invoice,
        description="Invoice created successfully"
    )

# Endpoint para atualizar uma fatura
@router.put("/{id}", response_model=Response)
async def update_invoice(request: Request, id: PydanticObjectId, req: UpdateInvoiceModel = Body(...)):
    updated_invoice = await update_invoice_data(id, req.dict())
    if updated_invoice:
        return create_response(
            request=request,
            data=updated_invoice,
            description=f"Invoice with ID: {id} updated successfully"
        )
    raise NotFoundException(f"Invoice with ID: {id} not found")

# Endpoint para deletar uma fatura
@router.delete("/{id}", response_description="Invoice data deleted from the database")
async def delete_invoice_data(request: Request, id: PydanticObjectId):
    deleted_invoice = await delete_invoice(id)
    if deleted_invoice:
        return create_response(
            request=request,
            data=deleted_invoice,
            description=f"Invoice with ID: {id} removed"
        )
    raise NotFoundException(f"Invoice with ID: {id} doesn't exist")
