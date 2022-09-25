import json
from pathlib import Path



from app.core.settings import envs, ENVIRONMENT
from app.core.settings import LocalSettings, ProductionSettings

ROOT_DIR = Path(__file__).resolve(strict=True).parent.parent.parent.parent

DATABASE = { "PING": "PONG" }
REPLICATION_DATABASE = {
    "replicated": {},
    "not-replicated": {},
    "eliminations": []
}

settings = LocalSettings() if ENVIRONMENT == "local" else ProductionSettings()

DB_PERSISTENT_DIR = ROOT_DIR.joinpath(f"db/db_{settings.ID}.json")
if DB_PERSISTENT_DIR.exists():
    with DB_PERSISTENT_DIR.open("r") as f:
        try:
            _data = json.load(f)
        except:
            _data = {}
        DATABASE = {**DATABASE, **_data}

REPLICATION_DB_PERSISTENT_DIR = ROOT_DIR.joinpath(f"db/replications/dbr_{settings.ID}.json")
if REPLICATION_DB_PERSISTENT_DIR.exists():
    with REPLICATION_DB_PERSISTENT_DIR.open("r") as f:
        try:
            _data = json.load(f)
        except:
            _data = {}
        REPLICATION_DATABASE = {**REPLICATION_DATABASE, **_data}
