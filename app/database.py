import os
from pymongo import MongoClient
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get the MongoDB URL
MONGO_URL = os.getenv("MONGO_URL", "mongodb://localhost:27017/")

# Create the MongoDB client
client = MongoClient(MONGO_URL)

# Create (or connect to) the database named 'resume_analyzer_db'
db = client["resume_analyzer_db"]

# Optional: Test the connection when the app starts
try:
    client.admin.command('ping')
    print("✅ Successfully connected to MongoDB!")
except Exception as e:
    print(f"❌ Could not connect to MongoDB: {e}")