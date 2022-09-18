import json
from typing import List
from pathlib import Path
from threading import RLock

from app.core.settings import envs, ENVIRONMENT
from app.core.settings import LocalSettings, ProductionSettings

ROOT_DIR = Path(__file__).resolve(strict=True).parent.parent.parent.parent

settings = LocalSettings() if ENVIRONMENT == "local" else ProductionSettings()

lock = RLock()
