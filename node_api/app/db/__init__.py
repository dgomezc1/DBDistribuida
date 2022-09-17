import json

from app.core.config import ROOT_DIR, DATABASE, settings

class KeyAlreadyExistsError(Exception):
    pass

class NoSuchKeyError(Exception):
    pass


class Database:

    def __init__(self):
        self.location = ROOT_DIR.joinpath(f"db/db_{settings.ID}.json")
        if not self.location.exists():
            self.location.touch()

    def persist(self):
        try:
            json.dump(DATABASE, self.location.open("w"))
        except:
            print("[ERROR] Error persisting database values")

    def write_base(self, key, value):
        DATABASE[key] = value
        self.persist()

    def save(self, key, value):
        if key in DATABASE:
            raise KeyAlreadyExistsError(f"Key: {key} already exists in db.")
        self.write_base(key, value)

    def update(self, key, value):
        if not key in DATABASE:
            raise NoSuchKeyError(f"Key: {key} does not exists in db.")
        self.write_base(key, value)

    def get(self, key):
        if not key in DATABASE:
            raise NoSuchKeyError(f"Key: {key} does not exists in db.")
        return DATABASE[key]

    def delete(self, key):
        if not key in DATABASE:
            raise NoSuchKeyError(f"Key: {key} does not exists in db.")
        del DATABASE[key]
