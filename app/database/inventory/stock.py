from typing import List, Union, Optional
from datetime import datetime
from beanie import PydanticObjectId

from app.models.inventory.stock import Stock

###### -------------------------- Stock -------------------------- ######

# Criar um novo registro de estoque
async def add_stock(stock: Stock) -> Stock:
    return await stock.create()

# Buscar todos os registros de estoque
async def retrieve_stocks() -> List[Stock]:
    stocks = await Stock.all().to_list()
    return stocks if stocks else []

# Buscar um registro de estoque por ID
async def retrieve_stock(id: PydanticObjectId) -> Optional[Stock]:
    return await Stock.get(id)

# Atualizar um registro de estoque
async def update_stock_data(id: PydanticObjectId, data: dict) -> Union[bool, Stock]:
    stock = await Stock.get(id)
    if stock:
        update_data = {k: v for k, v in data.items() if v is not None}
        update_data["updated_at"] = datetime.utcnow()  # Atualiza a data
        await stock.update({"$set": update_data})
        return stock
    return False

# Deletar um registro de estoque
async def delete_stock(id: PydanticObjectId) -> bool:
    stock = await Stock.get(id)
    if stock:
        await stock.delete()
        return True
    return False
