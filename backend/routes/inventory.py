from flask import Blueprint, request, jsonify
from datetime import datetime
from bson import ObjectId
from backend.models.inventory import InventoryItem
from backend.algorithms.order_routing import OrderRouter, Order
import json
from bson import json_util
from flask import current_app

inventory_bp = Blueprint('inventory', __name__)
router = OrderRouter()

# Initialize some example locations (you would typically load these from a database)
EXAMPLE_LOCATIONS = {
    'factory1': ('factory', (28.6139, 77.2090)),  # Delhi
    'warehouse1': ('warehouse', (19.0760, 72.8777)),  # Mumbai
    'warehouse2': ('warehouse', (22.5726, 88.3639)),  # Kolkata
    'user1': ('user', (12.9716, 77.5946)),  # Bangalore
    'user2': ('user', (17.3850, 78.4867))  # Hyderabad
}

# Initialize the router with example locations
for loc_id, (loc_type, coords) in EXAMPLE_LOCATIONS.items():
    router.add_location(loc_id, loc_type)

# Add example routes (you would typically load these from a database)
for loc1 in EXAMPLE_LOCATIONS:
    for loc2 in EXAMPLE_LOCATIONS:
        if loc1 != loc2:
            lat1, lng1 = EXAMPLE_LOCATIONS[loc1][1]
            lat2, lng2 = EXAMPLE_LOCATIONS[loc2][1]
            # Simple distance calculation (this should be replaced with proper distance calculation)
            distance = ((lat2-lat1)**2 + (lng2-lng1)**2)**0.5
            router.add_route(loc1, loc2, distance)

