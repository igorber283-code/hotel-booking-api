from typing import Optional
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_HOST: str
    POSTGRES_PORT: int

    POSTGRES_DB: str
    POSTGRES_TEST_DB: Optional[str] = None  # 👈 важно

    SECRET_KEY: str
    ALGORITHM: str

    @property
    def DATABASE_URL(self) -> str:
        return (
            f"postgresql+asyncpg://{self.POSTGRES_USER}:"
            f"{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:"
            f"{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
        )

    @property
    def TEST_DATABASE_URL(self) -> str:
        if not self.POSTGRES_TEST_DB:
            raise RuntimeError(
                "POSTGRES_TEST_DB is not set. It is required only for running tests."
            )

        return (
            f"postgresql+asyncpg://{self.POSTGRES_USER}:"
            f"{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:"
            f"{self.POSTGRES_PORT}/{self.POSTGRES_TEST_DB}"
        )

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()
