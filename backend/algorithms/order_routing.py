from typing import Dict, List, Optional, Tuple
import heapq
from datetime import datetime
from .graph import Graph
from .mst import kruskal_mst

class Order:
    def __init__(self, order_id: str, user_id: str, warehouse_id: str, 
                 items: List[Dict], timestamp: datetime):
        self.order_id = order_id
        self.user_id = user_id
        self.warehouse_id = warehouse_id
        self.items = items
        self.timestamp = timestamp
        self.status = "pending"
        self.route = []

class OrderRouter:
    def __init__(self):
        self.graph = Graph()
        self.order_queue = []  # Priority queue for orders
        self.warehouses = set()
        self.factories = set()
        self.users = set()

    def add_location(self, location_id: str, location_type: str):
        """Add a new location (factory, warehouse, or user)"""
        if location_type == "factory":
            self.factories.add(location_id)
        elif location_type == "warehouse":
            self.warehouses.add(location_id)
        else:  # user
            self.users.add(location_id)

    def add_route(self, from_location: str, to_location: str, distance: float):
        """Add a route between two locations"""
        self.graph.add_edge(from_location, to_location, distance)

    def find_optimal_factory_warehouse_route(self, factory_id: str) -> List[str]:
        """Find optimal route from factory to warehouses using Kruskal's MST"""
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

    def find_optimal_warehouse_user_route(self, warehouse_id: str, user_id: str) -> List[str]:
        """Find shortest path from warehouse to user using Dijkstra's"""
        return self.graph.get_shortest_path(warehouse_id, user_id)

    def find_optimal_user_to_user_route(self, from_user: str, to_user: str) -> List[str]:
        """Find shortest path between users using Dijkstra's"""
        return self.graph.get_shortest_path(from_user, to_user)

    def add_order(self, order: Order):
        """Add order to priority queue"""
        heapq.heappush(self.order_queue, (order.timestamp, order))

    def process_next_order(self) -> Optional[Tuple[Order, List[str]]]:
        """Process the next order in the queue"""
        if not self.order_queue:
            return None

        _, order = heapq.heappop(self.order_queue)
        
        # Find closest factory to the warehouse
        factory_routes = {}
        for factory in self.factories:
            route = self.find_optimal_factory_warehouse_route(factory)
            if route:
                factory_routes[factory] = route

        if not factory_routes:
            return None

        # Choose the factory with shortest route
        best_factory = min(factory_routes.keys(), 
                          key=lambda f: len(factory_routes[f]))
        
        # Get route from warehouse to user
        warehouse_user_route = self.find_optimal_warehouse_user_route(
            order.warehouse_id, order.user_id)

        # Combine routes
        complete_route = (factory_routes[best_factory] + 
                         warehouse_user_route[1:])  # Remove duplicate warehouse
        
        order.route = complete_route
        order.status = "processing"
        
        return order, complete_route

    def get_nearby_users(self, user_id: str, max_distance: float = float('inf')) -> List[Tuple[str, float]]:
        """Find nearby users within max_distance"""
        distances, _ = self.graph.dijkstra(user_id)
        nearby = [(u, d) for u, d in distances.items() 
                 if u in self.users and u != user_id and d <= max_distance]
        return sorted(nearby, key=lambda x: x[1])  # Sort by distance 