from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional

class Settings(BaseSettings):
    # App config
    APP_NAME: str = "Financial Planner AI"
    DEBUG_MODE: bool = False
    
    # DB Config
    DATABASE_URL: str = "sqlite:///./financial_data.db"
    CORS_ORIGINS: str = "http://localhost:3000"
    
    # API Keys
    GOOGLE_API_KEY: Optional[str] = None
    
    # Load from .env file securely
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

# Instantiate the global settings object for immediate application use
settings = Settings()
