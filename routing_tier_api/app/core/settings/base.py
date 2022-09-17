from typing import Dict, List

import environ
from pydantic import BaseSettings

envs = environ.Env()

ENVIRONMENT: str = envs("ENV", default="local")

class BaseAppSettings(BaseSettings):
    PREFIX: str = ''
    APP_NAME: str = 'routing-tier-api'
    VERSION: str = '0.1.0'
    ORIGINS: List[str] = envs.list("ALLOWED_ORIGINS", default=[])
    MAX_KEYS: int = int("14"+"0"*48)
    NODE_HOSTS: List[str] = envs.list("NODES", default=[])