@inventory_bp.route('/inventory', methods=['GET'])
def get_inventory():
    try:
        items = InventoryItem.get_all()
        return jsonify({
            'status': 'success',
            'data': items
        }), 200
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@inventory_bp.route('/inventory/<item_id>', methods=['GET'])
def get_item_by_id(item_id):
    try:
        item = InventoryItem.get_by_id(item_id)
        if item:
            return jsonify({
                'status': 'success',
                'data': item
            }), 200
        return jsonify({
            'status': 'error',
            'message': 'Item not found'
        }), 404
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@inventory_bp.route('/inventory', methods=['POST'])
def create_item():
    try:
        print("Received create_item request")
        data = request.get_json()
        print("Request data:", data)
        
        required_fields = ['name', 'quantity', 'category', 'price']
        
        if not all(field in data for field in required_fields):
            print("Missing required fields. Required:", required_fields)
            print("Received:", data.keys())
            return jsonify({
                'status': 'error',
                'message': 'Missing required fields'
            }), 400

        print("Creating item in database...")
        item_id = InventoryItem.create(data)
        print("Item created successfully with ID:", item_id)
        
        return jsonify({
            'status': 'success',
            'message': 'Item created successfully',
            'item_id': item_id
        }), 201
    except Exception as e:
        print("Error creating item:", str(e))
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@inventory_bp.route('/inventory/<item_id>', methods=['PUT'])
def update_item(item_id):
    try:
        data = request.get_json()
        if InventoryItem.update(item_id, data):
            return jsonify({
                'status': 'success',
                'message': 'Item updated successfully'
            }), 200
        return jsonify({
            'status': 'error',
            'message': 'Item not found'
        }), 404
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@inventory_bp.route('/inventory/<item_id>', methods=['DELETE'])
def delete_item(item_id):
    print(f"DEBUG: Type of item_id in delete_item route: {type(item_id)}")
    print(f"DEBUG: Value of item_id in delete_item route: {item_id}")
    try:
        if InventoryItem.delete(item_id):
            return jsonify({
                'status': 'success',
                'message': 'Item deleted successfully'
            }), 200
        return jsonify({
            'status': 'error',
            'message': 'Item not found'
        }), 404
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@inventory_bp.route('/inventory/summary', methods=['GET'])
def get_inventory_summary():
    try:
        total_items = InventoryItem.count_all()
        return jsonify({
            'status': 'success',
            'data': {
                'total_items': total_items
            }
        }), 200
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@inventory_bp.route('/orders/summary', methods=['GET'])
def get_orders_summary():
    try:
        # Assuming Order is a model similar to InventoryItem that can count all orders
        # If not, you'll need to implement a count_all method in your Order model
        total_orders = InventoryItem.count_all_orders() # Placeholder - needs actual Order model or direct DB query
        return jsonify({
            'status': 'success',
            'data': {
                'total_orders': total_orders
            }
        }), 200
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@inventory_bp.route('/routes/summary', methods=['GET'])
def get_routes_summary():
    try:
        # For active routes, this is a placeholder. You'd need logic to determine "active"
        active_routes_count = len(router.routes) # This counts all defined routes
        return jsonify({
            'status': 'success',
            'data': {
                'active_routes': active_routes_count
            }
        }), 200
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@inventory_bp.route('/orders', methods=['GET'])
def get_all_orders():
    try:
        orders = list(current_app.db.orders.find({}))
        return jsonify({
            'status': 'success',
            'data': json.loads(json_util.dumps(orders))
        }), 200
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@inventory_bp.route('/orders', methods=['POST'])
def create_order():
    try:
        data = request.get_json()
        if not data:
            return jsonify({
                'status': 'error',
                'message': 'No data provided in request'
            }), 400
        
        # Initialize order_data with common fields
        order_data = {
            'order_type': data.get('order_type'),
            'products': data.get('products'),
            'timestamp': datetime.utcnow()
        }

        # Validate required fields based on order type
        if 'order_type' not in data:
            return jsonify({
                'status': 'error',
                'message': 'Order type is required'
            }), 400

        # Validate products exist in inventory
        if 'products' not in data or not data['products']:
            return jsonify({
                'status': 'error',
                'message': 'Products are required'
            }), 400

        # For warehouse to user orders, validate stock availability
        if data['order_type'] == 'warehouse_to_user':
            for product in data['products']:
                if 'orderName' not in product or 'quantity' not in product:
                    return jsonify({
                        'status': 'error',
                        'message': f"Invalid product data: {product}"
                    }), 400
                item = next((item for item in InventoryItem.get_all() if item['name'] == product['orderName']), None)
                if not item:
                    return jsonify({
                        'status': 'error',
                        'message': f"Product {product['orderName']} not found in inventory"
                    }), 400
                if item['quantity'] < product['quantity']:
                    return jsonify({
                        'status': 'error',
                        'message': f"Insufficient stock for {product['orderName']}. Available: {item['quantity']}, Requested: {product['quantity']}"
                    }), 400

        elif data['order_type'] == 'factory_to_warehouse':
            if 'factory_id' not in data or 'warehouse_id' not in data:
                return jsonify({
                    'status': 'error',
                    'message': 'Factory ID and Warehouse ID are required for factory_to_warehouse orders'
                }), 400
            for product in data['products']:
                if 'orderName' not in product or 'quantity' not in product:
                    return jsonify({
                        'status': 'error',
                        'message': f"Invalid product data for factory_to_warehouse: {product}"
                    }), 400
                # For factory_to_warehouse, we increase the stock in general inventory
                # Assuming InventoryItem.update_stock handles the general stock regardless of location in the model
                InventoryItem.update_stock(product['orderName'], product['quantity'])
            order_data['source_factory_id'] = data['factory_id']
            order_data['destination_warehouse_id'] = data['warehouse_id']

        elif data['order_type'] == 'user_to_user':
            if 'source_user_id' not in data or 'destination_user_id' not in data:
                return jsonify({
                    'status': 'error',
                    'message': 'Source User ID and Destination User ID are required for user_to_user orders'
                }), 400
            for product in data['products']:
                if 'orderName' not in product or 'quantity' not in product:
                    return jsonify({
                        'status': 'error',
                        'message': f"Invalid product data for user_to_user: {product}"
                    }), 400
                # For user_to_user, reduce stock from source user and add to destination user (conceptual)
                # This would require a more complex user-specific inventory tracking
                # For now, we'll just log this and not modify central inventory for this type
                print(f"DEBUG: User to user transfer of {product['quantity']} of {product['orderName']}")

            order_data['source_user_id'] = data['source_user_id']
            order_data['destination_user_id'] = data['destination_user_id']
        
        else:
            return jsonify({
                'status': 'error',
                'message': 'Invalid order type'
            }), 400

        # Insert the order into the database
        order_id = current_app.db.orders.insert_one(order_data).inserted_id

        # Return success response
        return jsonify({
            'status': 'success',
            'message': 'Order created successfully',
            'order_id': str(order_id)
        }), 201
    except Exception as e:
        print("Error creating order:", str(e))
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@inventory_bp.route('/orders/process', methods=['POST'])
def process_orders():
    try:
        data = request.get_json()
        required_fields = ['type', 'orders']
        
        if not all(field in data for field in required_fields):
            return jsonify({
                'status': 'error',
                'message': 'Missing required fields'
            }), 400

        order_type = data['type']
        orders = data['orders']

        if order_type == 'factory_to_warehouse':
            if 'supplier' not in data:
                return jsonify({
                    'status': 'error',
                    'message': 'Supplier is required for factory to warehouse orders'
                }), 400
            # Process factory to warehouse orders
            for order in orders:
                try:
                    # Update inventory by adding stock
                    InventoryItem.update_stock(order['orderName'], order['quantity'])
                except Exception as e:
                    return jsonify({
                        'status': 'error',
                        'message': f"Error processing order for {order['orderName']}: {str(e)}"
                    }), 500

        elif order_type == 'warehouse_to_user':
            if 'user' not in data:
                return jsonify({
                    'status': 'error',
                    'message': 'User is required for warehouse to user orders'
                }), 400
            # Process warehouse to user orders
            for order in orders:
                try:
                    # Validate stock availability
                    item = next((item for item in InventoryItem.get_all() if item['name'] == order['orderName']), None)
                    if not item:
                        return jsonify({
                            'status': 'error',
                            'message': f"Product {order['orderName']} not found in inventory"
                        }), 400
                    if item['quantity'] < order['quantity']:
                        return jsonify({
                            'status': 'error',
                            'message': f"Insufficient stock for {order['orderName']}. Available: {item['quantity']}, Requested: {order['quantity']}"
                        }), 400
                    
                    # Update inventory by reducing stock
                    InventoryItem.update_stock(order['orderName'], -order['quantity'])
                except Exception as e:
                    return jsonify({
                        'status': 'error',
                        'message': f"Error processing order for {order['orderName']}: {str(e)}"
                    }), 500

        return jsonify({
            'status': 'success',
            'message': 'Orders processed successfully'
        }), 200
            
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@inventory_bp.route('/orders/<order_id>/nearby-users', methods=['GET'])
def get_nearby_users(order_id):
    try:
        max_distance = float(request.args.get('max_distance', float('inf')))
        user_id = request.args.get('user_id')
        
        if not user_id:
            return jsonify({
                'status': 'error',
                'message': 'User ID is required'
            }), 400
            
        nearby = router.get_nearby_users(user_id, max_distance)
        
        return jsonify({
            'status': 'success',
            'data': [{'user_id': uid, 'distance': dist} for uid, dist in nearby]
        }), 200
            
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@inventory_bp.route('/route/factory-to-warehouse', methods=['GET'])
def get_factory_warehouse_route():
    try:
        factory_id = request.args.get('factory_id')
        if not factory_id:
            return jsonify({
                'status': 'error',
                'message': 'Factory ID is required'
            }), 400
            
        route_ids = router.find_optimal_factory_warehouse_route(factory_id)
        # Convert location IDs to coordinates
        route = [EXAMPLE_LOCATIONS[loc_id][1] for loc_id in route_ids]
        
        return jsonify({
            'status': 'success',
            'route': route
        }), 200
            
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@inventory_bp.route('/route/warehouse-to-user', methods=['GET'])
def get_warehouse_user_route():
    try:
        warehouse_id = request.args.get('warehouse_id')
        user_id = request.args.get('user_id')
        
        if not warehouse_id or not user_id:
            return jsonify({
                'status': 'error',
                'message': 'Warehouse ID and User ID are required'
            }), 400
            
        route_ids = router.find_optimal_warehouse_user_route(warehouse_id, user_id)
        # Convert location IDs to coordinates
        route = [EXAMPLE_LOCATIONS[loc_id][1] for loc_id in route_ids]
        
        return jsonify({
            'status': 'success',
            'route': route
        }), 200
            
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@inventory_bp.route('/route/user-to-user', methods=['GET'])
def get_user_to_user_route():
    try:
        from_user = request.args.get('from_user')
        to_user = request.args.get('to_user')
        
        if not from_user or not to_user:
            return jsonify({
                'status': 'error',
                'message': 'From User ID and To User ID are required'
            }), 400
            
        route_ids = router.find_optimal_user_to_user_route(from_user, to_user)
        # Convert location IDs to coordinates
        route = [EXAMPLE_LOCATIONS[loc_id][1] for loc_id in route_ids]
        
        return jsonify({
            'status': 'success',
            'route': route
        }), 200
            
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500 