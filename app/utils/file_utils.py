# app/utils/file_utils.py
from fastapi import UploadFile, HTTPException
import magic

async def validate_file(file: UploadFile):
    # Verificar se é uma imagem
    content_type = magic.from_buffer(await file.read(1024), mime=True)
    await file.seek(0)
    
    if not content_type.startswith('image/'):
        raise HTTPException(
            status_code=400,
            detail="File must be an image"
        )

    # Verificar tamanho do arquivo (5MB)
    max_size = 5 * 1024 * 1024
    file_size = 0
    while content := await file.read(1024 * 1024):
        file_size += len(content)
        if file_size > max_size:
            raise HTTPException(
                status_code=400,
                detail="File size too large. Maximum size is 5MB"
            )
    await file.seek(0)

    return file