from pydantic_settings import BaseSettings
from dotenv import load_dotenv
import os

load_dotenv()


class Settings(BaseSettings):
    # General
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "broword"

    # Database
    DATABASE_NAME: str = PROJECT_NAME
    USER_COLLECTION_NAME: str = "users"
    TASK_COLLECTION_NAME: str = "tasks"
    WORD_COLLECTION_NAME: str = "words"
    ID_FIELD_NAME: str = "id"

    PORT: int = os.getenv("PORT")
    HOST: str = os.getenv("HOST")

    # JWT
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8
    ACCESS_TOKEN_FIELD_NAME: str = "access_token"
    TOKEN_TYPE_FIELD_NAME: str = "token_type"
    BEARER_STR: str = "bearer"
    JWT_SECRET: str = "TEST_SECRET_DO_NOT_USE_IN_PROD"
    ALGORITHM: str = "HS256"


settings = Settings()
