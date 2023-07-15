import os
from logging import config as logging_config
from typing import List, Optional

from pydantic_settings import BaseSettings

from .logger import LOGGING

logging_config.dictConfig(LOGGING)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__name__)))


class AppSettings(BaseSettings):
    app_title: str = "App"
    database_dsn: str = ...
    project_host: str = "127.0.0.1"
    project_port: int = 8000
    api_v1_prefix: str = "/api/v1"
    short_url_pattern: str = f"http://{project_host}:{project_port}{api_v1_prefix}/"
    black_list: List[Optional[str]] = []
    db_engine_echo: bool = False

    class Config:
        env_file = "../.env"


app_settings = AppSettings()
