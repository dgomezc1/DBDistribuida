import copy
import json

from app.core.config import DB_PERSISTENT_DIR, DATABASE, settings

class KeyAlreadyExistsError(Exception):
    pass

class NoSuchKeyError(Exception):
    pass


class Database:

    def __init__(self):
        self.location = DB_PERSISTENT_DIR
        if not self.location.exists():
            self.location.touch()

    def _persist(self):
        try:
            to_persist: dict = copy.deepcopy(DATABASE)
            del to_persist["PING"]
            json.dump(to_persist, self.location.open("w"))
        except:
            print("[ERROR] Error persisting database values")

    def _write_base(self, key, value):
        DATABASE[key] = value
        self._persist()

    def save(self, key, value, *args, **kwargs):
        if key in DATABASE:
            raise KeyAlreadyExistsError(f"Key: {key} already exists in db.")
        self._write_base(key, value)

    def update(self, key, value, *args, **kwargs):
        if not key in DATABASE:
            raise NoSuchKeyError(f"Key: {key} does not exists in db.")
        self._write_base(key, value)

    def get(self, key, *args, **kwargs):
        if not key in DATABASE:
            raise NoSuchKeyError(f"Key: {key} does not exists in db.")
        return DATABASE[key]

    def delete(self, key, *args, **kwargs):
        if not key in DATABASE:
            raise NoSuchKeyError(f"Key: {key} does not exists in db.")
        del DATABASE[key]

    def get_keys(self, *args, **kwargs):
        result = list(DATABASE.keys())
        if "PING" in result:
            result.remove("PING")
        return result
