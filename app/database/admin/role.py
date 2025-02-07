from typing import List, Union, Optional
from datetime import datetime
from beanie import PydanticObjectId

from app.models.admin.role import Role
#from app.models.admin.user import User  # Vamos adicionar isso no futuro

###### -------------------------- Role -------------------------- ######

# Criar um novo papel (Role)
async def add_role(role: Role) -> Role:
    return await role.create()

# Buscar todos os papéis (Roles)
async def retrieve_roles() -> List[Role]:
    roles = await Role.all().to_list()
    return roles if roles else []

# Buscar um papel (Role) por ID
async def retrieve_role(id: PydanticObjectId) -> Optional[Role]:
    return await Role.get(id)

# Atualizar um papel (Role)
async def update_role_data(id: PydanticObjectId, data: dict) -> Union[bool, Role]:
    role = await Role.get(id)
    if role:
        update_data = {k: v for k, v in data.items() if v is not None}
        update_data["updated_at"] = datetime.utcnow()  # Atualiza a data
        await role.update({"$set": update_data})
        return role
    return False

# Deletar um papel (Role)
async def delete_role(id: PydanticObjectId) -> bool:
    role = await Role.get(id)
    if role:
        await role.delete()
        return True
    return False
