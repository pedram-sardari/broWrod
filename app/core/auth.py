from datetime import timedelta, timezone, datetime

from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from motor.motor_asyncio import AsyncIOMotorClient

import crud
from core.config import settings
from core.security import verify_password
from schemas.user import UserInDB

oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{settings.API_V1_STR}/auth/login")


async def authenticate(*, db_cli: AsyncIOMotorClient,
                       email: str, password: str) -> UserInDB | None:
    user = await crud.user.get_by_email(db_cli=db_cli, email=email)
    if not user:
        return None
    if not verify_password(plain_password=password, hashed_password=user.password):
        return None
    return user


def create_access_token(*, sub: str) -> str:
    return _create_token(
        token_type=settings.ACCESS_TOKEN_FIELD_NAME,
        lifetime=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES),
        sub=sub,
    )


def _create_token(
        token_type: str,
        lifetime: timedelta,
        sub: str,
) -> str:
    payload = {}
    issued_at = datetime.now(timezone.utc)
    expire = issued_at + lifetime
    payload["type"] = token_type
    payload["exp"] = expire
    payload["iat"] = issued_at
    payload["sub"] = str(sub)
    return jwt.encode(payload, settings.JWT_SECRET, algorithm=settings.ALGORITHM)
