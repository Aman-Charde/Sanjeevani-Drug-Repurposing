"""
Application configuration settings.
"""
from pydantic_settings import BaseSettings
from typing import Optional
import os


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    # API Keys - Google Gemini is the primary (FREE) option
    google_api_key: str = ""
    openai_api_key: Optional[str] = None
    anthropic_api_key: Optional[str] = None
    
    # Application Settings
    debug: bool = True
    log_level: str = "INFO"
    
    # Server Configuration
    host: str = "0.0.0.0"
    port: int = 8000
    
    # LLM Configuration - Using Gemini as default (FREE)
    default_model: str = "gemini-2.0-flash"  # Fast and free
    temperature: float = 0.1
    max_tokens: int = 4096
    
    # Agent Configuration
    max_iterations: int = 10
    agent_timeout: int = 300  # seconds
    
    # Report Configuration
    reports_dir: str = "./reports"
    charts_dir: str = "./charts"
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


# Global settings instance
settings = Settings()


def get_settings() -> Settings:
    """Get application settings."""
    return settings
