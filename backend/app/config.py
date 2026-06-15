import os

from dotenv import load_dotenv

load_dotenv(override=True)

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    openai_api_key: str = os.getenv("OPENAI_API_KEY", "")
    database_url: str = os.getenv("DATABASE_URL", "")
    google_api_key:str = os.getenv("GOOGLE_API_KEY", "")
    

    @property
    def async_database_url(self) -> str:
        url = self.database_url
        # remove uncompatible query parameters
        url = url.split("?")[0]
        # switch to async driver
        url = url.replace("postgresql://", "postgresql+asyncpg://")
        return url


settings = Settings()

print(f"DATABASE_URL raw: {os.getenv('DATABASE_URL')}")
