from typing import Optional

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path
import os

# Get the project root directory (two levels up from config/settings.py)
ROOT_DIR = Path(__file__).resolve().parent.parent
ENV_PATH = os.path.join(ROOT_DIR, ".env")

class OmniSettings(BaseSettings):
    UI_BASE_URL: str
    API_BASE_URL: str

    # Credentials for Notes App identity
    USER_EMAIL: str
    USER_PASSWORD: str
    USER_EMAIL_2:str
    USER_PASSWORD_2:str

    # Optional token for Phase 3.3 Hybrid Bridge
    AUTH_TOKEN: Optional[str] = None

    # Browser config for WSL/Ubuntu environment
    BROWSER_HEADLESS: bool = True
    SLOW_MO: int = 0
    BROWSER_TYPE: str = "chromium"

    # Tell Pydantic to look for a .env file
    model_config = SettingsConfigDict(
        env_file=ENV_PATH,
        env_file_encoding="utf-8",
        extra="ignore" # Ignores extra variables in .env not defined here
    )

# Singleton instance to be used across the framework
settings = OmniSettings()