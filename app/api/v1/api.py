from fastapi import APIRouter

from api.v1.endpoints import auth
from api.v1.endpoints import word

api_router = APIRouter()
api_router.include_router(auth.router, prefix="/users", tags=["users"])
