from db.db import db

COLLECTION_NAME = 'settings'


def insert_settings(uuid: str, data: dict) -> int:
    db[COLLECTION_NAME].insert_one({'uuid': uuid, 'data': data})
    return 1


def get_settings_by_uid(uuid: str) -> int:
    return db[COLLECTION_NAME].find(uuid)


def is_uid_exists(uuid):
    if db[COLLECTION_NAME].find(uuid):
        return True
    return False
