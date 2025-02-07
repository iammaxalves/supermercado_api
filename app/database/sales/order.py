from typing import List, Optional, Union
from datetime import datetime
from beanie import PydanticObjectId
from app.models.sales.order import Order

# Criar um novo pedido
async def add_order(order: Order) -> Order:
    return await order.create()

# Buscar todos os pedidos
async def retrieve_orders() -> List[Order]:
    return await Order.all().to_list()

# Buscar um pedido por ID
async def retrieve_order(id: PydanticObjectId) -> Optional[Order]:
    return await Order.get(id)

# Atualizar um pedido
async def update_order_data(id: PydanticObjectId, data: dict) -> Union[bool, Order]:
    order = await Order.get(id)
    if order:
        update_data = {k: v for k, v in data.items() if v is not None}
        update_data["updated_at"] = datetime.utcnow()
        await order.update({"$set": update_data})
        return order
    return False

# Deletar um pedido
async def delete_order(id: PydanticObjectId) -> bool:
    order = await Order.get(id)
    if order:
        await order.delete()
        return True
    return False
