from typing import Any

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from motor.motor_asyncio import AsyncIOMotorClient

import crud
from api import deps
from core.auth import authenticate, create_access_token
from core.config import settings
from schemas import user as user_schemas

router = APIRouter()


@router.post('/register', status_code=201, response_model=user_schemas.UserRead)
async def register(
        user_in: user_schemas.UserCreate,
        db_cli: AsyncIOMotorClient = Depends(deps.get_db_cli)
) -> user_schemas.UserRead:  # todo: return a value error to check something that is not `User`

    if await crud.user.get_by_email(db_cli=db_cli, email=user_in.email):
        raise HTTPException(
            status_code=409,
            detail="The email already exists"
        )

    user_in_db = await crud.user.create_user(db_cli=db_cli,
                                             obj_in=user_schemas.UserInDB(**user_in.model_dump()))
    return user_in_db


@router.post("/login")
async def login(
        form_data: OAuth2PasswordRequestForm = Depends(),
        db_cli: AsyncIOMotorClient = Depends(deps.get_db_cli)
) -> Any:
    user = await authenticate(email=form_data.username, password=form_data.password, db_cli=db_cli)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    return {
        settings.ACCESS_TOKEN_FIELD_NAME: create_access_token(sub=user.id),
        "token_type": settings.BEARER_STR,
    }


@router.get("/me", description="Get logged in user info", response_model=user_schemas.UserRead)
async def me(current_user: user_schemas.UserRead = Depends(deps.get_current_user)):
    return current_user
