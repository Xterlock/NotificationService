from pydantic import BaseModel
from pydantic_settings import BaseSettings

DELIMITER: str = "__"


class AppSettings(BaseModel):
    """Настройки приложения"""
    title: str
    host: str = "127.0.0.1"
    port: int = 8080


class Settings(BaseSettings):
    """Базовый класс настроек"""
    app: AppSettings

    class Config:
        env_nested_delimiter = DELIMITER
