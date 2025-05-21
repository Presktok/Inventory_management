from typing import List, Tuple, Set

class UnionFind:
    def __init__(self, vertices: Set[str]):
        self.parent = {vertex: vertex for vertex in vertices}
        self.rank = {vertex: 0 for vertex in vertices}

    def find(self, item: str) -> str:
        """Find the root of the set that contains item"""
        if self.parent[item] != item:
            self.parent[item] = self.find(self.parent[item])
        return self.parent[item]

    def union(self, set1: str, set2: str):
        """Union two sets"""
        root1 = self.find(set1)
        root2 = self.find(set2)

        if root1 != root2:
            if self.rank[root1] < self.rank[root2]:
                root1, root2 = root2, root1
            self.parent[root2] = root1
            if self.rank[root1] == self.rank[root2]:
                self.rank[root1] += 1

def kruskal_mst(vertices: Set[str], edges: List[Tuple[str, str, float]]) -> List[Tuple[str, str, float]]:
    """
    Implement Kruskal's algorithm for finding minimum spanning tree
    Args:
        vertices: Set of all vertices
        edges: List of tuples (from_node, to_node, weight)
    Returns:
        List of edges in the minimum spanning tree
    """
    # Sort edges by weight
    edges = sorted(edges, key=lambda x: x[2])
    
    # Initialize union-find data structure
    uf = UnionFind(vertices)
    
    # Initialize result
    mst = []
    
    # Process edges in ascending order of weight
    for edge in edges:
        u, v, weight = edge
        
        # If including this edge doesn't create a cycle
        if uf.find(u) != uf.find(v):
            mst.append(edge)
            uf.union(u, v)
            
    return mst 