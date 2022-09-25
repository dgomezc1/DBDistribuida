import copy
import json
import requests

from app.core.config import REPLICATION_DATABASE, REPLICATION_DB_PERSISTENT_DIR


def insert_keys(node_url):
    inserted_keys = []
    for key, value in REPLICATION_DATABASE["not-replicated"].items():
        response = requests.post(
            f"{node_url}/db",
            json={"key": key, "value": value, "is_restore": True}
        )
        if response.status_code != 201:
            print(f"[ERROR] Error restoring: inserting {key} key")
        else:
            inserted_keys.append((key, value))
    return inserted_keys

def delete_keys(node_url):
    deleted_keys = []
    for key in REPLICATION_DATABASE["eliminations"]:
        response = requests.delete(f"{node_url}/db/{key}", json={"is_restore": True})
        if response.status_code != 204:
            print(f"[ERROR] Error restoring: deleteing {key} key")
            continue
        deleted_keys.append(key)
    for key in deleted_keys:
        REPLICATION_DATABASE["eliminations"].remove(key)
    if REPLICATION_DATABASE["eliminations"]:
        print(f"Pending eliminations: {REPLICATION_DATABASE['eliminations']}")

def move_keys(inserted_keys):
    for key, value in inserted_keys:
        del REPLICATION_DATABASE["not-replicated"][key]
        REPLICATION_DATABASE["replicated"][key] = value

def main(node_url):
    inserted_keys = insert_keys(node_url)
    move_keys(inserted_keys)
    delete_keys(node_url)
    try:
        to_persist: dict = copy.deepcopy(REPLICATION_DATABASE)
        if "PING" in to_persist:
            del to_persist["PING"]
        json.dump(to_persist, REPLICATION_DB_PERSISTENT_DIR.open("w"))
    except:
        print(f"[ERROR-REPLICATION_DB_PERSISTENT_DIR] Error persisting database values")