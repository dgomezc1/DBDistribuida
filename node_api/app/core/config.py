from pathlib import Path



from app.core.settings import envs, ENVIRONMENT
from app.core.settings import LocalSettings, ProductionSettings

ROOT_DIR = Path(__file__).resolve(strict=True).parent.parent.parent.parent

DATABASE = {}

settings = LocalSettings() if ENVIRONMENT == "local" else ProductionSettings()
