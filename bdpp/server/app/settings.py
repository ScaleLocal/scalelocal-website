"""BD++ backend settings — loaded from environment / .env."""
from __future__ import annotations
import os
from functools import lru_cache
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database_url: str = "sqlite+aiosqlite:///./bdpp.db"
    redis_url: str = "redis://localhost:6379/0"
    outscraper_token: str = ""
    millionverifier_token: str = ""
    apollo_api_key: str = ""
    google_api_key: str = ""
    google_cse_id: str = ""
    anthropic_api_key: str = ""
    default_max_spend_usd: float = 6.0

    class Config:
        env_file = ".env"
        case_sensitive = False
        extra = "ignore"


@lru_cache
def get_settings() -> Settings:
    return Settings()
