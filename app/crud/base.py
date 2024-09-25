from typing import TypeVar

from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import BaseModel

from core.config import settings

RetrieveSchemaType = TypeVar("RetrieveSchemaType", bound=BaseModel)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class BaseCRUD:
    db_name: str = settings.DATABASE_NAME

    def __init__(self, collection_name: str) -> None:
        self.col_name = collection_name

    async def get(self, *, db_cli: AsyncIOMotorClient, query: dict) -> RetrieveSchemaType:
        return await db_cli[self.db_name][self.col_name].find_one(query)

    async def create(self, *, db_cli: AsyncIOMotorClient, obj_in: CreateSchemaType) -> CreateSchemaType:
        doc = obj_in.model_dump()
        doc.pop(settings.ID_FIELD_NAME)
        res = await db_cli[self.db_name][self.col_name].insert_one(doc)
        obj_in.id = str(res.inserted_id)
        return obj_in
