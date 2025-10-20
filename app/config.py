from __future__ import annotations
from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    app_name: str = "Car Finder"
    environment: str = "development"

    # CORS
    cors_origins: List[str] = [
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost",
        "*",
    ]

    # Provider toggles/keys
    enable_mock_provider: bool = True

    # Optional: third-party provider keys (not required for mock)
    serpapi_key: str | None = None
    autotempest_key: str | None = None

    # AI summary
    openai_api_key: str | None = None
    openai_model: str = "gpt-4o-mini"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()  # type: ignore
