from typing import List, Union, Optional
from datetime import datetime
from beanie import PydanticObjectId

from app.models.sales.invoice import Invoice

###### -------------------------- Invoice -------------------------- ######

# Criar um novo invoice (fatura)
async def add_invoice(invoice: Invoice) -> Invoice:
    return await invoice.create()

# Buscar todos os invoices (faturas)
async def retrieve_invoices() -> List[Invoice]:
    invoices = await Invoice.all().to_list()
    return invoices if invoices else []

# Buscar um invoice (fatura) por ID
async def retrieve_invoice(id: PydanticObjectId) -> Optional[Invoice]:
    return await Invoice.get(id)

# Atualizar um invoice (fatura)
async def update_invoice_data(id: PydanticObjectId, data: dict) -> Union[bool, Invoice]:
    invoice = await Invoice.get(id)
    if invoice:
        update_data = {k: v for k, v in data.items() if v is not None}
        update_data["updated_at"] = datetime.utcnow()  # Atualiza a data
        await invoice.update({"$set": update_data})
        return invoice
    return False

# Deletar um invoice (fatura)
async def delete_invoice(id: PydanticObjectId) -> bool:
    invoice = await Invoice.get(id)
    if invoice:
        await invoice.delete()
        return True
    return False
