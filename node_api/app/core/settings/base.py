from typing import Dict, List

import environ
from pydantic import BaseSettings

envs = environ.Env()

ENVIRONMENT: str = envs("ENV", default="local")

class BaseAppSettings(BaseSettings):
    PREFIX: str = ''
    APP_NAME: str = 'node-api'
    VERSION: str = '0.1.0'
    ID = envs("ID")
    ORIGINS: List[str] = envs.list("ALLOWED_ORIGINS", default=[])
