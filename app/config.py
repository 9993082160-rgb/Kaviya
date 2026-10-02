from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    gemini_api_key: str = ""
    gemini_model: str = "gemini-2.5-flash"
    debug: bool = True
    host: str = "127.0.0.1"
    port: int = 8000
    session_secret: str = "change-this-secret-key"
    cookie_secure: bool = False
    database_url: str = "sqlite:///./pocketsmart.db"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


settings = Settings()