from fastapi import APIRouter, Body, Request, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from beanie import PydanticObjectId
from datetime import timedelta
from app.utils.security_utils import validate_object_id
from app.middleware.logging import limiter
from app.config.config import sanitize_input
from fastapi.responses import JSONResponse
import secrets
from app.database.admin.user import (
    retrieve_users,
    retrieve_user,
    add_user,
    update_user_data,
    delete_user
)
from app.middleware.auth import (
    get_password_hash,
    verify_password,
    create_access_token,
    get_current_user,
    get_current_admin_user
)
from app.models.admin.user import User
from app.schemas.admin.user import Response, UpdateUserModel, UserCreate, UserResponse
from app.utils.response_utils import create_response
from app.utils.exceptions import NotFoundException

router = APIRouter()

@router.post("/login", response_model=dict)
@limiter.limit("5/minute")
async def login(request: Request, form_data: OAuth2PasswordRequestForm = Depends()):
    # Verifica o usuário
    user = await User.find_one({"username": form_data.username})
    if not user or not verify_password(form_data.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuário ou senha incorretos",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Verifica se o usuário está ativo
    if not getattr(user, 'is_active', True):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Conta de usuário está inativa"
        )

    # Gera os tokens
    access_token = create_access_token(data={"sub": user.username})
    csrf_token = secrets.token_urlsafe(32)

    # Armazena o token CSRF na sessão
    if "session" in request.scope:
        request.session["csrf_token"] = csrf_token  # Armazena corretamente o token CSRF

    # Prepara os dados do usuário para a resposta
    response_data = {
        "access_token": access_token,
        "token_type": "bearer",
        "username": user.username,
        "is_admin": user.is_admin,
        "csrf_token": csrf_token
    }

    # Cria a resposta final com o header CSRF
    response = JSONResponse(content=response_data)
    response.headers["X-CSRF-Token"] = csrf_token  # Envia o token CSRF no cabeçalho

    return response

@router.get("/", response_description="Users retrieved")
async def get_users(
    request: Request,
    current_user: User = Depends(get_current_admin_user)
):
    users = await retrieve_users()
    if users:
        return create_response(
            request=request,
            data=users,
            description="Users data retrieved successfully"
        )
    raise NotFoundException("No users found")

@router.get("/{id}", response_description="User data retrieved")
async def get_user_data(
    request: Request,
    id: str,
    current_user: User = Depends(get_current_admin_user)
):
    user_id = validate_object_id(id)
    user = await retrieve_user(user_id)
    if user:
        return create_response(
            request=request,
            data=user,
            description="User data retrieved successfully"
        )
    raise NotFoundException("Invalid credentials")

@router.post("/register", response_description="User data added into the database")
async def register_user(request: Request, user: UserCreate):
    sanitized_username = sanitize_input(user.username)
    sanitized_email = sanitize_input(user.email)
    sanitized_full_name = sanitize_input(user.full_name)

    existing_user = await User.find_one({"email": sanitized_email})
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    hashed_password = get_password_hash(user.password)
    new_user = User(
        email=sanitized_email,
        username=sanitized_username,
        full_name=sanitized_full_name,
        password=hashed_password,
        is_admin=user.is_admin
    )
    created_user = await add_user(new_user)
    
    return create_response(
        request=request,
        data=created_user,
        description="User created successfully"
    )

@router.get("/me/profile", response_description="User profile retrieved")
async def read_users_me(
    request: Request,
    current_user: User = Depends(get_current_user)
):
    return create_response(
        request=request,
        data=current_user,
        description="Profile retrieved successfully"
    )

@router.put("/{id}", response_model=Response)
async def update_user_endpoint(
    request: Request,
    id: PydanticObjectId,
    req: UpdateUserModel = Body(...),
    
    current_user: User = Depends(get_current_admin_user)
):
    if "password" in req.dict(exclude_unset=True):
        req.password = get_password_hash(req.password)
    
    updated_user = await update_user_data(id, req.dict(exclude_unset=True))
    if updated_user:
        return create_response(
            request=request,
            data=updated_user,
            description=f"User with ID: {id} updated successfully"
        )
    raise NotFoundException(f"User with ID: {id} not found")

@router.delete("/{id}", response_description="User data deleted from the database")
async def delete_user_data(
    request: Request,
    id: PydanticObjectId,
    current_user: User = Depends(get_current_admin_user)
):
    deleted_user = await delete_user(id)
    if deleted_user:
        return create_response(
            request=request,
            data=deleted_user,
            description=f"User with ID: {id} removed"
        )
    raise NotFoundException(f"User with ID: {id} doesn't exist")


@router.post("/logout", response_model=dict)
async def logout(request: Request):
    # Verifica se a sessão está ativa
    if "session" not in request.scope:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No active session"
        )

    # Remove os dados da sessão
    request.session.clear()

    return {"message": "Logout successful"}

