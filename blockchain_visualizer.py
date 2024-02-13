import matplotlib.pyplot as plt
import numpy as np
def visualize_graph(adjacency_list):

  # Set up plot
  plt.figure(figsize=(8, 6))  # Adjust figure size as needed

  # Calculate node positions (random for simplicity)
  num_nodes = len(adjacency_list)
  node_positions = [(i, 0) for i in range(num_nodes)]

  # Draw nodes
  plt.plot([p[0] for p in node_positions], [p[1] for p in node_positions], 'o', markersize=15)

  # Draw edges
  for i, neighbors in enumerate(adjacency_list):
    print(i, neighbors)
    for neighbor in neighbors:
      print([node_positions[i][0], node_positions[neighbor][0]], [node_positions[i][1], node_positions[neighbor][1]])
      plt.plot([node_positions[i][0], node_positions[neighbor][0]],
               [node_positions[i][1], node_positions[neighbor][1]], 'b-', alpha=0.7)

  # Label nodes (optional)
  for i, pos in enumerate(node_positions):
    plt.text(pos[0], pos[1], str(i), ha='center', va='center', fontsize=12)

  # Customize plot (optional)
  plt.title("Graph Visualization")
  plt.axis('off')  # Remove axes ticks and labels
  plt.show()