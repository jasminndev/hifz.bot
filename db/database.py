import os
from dataclasses import dataclass

from dotenv import load_dotenv

load_dotenv()


@dataclass
class DatabaseConfig:
    DB_USER: str = os.getenv("DB_USER")
    DB_PASS: str = os.getenv("DB_PASS")
    DB_HOST: str = os.getenv("DB_HOST")
    DB_PORT: str = os.getenv("DB_PORT")
    DB_NAME: str = os.getenv("DB_NAME")

    @property
    def db_url(self) -> str:
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"


@dataclass
class BotConfig:
    BOT_TOKEN: str = os.getenv("BOT_TOKEN")
    ADMIN_IDS: list[int] = None

    def __post_init__(self):
        ids = os.getenv("ADMIN_IDS", "")
        self.ADMIN_IDS = [int(i.strip()) for i in ids.split(",") if i.strip()]


@dataclass
class Configuration:
    db = DatabaseConfig()
    bot = BotConfig()


conf = Configuration()
