"""
Config file for the backend. config + .env file
"""
from pydantic_settings import BaseSettings
from typing import List
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent
ENV_FILE_PATH = BASE_DIR / ".env"
class Settings(BaseSettings):
    # Fixer API
    fixer_api_key: str = "hftPFkNydW1Ny8oIpc6IKaQbpXRVCC26"
    fixer_api_url: str = "https://api.apilayer.com/fixer"
    # Server
    port: int = 8000
    host: str = "0.0.0.0"    
    # CORS (0.0.0.0都可以)
    frontend_url: str = "http://localhost:3000"
    
    @property
    def cors_origins(self) -> List[str]:
        return [
            self.frontend_url,
            "http://localhost:3000",
            "http://127.0.0.1:3000",
        ]
    
    class Config:
        env_file = str(ENV_FILE_PATH) if ENV_FILE_PATH.exists() else None
        env_file_encoding = 'utf-8'
        case_sensitive = False


# Global Setting Instance，要嚮其他文件引入呢個Instance
settings = Settings()

