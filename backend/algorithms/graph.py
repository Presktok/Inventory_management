from collections import defaultdict
import heapq
from typing import Dict, List, Set, Tuple

class Graph:
    def __init__(self):
        self.nodes = defaultdict(list)
        self.distances = {}

    def add_edge(self, from_node: str, to_node: str, distance: float):
        """Add an edge to the graph with its distance"""
        self.nodes[from_node].append(to_node)
        self.nodes[to_node].append(from_node)  # For undirected graph
        self.distances[(from_node, to_node)] = distance
        self.distances[(to_node, from_node)] = distance

    def dijkstra(self, initial: str) -> Tuple[Dict[str, float], Dict[str, str]]:
        """
        Implements Dijkstra's shortest path algorithm
        Returns distances and predecessors
        """
        distances = {node: float('infinity') for node in self.nodes}
        distances[initial] = 0
        pq = [(0, initial)]
        visited = set()
        predecessors = {node: None for node in self.nodes}

        while pq:
            current_distance, current_vertex = heapq.heappop(pq)

            if current_vertex in visited:
                continue

            visited.add(current_vertex)

            for neighbor in self.nodes[current_vertex]:
                if neighbor in visited:
                    continue

                distance = self.distances.get((current_vertex, neighbor), float('infinity'))
                new_distance = current_distance + distance

                if new_distance < distances[neighbor]:
                    distances[neighbor] = new_distance
                    predecessors[neighbor] = current_vertex
                    heapq.heappush(pq, (new_distance, neighbor))

        return distances, predecessors

    def get_shortest_path(self, start: str, end: str) -> List[str]:
        """Get the shortest path between start and end nodes"""
        distances, predecessors = self.dijkstra(start)
        
        if distances[end] == float('infinity'):
            return []

        path = []
        current = end
        while current is not None:
            path.append(current)
            current = predecessors[current]
        
        return list(reversed(path)) 