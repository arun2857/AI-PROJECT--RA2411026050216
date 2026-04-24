import time
from collections import deque

# Default city graph (bidirectional)
DEFAULT_GRAPH = {
    'A': ['B', 'C'],
    'B': ['A', 'D', 'E'],
    'C': ['A', 'F', 'G'],
    'D': ['B', 'H'],
    'E': ['B', 'H', 'I'],
    'F': ['C', 'J'],
    'G': ['C', 'J', 'K'],
    'H': ['D', 'E', 'L'],
    'I': ['E', 'L'],
    'J': ['F', 'G', 'M'],
    'K': ['G', 'M'],
    'L': ['H', 'I', 'N'],
    'M': ['J', 'K', 'N'],
    'N': ['L', 'M']
}

def parse_graph(text):
    """Parse user-defined graph from text. Format: A-B,C; B-D,E"""
    graph = {}
    if not text.strip():
        return DEFAULT_GRAPH
    try:
        for part in text.split(';'):
            part = part.strip()
            if not part or '-' not in part:
                continue
            node, neighbors_str = part.split('-', 1)
            node = node.strip().upper()
            neighbors = [n.strip().upper() for n in neighbors_str.split(',') if n.strip()]
            graph[node] = neighbors
            for nb in neighbors:
                if nb not in graph:
                    graph[nb] = []
                if node not in graph[nb]:
                    graph[nb].append(node)
    except Exception:
        return DEFAULT_GRAPH
    return graph if graph else DEFAULT_GRAPH

def bfs(graph, start, goal):
    start, goal = start.upper(), goal.upper()
    if start not in graph or goal not in graph:
        return None, 0, 0.0

    start_time = time.perf_counter()
    visited = set()
    queue = deque([(start, [start])])
    nodes_explored = 0

    while queue:
        node, path = queue.popleft()
        nodes_explored += 1
        if node == goal:
            elapsed = (time.perf_counter() - start_time) * 1000
            return path, nodes_explored, elapsed
        if node in visited:
            continue
        visited.add(node)
        for neighbor in graph.get(node, []):
            if neighbor not in visited:
                queue.append((neighbor, path + [neighbor]))

    elapsed = (time.perf_counter() - start_time) * 1000
    return None, nodes_explored, elapsed

def dfs(graph, start, goal):
    start, goal = start.upper(), goal.upper()
    if start not in graph or goal not in graph:
        return None, 0, 0.0

    start_time = time.perf_counter()
    visited = set()
    nodes_explored = 0

    def _dfs(node, path):
        nonlocal nodes_explored
        nodes_explored += 1
        if node == goal:
            return path
        visited.add(node)
        for neighbor in graph.get(node, []):
            if neighbor not in visited:
                result = _dfs(neighbor, path + [neighbor])
                if result:
                    return result
        return None

    result = _dfs(start, [start])
    elapsed = (time.perf_counter() - start_time) * 1000
    return result, nodes_explored, elapsed

def get_all_nodes(graph):
    return sorted(graph.keys())
