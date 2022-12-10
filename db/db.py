from pymongo import MongoClient
import os 

MONGODB_HOST = os.getenv('MONGO_HOST', default='localhost')
MONGODB_PORT = os.getenv('MONGO_PORT', default=27017)
DB_NAME = os.getenv('DB_NAME', default='mz_bot_ai') 

connection = MongoClient(MONGODB_HOST, MONGODB_PORT)
db = connection[DB_NAME]
