from typing import List, Union, Optional
from datetime import datetime
from beanie import PydanticObjectId

from app.models.admin.user import User

###### -------------------------- User -------------------------- ######

# Criar um novo usuário (User)
async def add_user(user: User) -> User:
    return await user.create()

# Buscar todos os usuários (Users)
async def retrieve_users() -> List[User]:
    users = await User.all().to_list()
    return users if users else []

# Buscar um usuário (User) por ID
async def retrieve_user(id: PydanticObjectId) -> Optional[User]:
    return await User.get(id)

# Atualizar um usuário (User)
async def update_user_data(id: PydanticObjectId, data: dict) -> Union[bool, User]:
    user = await User.get(id)
    if user:
        update_data = {k: v for k, v in data.items() if v is not None}
        update_data["updated_at"] = datetime.utcnow()  # Atualiza a data
        await user.update({"$set": update_data})
        return user
    return False

# Deletar um usuário (User)
async def delete_user(id: PydanticObjectId) -> bool:
    user = await User.get(id)
    if user:
        await user.delete()
        return True
    return False
