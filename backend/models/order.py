from datetime import datetime
from bson import ObjectId, json_util
import json
from flask import current_app

class Order:
    def __init__(self, order_id, user_id, warehouse_id, items, timestamp=None):
        self.order_id = order_id
        self.user_id = user_id
        self.warehouse_id = warehouse_id
        self.items = items
        self.timestamp = timestamp or datetime.utcnow()
        self.status = "pending"
        self.route = []

    def to_dict(self):
        return {
            'order_id': self.order_id,
            'user_id': self.user_id,
            'warehouse_id': self.warehouse_id,
            'items': self.items,
            'timestamp': self.timestamp,
            'status': self.status,
            'route': self.route
        }

    @staticmethod
    def create(order_data):
        """Create a new order in the database"""
        order_data['created_at'] = datetime.utcnow()
        order_data['status'] = 'pending'
        result = current_app.db.orders.insert_one(order_data)
        return str(result.inserted_id)

    @staticmethod
    def get_all():
        """Get all orders from the database"""
        orders = list(current_app.db.orders.find())
        return json.loads(json_util.dumps(orders))

    @staticmethod
    def get_by_id(order_id):
        """Get an order by its ID"""
        order = current_app.db.orders.find_one({'_id': ObjectId(order_id)})
        return json.loads(json_util.dumps(order)) if order else None

    @staticmethod
    def update_status(order_id, status):
        """Update the status of an order"""
        result = current_app.db.orders.update_one(
            {'_id': ObjectId(order_id)},
            {
                '$set': {
                    'status': status,
                    'updated_at': datetime.utcnow()
                }
            }
        )
        return result.modified_count > 0

    @staticmethod
    def update_route(order_id, route):
        """Update the route of an order"""
        result = current_app.db.orders.update_one(
            {'_id': ObjectId(order_id)},
            {
                '$set': {
                    'route': route,
                    'updated_at': datetime.utcnow()
                }
            }
        )
        return result.modified_count > 0

    @staticmethod
    def get_pending_orders():
        """Get all pending orders"""
        orders = list(current_app.db.orders.find({'status': 'pending'}))
        return json.loads(json_util.dumps(orders))

    @staticmethod
    def get_orders_by_user(user_id):
        """Get all orders for a specific user"""
        orders = list(current_app.db.orders.find({'user_id': user_id}))
        return json.loads(json_util.dumps(orders))

    @staticmethod
    def get_orders_by_warehouse(warehouse_id):
        """Get all orders for a specific warehouse"""
        orders = list(current_app.db.orders.find({'warehouse_id': warehouse_id}))
        return json.loads(json_util.dumps(orders))

    @staticmethod
    def delete(order_id):
        """Delete an order"""
        result = current_app.db.orders.delete_one({'_id': ObjectId(order_id)})
        return result.deleted_count > 0
