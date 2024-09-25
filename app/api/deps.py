from typing import Generator

from fastapi import Depends, HTTPException
from jose import jwt, JWTError
from motor.motor_asyncio import AsyncIOMotorClient
from starlette import status

import crud
from core.auth import oauth2_scheme
from schemas.others import TokenData
from schemas.user import UserInDBBase
from core.config import settings
from db.session import Client


def get_db_cli() -> Generator:  # todo: can this be a coroutine?
    db_cli = Client()
    try:
        yield db_cli
    finally:
        db_cli.close()
        print('%' * 20, 'closing the db client', '%' * 20)


async def get_current_user(
        db_cli: AsyncIOMotorClient = Depends(get_db_cli), token: str = Depends(oauth2_scheme)
) -> UserInDBBase:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(
            token,
            settings.JWT_SECRET,
            algorithms=[settings.ALGORITHM],
            options={"verify_aud": False},
        )
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
        token_data = TokenData(user_id=user_id)
    except JWTError:
        raise credentials_exception

    user = await crud.user.get_by_id(db_cli=db_cli, id=token_data.user_id)
    if user is None:
        raise credentials_exception
    return user
