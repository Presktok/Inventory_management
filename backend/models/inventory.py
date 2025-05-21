from datetime import datetime
from bson import ObjectId, json_util
import json
from flask import current_app
from typing import List

class InventoryItem:
    def __init__(self, name, quantity, category, price, description=None):
        self.name = name
        self.quantity = quantity
        self.category = category
        self.price = price
        self.description = description
        self.created_at = datetime.utcnow()
        self.updated_at = datetime.utcnow()

    @staticmethod
    def create(item_data):
        item_data['created_at'] = datetime.utcnow()
        item_data['updated_at'] = datetime.utcnow()
        result = current_app.db.inventory.insert_one(item_data)
        return str(result.inserted_id)

    @staticmethod
    def get_all():
        items = list(current_app.db.inventory.find())
        # Convert ObjectId to string for JSON serialization
        return json.loads(json_util.dumps(items))

    @staticmethod
    def get_by_id(item_id):
        item = current_app.db.inventory.find_one({'_id': ObjectId(item_id)})
        return json.loads(json_util.dumps(item)) if item else None

    @staticmethod
    def update(item_id, update_data):
        update_data['updated_at'] = datetime.utcnow()
        result = current_app.db.inventory.update_one(
            {'_id': ObjectId(item_id)},
            {'$set': update_data}
        )
        return result.modified_count > 0

    @staticmethod
    def delete(item_id):
        result = current_app.db.inventory.delete_one({'_id': ObjectId(item_id)})
        return result.deleted_count > 0

    @staticmethod
    def search(query):
        items = list(current_app.db.inventory.find({
            '$or': [
                {'name': {'$regex': query, '$options': 'i'}},
                {'category': {'$regex': query, '$options': 'i'}},
                {'description': {'$regex': query, '$options': 'i'}}
            ]
        }))
        return json.loads(json_util.dumps(items))

    @staticmethod
    def update_stock(item_name, quantity_change):
        """
        Update the stock quantity of an item.
        Positive quantity_change means adding stock (factory to warehouse)
        Negative quantity_change means reducing stock (warehouse to user)
        """
        # First check if the item exists and get its current quantity
        item = current_app.db.inventory.find_one({'name': item_name})
        if not item:
            # If item doesn't exist and we're adding stock, create it
            if quantity_change > 0:
                current_app.db.inventory.insert_one({
                    'name': item_name,
                    'quantity': quantity_change,
                    'category': 'Uncategorized',
                    'price': 0.0,  # Default price
                    'created_at': datetime.utcnow(),
                    'updated_at': datetime.utcnow()
                })
                return True
            else:
                raise ValueError(f"Item '{item_name}' not found in inventory")
        
        # For reducing stock, check if we have enough
        if quantity_change < 0 and item['quantity'] + quantity_change < 0:
            raise ValueError(f"Insufficient stock for {item_name}. Available: {item['quantity']}, Requested: {abs(quantity_change)}")
        
        # Update the stock
        result = current_app.db.inventory.update_one(
            {'name': item_name},
            {
                '$inc': {'quantity': quantity_change},
                '$set': {'updated_at': datetime.utcnow()}
            }
        )
        
        if result.modified_count == 0:
            raise ValueError(f"Failed to update stock for item '{item_name}'")
        
        return True

    def find_optimal_factory_warehouse_route(self, factory_id: str) -> List[str]:
        # Create edges for Kruskal's algorithm
        edges = []
        for warehouse_id in self.warehouses:
            distances, _ = self.graph.dijkstra(factory_id)
            if warehouse_id in distances:
                edges.append((factory_id, warehouse_id, distances[warehouse_id]))

        # Get minimum spanning tree
        vertices = self.warehouses | {factory_id}
        mst = kruskal_mst(vertices, edges)
        
        # Convert MST to route
        route = []
        for edge in mst:
            route.extend(self.graph.get_shortest_path(edge[0], edge[1]))
        
        return route 