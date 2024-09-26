from bson import ObjectId
from fastapi import APIRouter, Depends
from motor.motor_asyncio import AsyncIOMotorClient

import crud
from api import deps
from schemas.task import TaskRead, TaskCreate, TaskInDB
from schemas.user import UserRead

router = APIRouter()


@router.post("/", response_model=TaskRead)
async def create_task(
        task_in: TaskCreate,
        current_user: UserRead = Depends(deps.get_current_user),
        db_cli: AsyncIOMotorClient = Depends(deps.get_db_cli)
):
    task_in_db = await crud.task.create(db_cli=db_cli,
                                        obj_in=TaskInDB(user_id=current_user.id, **task_in.model_dump()))
    return task_in_db


@router.get("/{task_id}", response_model=TaskRead)
async def create_task(
        task_id: str,
        current_user: UserRead = Depends(deps.get_current_user),
        db_cli: AsyncIOMotorClient = Depends(deps.get_db_cli)
):
    task_doc = await crud.task.get(db_cli=db_cli,
                                   query={"_id": ObjectId(task_id), "user_id": current_user.id})
    return task_doc
