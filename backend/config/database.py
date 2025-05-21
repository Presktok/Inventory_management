from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Get MongoDB connection string from environment variable
MONGO_URI = os.getenv('MONGO_URI', 'mongodb://localhost:27017')

def init_db(app):
    try:
        # Create MongoDB client with proper options
        client = MongoClient(
            app.config['MONGO_URI'],
            serverSelectionTimeoutMS=5000,  # 5 second timeout
            connectTimeoutMS=5000,
            socketTimeoutMS=5000
        )
        
        # Test the connection
        client.admin.command('ping')
        
        # Get database instance
        db_name = app.config.get('MONGO_DBNAME', 'inventoryDB')
        app.db = client[db_name]
        
        # Initialize collections
        app.db.inventory = app.db.get_collection('inventory')
        app.db.users = app.db.get_collection('users')
        app.db.transactions = app.db.get_collection('transactions')
        
        print("MongoDB connected successfully to database:", db_name)
        
    except ConnectionFailure as e:
        print(f"MongoDB connection error: {e}")
        raise Exception(f"Failed to connect to MongoDB: {e}")
    except Exception as e:
        print(f"MongoDB initialization error: {e}")
        raise e
    
