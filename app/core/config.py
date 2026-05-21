"""
NEXUS Core Configuration

All application settings are defined here and loaded from environment variables.
Nothing else in the codebase reads from os.environ directly.
This is the single source of truth for configuration.
"""

from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field
from functools import lru_cache


class Settings(BaseSettings):
    """
    Application settings loaded from environment variables.

    pydantic-settings automatically reads from:
    1. Environment variables
    2. .env file (specified in model_config)

    Field names map directly to env var names (case-insensitive).
    """

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # Application
    app_name: str = Field(default="NEXUS")
    app_version: str = Field(default="0.1.0")
    debug: bool = Field(default=False)

    # Provider routing
    primary_provider: str = Field(default="anthropic")
    fallback_provider: str = Field(default="ollama")

    # Anthropic
    anthropic_api_key: str = Field(default="")
    anthropic_model: str = Field(default="claude-sonnet-4-5")

    # Ollama
    ollama_base_url: str = Field(default="http://localhost:11434")
    ollama_model: str = Field(default="llama3.2:1b")


@lru_cache
def get_settings() -> Settings:
    """
    Returns cached settings instance.

    lru_cache ensures we only read and parse the .env file once,
    no matter how many times get_settings() is called across the app.
    This is a performance optimization and also ensures consistency —
    every part of the app sees the same config object.
    """
    return Settings()