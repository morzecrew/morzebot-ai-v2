from pymongo import MongoClient
import os 

MONGO_HOST = os.getenv('MONGO_HOST', default='localhost')
MONGO_PORT = os.getenv('MONGO_PORT', default=27017)
MONGO_USER = os.getenv('MONGO_USER', default='root')
MONGO_PASSWORD = os.getenv('MONGO_PASSWORD', default='root')

DB_NAME = os.getenv('DB_NAME', default='mz_bot_ai') 

connection = MongoClient(f'mongodb://{MONGO_USER}:{MONGO_PASSWORD}@{MONGO_HOST}:{MONGO_PORT}/{DB_NAME}')
db = connection[DB_NAME]
