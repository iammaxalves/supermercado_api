from typing import List, Union, Optional
from datetime import datetime
from beanie import PydanticObjectId

from app.models.inventory.product import Product

###### -------------------------- Product -------------------------- ######

# Criar um novo produto
async def add_product(product: Product) -> Product:
    return await product.create()

# Buscar todos os produtos
async def retrieve_products() -> List[Product]:
    products = await Product.all().to_list()
    return products if products else []

# Buscar um produto por ID
async def retrieve_product(id: PydanticObjectId) -> Optional[Product]:
    return await Product.get(id)

# Atualizar um produto
async def update_product_data(id: PydanticObjectId, data: dict) -> Union[bool, Product]:
    product = await Product.get(id)
    if product:
        update_data = {k: v for k, v in data.items() if v is not None}
        update_data["updated_at"] = datetime.utcnow()  # Atualiza a data
        await product.update({"$set": update_data})
        return product
    return False

# Deletar um produto
async def delete_product(id: PydanticObjectId) -> bool:
    product = await Product.get(id)
    if product:
        await product.delete()
        return True
    return False
