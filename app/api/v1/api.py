from fastapi import APIRouter

from api.v1.endpoints import auth
from api.v1.endpoints import task

api_router = APIRouter()
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(task.router, prefix="/tasks", tags=["tasks"])
