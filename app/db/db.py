# db.py
from motor.motor_asyncio import AsyncIOMotorClient
from config import MONGO_CONNECTION_STRING, MONGO_DB

class Database:
    client: AsyncIOMotorClient = None

db = Database()

async def connect_to_mongo():
    db.client = AsyncIOMotorClient(MONGO_CONNECTION_STRING)
    db.database = db.client[MONGO_DB]
    print("Connected to MongoDB")
    print("Database Name: ", db.database.name)

async def close_mongo_connection():
    db.client.close()
    print("Closed MongoDB connection")
