from fastapi import APIRouter, Body, Form, Request, UploadFile, File, Depends
import os
from pathlib import Path
from beanie import PydanticObjectId
from typing import Optional
from uuid import uuid4
import aiofiles

from app.database.inventory.product import (
    retrieve_products,
    retrieve_product,
    add_product,
    update_product_data,
    delete_product
)
from app.models.inventory.product import Product
from app.schemas.inventory.product import Response, UpdateProductModel
from app.utils.response_utils import create_response
from app.utils.exceptions import NotFoundException, InternalServerErrorException
from app.utils.file_utils import validate_file



router = APIRouter()
UPLOAD_DIR = Path("uploads/products")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)


# Endpoint para listar todos os produtos
@router.get("/", response_description="Products retrieved")
async def get_products(request: Request):
    products = await retrieve_products()
    if products:
        return create_response(
            request=request,
            data=products,
            description="Products data retrieved successfully"
        )
    raise NotFoundException("No products found")

# Endpoint para buscar um produto por ID
@router.get("/{id}", response_description="Product data retrieved")
async def get_product_data(request: Request, id: PydanticObjectId):
    product = await retrieve_product(id)
    if product:
        return create_response(
            request=request,
            data=product,
            description="Product data retrieved successfully"
        )
    raise NotFoundException("Product doesn't exist")


@router.post("/", response_description="Product data added into the database")
async def add_product_data(
    request: Request,
    name: str = Form(...),
    description: str = Form(...),
    price: float = Form(...),
    quantity: int = Form(...),
    image: Optional[UploadFile] = File(None),
):
    try:
        # Criar o objeto do produto
        product_data = {
            "name": name,
            "description": description,
            "price": price,
            "quantity": quantity,
            "image_url": None
        }
        
        if image:
            validated_file = await validate_file(image)
            file_extension = os.path.splitext(image.filename)[1]
            file_name = f"{uuid4()}{file_extension}"
            file_path = UPLOAD_DIR / file_name
            
            async with aiofiles.open(file_path, "wb") as buffer:
                content = await validated_file.read()
                await buffer.write(content)
            product_data["image_url"] = f"/uploads/products/{file_name}"

        product = Product(**product_data)
        new_product = await add_product(product)
        
        return create_response(
            request=request,
            data=new_product,
            description="Product created successfully"
        )
    except Exception as e:
        raise InternalServerErrorException(str(e))

# Endpoint para atualizar um produto
@router.put("/{id}", response_model=Response)
async def update_product(request: Request, id: PydanticObjectId, req: UpdateProductModel = Body(...)):
    updated_product = await update_product_data(id, req.dict())
    if updated_product:
        return create_response(
            request=request,
            data=updated_product,
            description=f"Product with ID: {id} updated successfully"
        )
    raise NotFoundException(f"Product with ID: {id} not found")

# Endpoint para deletar um produto
@router.delete("/{id}", response_description="Product data deleted from the database")
async def delete_product_data(request: Request, id: PydanticObjectId):
    deleted_product = await delete_product(id)
    if deleted_product:
        return create_response(
            request=request,
            data=deleted_product,
            description=f"Product with ID: {id} removed"
        )
    raise NotFoundException(f"Product with ID: {id} doesn't exist")


# Adicione este novo endpoint na sua router
@router.post("/upload/{id}", response_description="Product image uploaded")
async def upload_product_image(
    request: Request,
    id: PydanticObjectId,
    file: UploadFile = Depends(validate_file)
):
    # Verificar se o produto existe
    product = await retrieve_product(id)
    if not product:
        raise NotFoundException(f"Product with ID: {id} doesn't exist")

    # Criar nome único para o arquivo
    file_extension = os.path.splitext(file.filename)[1]
    file_name = f"{id}{file_extension}"
    file_path = UPLOAD_DIR / file_name

    # Salvar o arquivo
    try:
        with open(file_path, "wb") as buffer:
            content = await file.read()
            buffer.write(content)
    except Exception as e:
        return create_response(
            request=request,
            data=None,
            description="Failed to upload image",
            status_code=500
        )

    # Atualizar o produto com o URL da imagem
    image_url = f"/uploads/products/{file_name}"
    update_data = {"image_url": image_url}
    updated_product = await update_product_data(id, update_data)

    return create_response(
        request=request,
        data=updated_product,
        description="Product image uploaded successfully"
    )