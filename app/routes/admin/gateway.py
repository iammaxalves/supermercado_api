from fastapi import APIRouter

router = APIRouter()

@router.get("/api/gateway/status", tags=["Gateway"])
async def gateway_status():
    return {"message": "API Gateway está ativo e funcionando corretamente!"}
