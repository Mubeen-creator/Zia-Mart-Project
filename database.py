# app/database.py

from motor.motor_asyncio import AsyncIOMotorClient
from config import MONGODB_URL

# MongoDB connection
client = AsyncIOMotorClient(MONGODB_URL)
database = client['your_database_name']  # Define the database
users_collection = database.get_collection('Zia')  # Collection for user data

# Helper function to get database connection
def get_database():
    return database
