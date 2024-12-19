import networkx as nx
import matplotlib.pyplot as plt
import random

def generate_graph(num_nodes, edge_probability, weight_range):
    """
    Generates a random graph with specified nodes, edge probability, and weight range.

    Parameters:
    - num_nodes: Number of nodes in the graph.
    - edge_probability: Probability of edge creation between nodes.
    - weight_range: Tuple indicating the range of edge weights.

    Returns:
    - graph: A NetworkX graph object with random weights.
    """
    graph = nx.Graph()
    graph.add_nodes_from(range(num_nodes))

    for i in range(num_nodes):
        for j in range(i + 1, num_nodes):
            if random.random() < edge_probability:
                weight = random.randint(*weight_range)
                graph.add_edge(i, j, weight=weight)
    
    return graph

def visualize_graph(graph):
    """
    Visualizes a graph with weights displayed on the edges.

    Parameters:
    - graph: A NetworkX graph object.
    """
    pos = nx.spring_layout(graph)
    nx.draw(graph, pos, with_labels=True, node_color="lightblue", node_size=500, font_size=10)
    edge_labels = nx.get_edge_attributes(graph, 'weight')
    nx.draw_networkx_edge_labels(graph, pos, edge_labels=edge_labels)
    plt.show()

def generate_directed_graph(num_nodes, edge_probability, weight_range):
    """
    Generates a random directed graph with specified nodes, edge probability, and weight range.

    Parameters:
    - num_nodes: Number of nodes in the graph.
    - edge_probability: Probability of edge creation between nodes.
    - weight_range: Tuple indicating the range of edge weights.

    Returns:
    - graph: A NetworkX directed graph object with random weights.
    """
    graph = nx.DiGraph()
    graph.add_nodes_from(range(num_nodes))

    for i in range(num_nodes):
        for j in range(num_nodes):
            if i != j and random.random() < edge_probability:
                weight = random.randint(*weight_range)
                graph.add_edge(i, j, weight=weight)

    return graph

def visualize_directed_graph(graph):
    """
    Visualizes a directed graph with weights displayed on the edges.

    Parameters:
    - graph: A NetworkX directed graph object.
    """
    pos = nx.spring_layout(graph)
    nx.draw(graph, pos, with_labels=True, node_color="lightblue", node_size=500, font_size=10, arrows=True)
    edge_labels = nx.get_edge_attributes(graph, 'weight')
    nx.draw_networkx_edge_labels(graph, pos, edge_labels=edge_labels)
    plt.show()

# Test 
if __name__ == "__main__":
    num_nodes = 10  # Example: 10 nodes
    edge_probability = 0.3  # 30% chance for each edge
    weight_range = (1, 10)  # Edge weights between 1 and 10

    random_graph = generate_graph(num_nodes, edge_probability, weight_range)
    visualize_graph(random_graph)

    # random_directed_graph = generate_directed_graph(num_nodes, edge_probability, weight_range)
    # visualize_directed_graph(random_directed_graph)