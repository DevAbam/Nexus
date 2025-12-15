from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    DATABASE_URL: str
    IMAGEKIT_PRIVATE_KEY: str
    IMAGEKIT_PUBLIC_KEY: str
    IMAGEKIT_URL: str
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()
