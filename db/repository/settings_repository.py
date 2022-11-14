from db.db import db
from typing import LiteralString

COLLECTION_NAME = 'settings'


def insert_settings(uuid: LiteralString, data: dict) -> int:
    if is_uuid_exists(uuid):
        db[COLLECTION_NAME].update_one({"uuid": uuid}, {"$set": {"data": data}})
    else:
        db[COLLECTION_NAME].insert_one({"uuid": uuid, "data": data})
    return 1


def get_settings_by_uuid(uuid: LiteralString) -> int:
    return db[COLLECTION_NAME].find_one({"uuid": uuid})


def is_uuid_exists(uuid: LiteralString):
    if db[COLLECTION_NAME].find_one({"uuid": uuid}):
        return True
    return False
