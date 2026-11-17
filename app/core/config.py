
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # Application settings
    APP_NAME: str = "Task Management Application"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = False

    # Database settings
    DATABASE_URL: str

    # Authentication settings
    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


settings = Settings()