from pydantic_settings import BaseSettings, SettingsConfigDict


class __Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    jwt_secret_key: str = "not_so_secure_secret"
    jwt_algorithm: str = "HS256"
    jwt_expire_minutes: int = 30
    database_url: str = "sqlite:///database.db"


settings = __Settings()
