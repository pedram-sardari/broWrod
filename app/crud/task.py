import asyncio

from motor.motor_asyncio import AsyncIOMotorClient

from core.config import settings
from core.security import get_password_hash
from crud.base import BaseCRUD
from schemas.user import UserInDB


class TaskCRUD(BaseCRUD):
    ...


task = TaskCRUD(settings.TASK_COLLECTION_NAME)
#
# if __name__ == "__main__":
#     async def main():
#         print('iner')
#         # res = await user.get(db_cli=AsyncIOMotorClient(), query={"_id": ObjectId("66f42cef7b87f794b9d55621")})
#         # res = await user.get_by_email(db_cli=AsyncIOMotorClient(), email="john_doe@gmail.com")
#         res = await user.get_by_id(db_cli=AsyncIOMotorClient(), id="66f42cef7b87f794b9d55621")
#         print(type(res))
#         print(res)
#
#
#     asyncio.run(main())
