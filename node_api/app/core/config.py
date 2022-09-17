import json
from pathlib import Path



from app.core.settings import envs, ENVIRONMENT
from app.core.settings import LocalSettings, ProductionSettings

ROOT_DIR = Path(__file__).resolve(strict=True).parent.parent.parent.parent

DATABASE = { "PING": "PONG" }

settings = LocalSettings() if ENVIRONMENT == "local" else ProductionSettings()

DB_PERSISTENT_DIR = ROOT_DIR.joinpath(f"db/db_{settings.ID}.json")
if DB_PERSISTENT_DIR.exists():
    with DB_PERSISTENT_DIR.open("r") as f:
        _data = json.load(f)
        DATABASE = {**DATABASE, **_data}