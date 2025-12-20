from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path
import os

# Get the project root directory (two levels up from config/settings.py)
ROOT_DIR = Path(__file__).resolve().parent.parent
ENV_PATH = os.path.join(ROOT_DIR, ".env")

class OmniSettings(BaseSettings):
    # Use Field with validation_alias to support both .env and OS env vars
    UI_BASE_URL: str = Field(default="https://practice.expandtesting.com")
    API_BASE_URL: str = Field(default="https://practice.expandtesting.com/api")

    # Credentials (Required - Pydantic will throw error if missing from .env)
    USER_NAME: str
    PASSWORD: str

    # Browser Settings
    BROWSER_HEADLESS: bool = True
    SLOW_MO: int = 0  # Useful for debugging UI

    # Tell Pydantic to look for a .env file
    model_config = SettingsConfigDict(
        env_file=ENV_PATH,
        env_file_encoding="utf-8",
        extra="ignore" # Ignores extra variables in .env not defined here
    )

# Singleton instance to be used across the framework
settings = OmniSettings()