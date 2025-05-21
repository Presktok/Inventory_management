from flask import Blueprint, jsonify, current_app
from datetime import datetime

api_bp = Blueprint('api', __name__)

@api_bp.route('/test-db', methods=['GET'])
def test_db():
    try:
        db = current_app.db  # ✅ Use current_app here too
        print("Database connected:", db.name)
        test_collection = db.test
        test_doc = {"name": "test", "timestamp": datetime.utcnow()}
        test_collection.insert_one(test_doc)
        documents = list(test_collection.find({}, {'_id': 0}))
        return jsonify({"status": "success", "data": documents}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500
