from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import HttpUrl
from pathlib import Path

CURRENT_FILE_DIR = Path(__file__).resolve().parent

class Settings(BaseSettings):
    app_name: str = 'practice!'
    debug: bool = True

    google_client_id: str
    google_client_secret: str
    google_redirect_uri: HttpUrl

    postgres_host: str = 'localhost'
    postgres_user: str = 'practice_user'
    postgres_password: str
    postgres_database: str = 'practice'

    database_port: int = 5050

    model_config = SettingsConfigDict(
        env_file=CURRENT_FILE_DIR / '../.env',
        env_file_encoding='utf-8',
        extra='ignore')

settings = Settings() #type: ignore