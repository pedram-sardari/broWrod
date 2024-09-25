from pydantic_settings import BaseSettings
from dotenv import load_dotenv
import os

load_dotenv()


class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "broword"
    DATABASE_NAME: str = PROJECT_NAME
    USER_COLLECTION_NAME: str = "users"
    WORD_COLLECTION_NAME: str = "words"
    ID_FIELD_NAME: str = "id"
    PORT: int = os.getenv("PORT")
    HOST: str = os.getenv("HOST")


settings = Settings()
