from pymongo import MongoClient
import os 

MONGO_URL = os.getenv('MONGO_URL', default='mongodb://localhost:27017/mz_bot_ai')
DB_NAME = os.getenv('MONGO_DB_NAME', default='mz_bot_ai')

connection = MongoClient(MONGO_URL)
db = connection[DB_NAME]
