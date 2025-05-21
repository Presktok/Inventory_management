import os
from dotenv import load_dotenv
load_dotenv()

class DevelopmentConfig:
    MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
    MONGO_DBNAME = os.getenv("MONGO_DBNAME", "inventoryDB")
    DEBUG = True
    
