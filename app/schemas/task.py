from datetime import datetime

from pydantic import BaseModel, EmailStr, Field

from schemas.base import DateTime


class BaseTask(BaseModel):
    title: str
    description: str | None = None
    due_date: datetime | None = None
    completed: bool = Field(default=False)


class TaskCreate(BaseTask):
    ...


class TaskInDBBase(BaseTask):
    id: str | None = Field(None)
    user_id: str = Field(...)

    class Config:
        orm_mod = True


class TaskInDB(TaskInDBBase, DateTime):
    ...


class TaskRead(TaskInDBBase, DateTime):
    ...
