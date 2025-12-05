from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    # Database
    DATABASE_URL: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    
    # OpenWeather API
    OPENWEATHER_API_KEY: str
    OPENWEATHER_BASE_URL: str
    CITY_NAME: str
    
    # App Settings
    APP_NAME: str = "Weather Monitoring System"
    DEBUG: bool = True
    
    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()
