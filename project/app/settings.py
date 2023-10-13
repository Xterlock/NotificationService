from typing import Optional

from pydantic import BaseModel, AnyUrl
from pydantic_settings import BaseSettings

DELIMITER: str = "__"

STATIC_DIR = "static"


class DatabaseSetting(BaseModel):
    driver: str = "postgresql+asyncpg"
    host: str
    port: int
    user: str
    password: str
    db_name: str

    def get_url(self, driver: Optional[str] = None) -> str:
        """
        Получить url для подключение к бд
        :param driver: драйвер взаимодействия с бд
        """
        d = driver if driver else self.driver
        return f'{d}://{self.user}:{self.password}@{self.host}:{self.port}/{self.db_name}'


class RedisSettings(BaseModel):
    """Настройки Redis"""
    host: str
    port: str
    db: int

    def get_url_redis(self) -> str:
        return f"redis://{self.host}:{self.port}/{self.db}"


class AppSettings(BaseModel):
    """Настройки приложения"""
    title: str
    host: str = "127.0.0.1"
    port: int = 8080


class Settings(BaseSettings):
    """Базовый класс настроек"""
    app: AppSettings
    db: DatabaseSetting
    cache: RedisSettings

    class Config:
        env_nested_delimiter = DELIMITER


base_setting = Settings()
