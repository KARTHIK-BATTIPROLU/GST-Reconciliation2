"""
Centralized configuration management using Pydantic Settings.
Validates environment variables at startup.
"""

from functools import lru_cache
from typing import List
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    # App
    APP_NAME: str = "GST Reconciliation"
    DEBUG: bool = False
    
    # Backend
    PORT: int = 8001
    HOST: str = "0.0.0.0"
    ALLOWED_ORIGINS: List[str] = ["http://localhost:8501", "http://localhost:8502"]

    # Database - MongoDB
    MONGO_URI: str
    MONGO_DB_NAME: str = "gst_reconciliation"
    
    # Database - Neo4j
    NEO4J_URI: str
    NEO4J_USER: str
    NEO4J_PASSWORD: str

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

@lru_cache()
def get_settings():
    return Settings()
