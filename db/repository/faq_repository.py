from db.db import db

COLLECTION_NAME = 'faq'


def is_faq_dataset_exists(criteria: object):
    return db[COLLECTION_NAME].count_documents(criteria)


def insert_faq_dataset(uuid: str, data: bytes):
    result = db[COLLECTION_NAME].insert_one({'uuid': uuid, 'data': data})
    return result.inserted_id


def insert_new_string(uuid: str, data: str):
    if is_faq_dataset_exists({'uuid': uuid}):
        db[COLLECTION_NAME].update_one({'uuid': uuid}, {"$set": {"data": data}})
    else:
        db[COLLECTION_NAME].insert_one({'uuid': uuid, 'data': data})


def get_faq_dataset_by_uuid(uuid: str) -> int:
    return db[COLLECTION_NAME].find_one({"uuid": uuid})


