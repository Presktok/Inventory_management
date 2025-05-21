# backend/config/graph.py

graph = {
    "FactoryA": {"W1": 6, "W2": 3},
    "W1": {"User1": 2},
    "W2": {"User1": 4}
}

edges = [
    ("FactoryA", "W1", 6),
    ("FactoryA", "W2", 3),
    ("W1", "User1", 2),
    ("W2", "User1", 4)
]

node_coordinates = {
    "FactoryA": {"lat": 28.6139, "lng": 77.2090},
    "W1": {"lat": 28.7041, "lng": 77.1025},
    "W2": {"lat": 28.5355, "lng": 77.3910},
    "User1": {"lat": 28.4089, "lng": 77.3178}
}

def get_path_from_dijkstra(previous, destination):
    path = []
    while destination:
        path.insert(0, destination)
        destination = previous.get(destination)
    return path
