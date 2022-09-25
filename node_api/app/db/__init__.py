import copy
import json

import requests

from app.core.config import DB_PERSISTENT_DIR, DATABASE, settings
from app.core.config import REPLICATION_DB_PERSISTENT_DIR, REPLICATION_DATABASE

class KeyAlreadyExistsError(Exception):
    pass

class NoSuchKeyError(Exception):
    pass


class DBBase:

    def __init__(self, db_name, location, is_replication_db=False):
        self.db_name = db_name
        self.db = globals().get(db_name)
        self.location = location
        self.is_replication_db = is_replication_db
        if not self.location.exists():
            self.location.touch()

    def _persist(self):
        try:
            to_persist: dict = copy.deepcopy(self.db)
            if "PING" in to_persist:
                del to_persist["PING"]
            json.dump(to_persist, self.location.open("w"))
        except:
            print(f"[ERROR-{self.db_name}] Error persisting database values")

    def _write_base(self, key, value, replication_url, is_restore = False, *args, **kwargs):
        self.db[key] = value
        self._persist()
        if not self.is_replication_db and not is_restore:
            response = requests.post(f"{replication_url}/db/replication", json={"key": key, "value": value})
            if response.status_code != 201:
                print(f"[ERROR] Replication for {key} key failed")

    def save(self, key, value, replication_url, insert_type: int = 0, is_restore=False, *args, **kwargs):
        self._write_base(key, value, replication_url, insert_type=insert_type, is_restore=is_restore)


    def update(self, key, value, *args, **kwargs):
        if not key in DATABASE:
            raise NoSuchKeyError(f"Key: {key} does not exists in {self.db_name} db.")
        self._write_base(key, value)

    def get(self, key, *args, **kwargs):
        if not key in self.db:
            raise NoSuchKeyError(f"Key: {key} does not exists in {self.db_name} db.")
        return self.db[key]

    def delete(self, key, replication_url, is_restore=False, *args, **kwargs):
        if not key in self.db:
            raise NoSuchKeyError(f"Key: {key} does not exists in {self.db_name} db.")
        del self.db[key]
        if not self.is_replication_db and not is_restore:
            response = requests.delete(f"{replication_url}/db/replication/{key}", json={})
            if response.status_code != 204:
                print(f"[ERROR] Replication for {key} key failed")
        self._persist()

    def get_keys(self, *args, **kwargs):
        result = list(self.db.keys())
        if "PING" in result:
            result.remove("PING")
        return result


class Database(DBBase):

    def __init__(self):
        super().__init__("DATABASE", DB_PERSISTENT_DIR)


class ReplicationDatabase(DBBase):

    def __init__(self):
        super().__init__("REPLICATION_DATABASE", REPLICATION_DB_PERSISTENT_DIR, True)

    def _write_base(self, key, value, replication_url, insert_type: int = 0, *args, **kwargs):
        self.db["replicated" if insert_type == 0 else "not-replicated"][key] = value
        self._persist()
        """if not self.is_replication_db:
            response = requests.post(replication_url, json={"key": key, "value": value})
            if response.status_code != 201:
                print(f"[ERROR] Replication for {key} key failed")"""

    def get(self, key, *args, **kwargs):
        if value := self.db["replicated"].get(key):
            return value

        if value := self.db["not-replicated"].get(key):
            return value

        raise NoSuchKeyError(f"Key: {key} does not exists in {self.db_name} db.")

    def delete(self, key, insert_type: int = 0, *args, **kwargs):
        if key in self.db["replicated"]:
            if insert_type:
                self.db["eliminations"].append(key)
            del self.db["replicated"][key]
            self._persist()
            return

        if key in self.db["not-replicated"]:
            del self.db["not-replicated"][key]
            self._persist()
            return

        raise NoSuchKeyError(f"Key: {key} does not exists in {self.db_name} db.")

    def get_keys(self, *args, **kwargs):
        result = list(self.db["replicated"].keys()) + list(self.db["not-replicated"].keys())
        if "PING" in result:
            result.remove("PING")
        return result

