"""
Database connection for ScoreShield
MongoDB connection setup
"""

from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.errors import ConnectionFailure
import os
from dotenv import load_dotenv

load_dotenv()

# MongoDB connection settings
MONGODB_URL = os.getenv("MONGODB_URL", "mongodb://localhost:27017")
DATABASE_NAME = os.getenv("DATABASE_NAME", "scoreshield")

# Global database client
client = None
database = None

async def connect_to_mongo():
    """Connect to MongoDB"""
    global client, database
    try:
        client = AsyncIOMotorClient(MONGODB_URL)
        database = client[DATABASE_NAME]
        # Test the connection
        await client.admin.command('ping')
        print(f"Connected to MongoDB: {DATABASE_NAME}")
    except ConnectionFailure as e:
        print(f"Failed to connect to MongoDB: {e}")
        raise

async def close_mongo_connection():
    """Close MongoDB connection"""
    global client
    if client:
        client.close()
        print("MongoDB connection closed")

def get_database():
    """Get database instance"""
    return database

def get_collection(collection_name: str):
    """Get collection from database"""
    return database[collection_name]
