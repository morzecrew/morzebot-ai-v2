from pymongo import MongoClient

MONGODB_HOST = 'localhost'
MONGODB_PORT = 27017
DB_NAME = 'mz_bot_ai'

connection = MongoClient(MONGODB_HOST, MONGODB_PORT)
db = connection[DB_NAME]
