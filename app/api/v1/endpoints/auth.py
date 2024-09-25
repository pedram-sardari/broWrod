from fastapi import APIRouter, Depends, HTTPException
from motor.motor_asyncio import AsyncIOMotorClient

import crud
from api import deps
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
