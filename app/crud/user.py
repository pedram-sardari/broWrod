import asyncio

from motor.motor_asyncio import AsyncIOMotorClient

from core.config import settings
from core.security import get_password_hash
from crud.base import BaseCRUD
from schemas.user import UserInDB


class UserCRUD(BaseCRUD):
    async def get_by_email(self, db_cli: AsyncIOMotorClient, email: str) -> UserInDB | None:
        user_doc = await super().get(db_cli=db_cli, query={"email": email})
        if user_doc:
            return UserInDB(**user_doc)
        return None

    async def get_by_id(self, db_cli: AsyncIOMotorClient, id: str) -> UserInDB | None:
        user_doc = await super().get_by_id(db_cli=db_cli, id=id)
        if user_doc:
            return UserInDB(**user_doc)
        return None

    async def create(self, *, db_cli: AsyncIOMotorClient, obj_in: UserInDB) -> UserInDB:
        obj_in.password = get_password_hash(obj_in.password)
        return await super().create(obj_in=obj_in, db_cli=db_cli)

    async def create_user(self, *, db_cli: AsyncIOMotorClient, obj_in: UserInDB) -> UserInDB:
        obj_in.is_superuser = False
        return await self.create(obj_in=obj_in, db_cli=db_cli)

    async def create_superuser(self, *, db_cli: AsyncIOMotorClient, obj_in: UserInDB) -> UserInDB:
        obj_in.is_superuser = True
        return await self.create(obj_in=obj_in, db_cli=db_cli)


user = UserCRUD(settings.USER_COLLECTION_NAME)

if __name__ == "__main__":
    async def main():
        print('iner')
        # res = await user.get(db_cli=AsyncIOMotorClient(), query={"_id": ObjectId("66f42cef7b87f794b9d55621")})
        # res = await user.get_by_email(db_cli=AsyncIOMotorClient(), email="john_doe@gmail.com")
        res = await user.get_by_id(db_cli=AsyncIOMotorClient(), id="66f42cef7b87f794b9d55621")
        print(type(res))
        print(res)


    asyncio.run(main())
