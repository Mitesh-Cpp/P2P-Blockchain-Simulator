import matplotlib.pyplot as plt
from peer import peer

class Node:
    def __init__(self, value=None):
        self.value = value
        self.children = []

def visualize_tree(root_node, peer_index, total_peers):
    def display_tree_matplotlib(root_node, x, y, level=0):
        if not root_node:
            return

        dx, dy = 0.2, 0.1  # Adjust spacing as needed

        print("This block was mined by miner: ", root_node.miner_id)
        # Mark all nodes even if there are no children (leaf nodes)
        if(root_node.miner_id == None):
            plt.scatter(x, y, marker='o', c='green', s=20)  # Adjust marker size
        elif(root_node.miner_id < total_peers-2):
            plt.scatter(x, y, marker='o', c='green', s=20)  # Adjust marker size
        elif(root_node.miner_id == total_peers-2):
            plt.scatter(x, y, marker='o', c='red', s=20)
        else:
            plt.scatter(x, y, marker='o', c='blue', s=20)

        for i, child in enumerate(root_node.children):
            # Plot lines in black with low alpha for connections
            plt.plot([x, x + dx * (i + 1)], [y, y - dy], "k-", alpha=0.7)
            display_tree_matplotlib(child, x + dx * (i + 1), y - dy, level + 1)

    plt.clf()
    # Assuming you have a root_node object of type Node
    display_tree_matplotlib(root_node, 0.5, 1)  # Initial x and y coordinates
    plt.axis('off')
    plt.savefig(f'Blockchain_of_each_peer/Peer_{peer_index}.png')
    # plt.show()