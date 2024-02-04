import random
from peer import peer

def connect_graph(peers):
    n = len(peers)
    network_graph = [[False] * n for _ in range(n)]  # Initialize an empty network graph

    def show_graph(peers, network_graph):
        for i, row in enumerate(network_graph):
            connected_nodes = [peers[j].id for j, has_edge in enumerate(row) if has_edge]
            print(f"Node {peers[i].id}: Connected to {', '.join(map(str, connected_nodes))}")

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

    degree = [0] * n  # Define degree in the broader scope

    def connect_peers(peers, network_graph):
        for i in range(n):
            if degree[i] == 6:
                continue
            deg = 3 + random.randint(0, 3) - degree[i]
            available_nodes = set(range(n))
            
            # Clear connected_nodes list for all peers
            for peer in peers:
                peer.connected_nodes = []

            while deg > 0 and available_nodes:
                node_id = random.choice(list(available_nodes))
                if not network_graph[i][node_id] and degree[node_id] < 6 and node_id != i:
                    network_graph[i][node_id] = network_graph[node_id][i] = True
                    degree[i] += 1
                    degree[node_id] += 1
                    peers[i].connected_nodes.append(peers[node_id].id)
                    peers[node_id].connected_nodes.append(peers[i].id)
                    deg -= 1
                available_nodes.remove(node_id)
        show_graph(peers, network_graph)
        return network_graph

    connected_graph = connect_peers(peers, network_graph)

    # Check if the degree of each node is at least 3
    while min(degree) < 3 or not is_connected(connected_graph, 0, [False] * n):
        print("Rerunning connect_peers as some nodes have degree less than 3 or the graph is not connected.")
        network_graph = [[False] * n for _ in range(n)]
        connected_graph = connect_peers(peers, network_graph)

    print("Connectivity established successfully!")
    return connected_graph