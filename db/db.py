from pymongo import MongoClient
import os 

MONGO_URL = os.getenv('MONGO_URL', default='mongodb://localhost:27017/mz_bot_ai')

connection = MongoClient(MONGO_URL)
db = connection[DB_NAME]
