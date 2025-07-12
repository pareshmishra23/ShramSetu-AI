from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# MongoDB connection
mongo_url = os.environ.get('MONGO_URL', 'mongodb://localhost:27017')
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ.get('DB_NAME', 'shramsetu_db')]

def init_db():
    """Initialize database connection"""
    try:
        # Test the connection
        client.admin.command('ping')
        print("Connected to MongoDB successfully!")
    except Exception as e:
        print(f"Failed to connect to MongoDB: {e}")
        raise e

# Collections
laborers_collection = db.laborers