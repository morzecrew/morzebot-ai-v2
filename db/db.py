from pymongo import MongoClient
import os 

MONGODB_HOST = os.getenv('MONGO_HOST', default='localhost')
MONGODB_PORT = os.getenv('MONGO_PORT', default=27017)
MONGODB_USER = os.getenv('MONGO_USER', default='root')
MONGODB_PASSWORD = os.getenv('MONGODB_PASSWORD', default='root')

DB_NAME = os.getenv('DB_NAME', default='mz_bot_ai') 

connection = MongoClient(f'mongodb://{MONGODB_USER}:{MONGODB_PASSWORD}@{MONGODB_HOST}:{MONGO_PORT}/{DB_NAME}')
db = connection[DB_NAME]
