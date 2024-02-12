import matplotlib.pyplot as plt

class Node:
    def __init__(self, value=None):
        self.value = value
        self.children = []

def visualize_tree(root_node):
    def display_tree_matplotlib(root_node, x, y, level=0):
        """
        Displays the entire tree structure graphically using Matplotlib.

        Args:
            root_node: The root node of the tree (Node object).
            x: Initial x-coordinate for node placement.
            y: Initial y-coordinate for node placement.
            level: Current level of the node in the tree hierarchy.
        """
        if not root_node:
            return

        dx, dy = 0.2, 0.1  # Adjust spacing as needed

        # Mark all nodes even if there are no children (leaf nodes)
        plt.scatter(x, y, marker='o', c='red', s=5)  # Adjust marker size

        for i, child in enumerate(root_node.children):
            # Plot lines in black with low alpha for connections
            plt.plot([x, x + dx * (i + 1)], [y, y - dy], "k-", alpha=0.7)
            display_tree_matplotlib(child, x + dx * (i + 1), y - dy, level + 1)

    # Assuming you have a root_node object of type Node
    display_tree_matplotlib(root_node, 0.5, 1)  # Initial x and y coordinates
    plt.axis('off')
    plt.show()