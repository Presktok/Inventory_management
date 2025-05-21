from pymongo import MongoClient

def init_db(app):
    client = MongoClient(app.config['MONGO_URI'])
    db = client.get_default_database()
    app.db = db  # ✅ Attach the db to the app
    
