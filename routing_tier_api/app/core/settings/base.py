from typing import Dict, List

import environ
from pydantic import BaseSettings

from app.node.node import Node

envs = environ.Env()

ENVIRONMENT: str = envs("ENV", default="local")

class BaseAppSettings(BaseSettings):
    PREFIX: str = ''
    APP_NAME: str = 'routing-tier-api'
    VERSION: str = '0.1.0'
    ORIGINS: List[str] = envs.list("ALLOWED_ORIGINS", default=[])
    MAX_KEYS: int = int("9"+"0"*47) # 14 | 48
    NODES: List[Node] = []
    LIST_OF_NODE_HOSTS: List[str] = envs.list("NODE_HOSTS", default=[])
