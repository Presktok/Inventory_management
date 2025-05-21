from pymongo import MongoClient

def init_db(app):
    try:
        client = MongoClient(app.config['MONGO_URI'])
        db_name = app.config.get('MONGO_DBNAME', 'inventoryDB')  # fallback if not set
        app.db = client[db_name]
        print("MongoDB connected successfully")
    except Exception as e:
        print(f"MongoDB connection error: {e}")
        raise e
    
