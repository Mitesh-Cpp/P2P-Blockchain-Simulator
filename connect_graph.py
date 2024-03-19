import random
from peer import peer

def connect_graph(peers):
    n = len(peers)
    network_graph = [[False] * n for _ in range(n)]  # Initialize an empty network graph

    def show_graph(peers, network_graph):
        for i, row in enumerate(network_graph):
            print(f"Node {peers[i].id}: Connected to {', '.join(map(str, peers[i].connected_nodes))}")

    # Checks if all peers are connected or not
    def is_connected(graph, start, visited):
        stack = [start]
        visited[start] = True

        while stack:
            current_node = stack.pop()
            for neighbor, has_edge in enumerate(graph[current_node]):
                if has_edge and not visited[neighbor]:
                    stack.append(neighbor)
                    visited[neighbor] = True

        return all(visited)

    # Tries Connect peers such that each peer has degree in between 3 and 6
    def connect_peers(peers, network_graph):
        for i in range(n):
            peers[i].connected_nodes = []
        for i in range(n):
            if len(peers[i].connected_nodes) == 6:
                continue
            deg = 3 + random.randint(0, 3) - len(peers[i].connected_nodes)
            available_nodes = set(range(n))

            while deg > 0 and available_nodes:
                node_id = random.choice(list(available_nodes))
                if not network_graph[i][node_id] and len(peers[node_id].connected_nodes) < 6 and node_id != i:
                    network_graph[i][node_id] = network_graph[node_id][i] = True
                    peers[i].connected_nodes.append(peers[node_id].id)
                    peers[node_id].connected_nodes.append(peers[i].id)
                    deg -= 1
                available_nodes.remove(node_id)

    connect_peers(peers, network_graph)

    # Check if the degree of each node is at least 3
    min_degree = 7
    for i in range(n):
        min_degree = min(min_degree, len(peers[i].connected_nodes))
    
    # If graph generated is not satisfying our conditions, then rebuild it.
    while min_degree < 3 or not is_connected(network_graph, 0, [False] * n):
        network_graph = [[False] * n for _ in range(n)]
        connect_peers(peers, network_graph)
    
    show_graph(peers, network_graph)