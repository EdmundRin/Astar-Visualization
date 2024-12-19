import networkx as nx
import matplotlib.pyplot as plt
import random
import time

from queue import PriorityQueue

import generator

def a_star(graph, start, goal, heuristic):
    """
    Implements the A* algorithm to find the shortest path in a weighted graph.

    Parameters:
    - graph: A NetworkX graph object.
    - start: The starting node.
    - goal: The goal node.
    - heuristic: A function that estimates the cost from a node to the goal.

    Returns:
    - path: A list of nodes representing the shortest path from start to goal.
    - cost: The total cost of the path.
    """
    open_set = PriorityQueue()
    open_set.put((0, start))

    came_from = {}
    g_score = {node: float('inf') for node in graph.nodes}
    g_score[start] = 0

    f_score = {node: float('inf') for node in graph.nodes}
    f_score[start] = heuristic(start, goal)

    while not open_set.empty():
        current = open_set.get()[1]

        if current == goal:
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            path.append(start)
            path.reverse()
            return path, g_score[goal]

        for neighbor in graph.neighbors(current):
            tentative_g_score = g_score[current] + graph[current][neighbor]['weight']

            if tentative_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g_score
                f_score[neighbor] = g_score[neighbor] + heuristic(neighbor, goal)

                open_set.put((f_score[neighbor], neighbor))

    return None, float('inf')

def heuristic(node, goal):
    """
    Example heuristic function for A* algorithm.

    This is a simple placeholder that assumes the cost is 0.
    Modify this based on graph's characteristics.

    Parameters:
    - node: Current node.
    - goal: Goal node.

    Returns:
    - Estimated cost from the node to the goal.
    """
    return 0

def random_heuristic(node, goal):
    """
    Returns a random number as the heuristic value of the current node
    
    Parameters:
    - node: Current node.
    - goal: Goal node.

    Returns:
    - a random integer between 0 and 20.
    """
    return random.randint(0,20) 

def heuristic_weighted_graph(node, goal, graph):
    """
    Heuristic for weighted graphs, estimating the cost from the node to the goal.

    Parameters:
    - node: The current node.
    - goal: The goal node.
    - graph: The graph object with weighted edges.

    Returns:
    - Estimated cost from the node to the goal.
    """
    edge_weights = nx.get_edge_attributes(graph, 'weight').values()
    if len(edge_weights) > 0:
        average_edge_weight = sum(edge_weights) / len(edge_weights)
    else:
        average_edge_weight = 1

    try:
        estimated_path_length = nx.shortest_path_length(graph, node, goal, weight=None)
    except nx.NetworkXNoPath:
        return float('inf')

    return estimated_path_length * average_edge_weight

def a_star_weighted(graph, start, goal):
    """
    Implements the A* algorithm with a heuristic tailored for weighted graphs.

    Parameters:
    - graph: A NetworkX graph object.
    - start: The starting node.
    - goal: The goal node.

    Returns:
    - path: A list of nodes representing the shortest path from start to goal.
    - cost: The total cost of the path.
    """
    return a_star(graph, start, goal, lambda n, g: heuristic_weighted_graph(n, g, graph))

def a_star_with_logging(graph, start, goal, heuristic, log_callback=None):
    """
    Implements the A* algorithm with detailed logging to track the decision-making process.

    Parameters:
    - graph: A NetworkX graph object representing the weighted graph.
    - start: The starting node in the graph.
    - goal: The target node to find a path to.
    - heuristic: A function that estimates the cost to reach the goal from a given node.
    - log_callback: Optional callback function to log progress messages.

    Returns:
    - path: A list of nodes representing the shortest path from the start node to the goal node. If no path is found, returns None.
    - cost: The total cost of the path from start to goal. If no path is found, returns infinity.

    Features:
    - Uses a priority queue to manage the open set of nodes to be explored.
    - Logs the contents of the open set before and after processing each node.
    - Tracks and logs the decision-making process, including when a node is processed and when the goal is reached or no path is found.
    """
    open_set = PriorityQueue()
    open_set.put((0, start))

    came_from = {}
    g_score = {node: float('inf') for node in graph.nodes}
    g_score[start] = 0

    f_score = {node: float('inf') for node in graph.nodes}
    f_score[start] = heuristic(start, goal)

    open_set_elements = {start}

    if log_callback:
        log_callback("Starting A* Algorithm")
        log_callback(f"Initial Open Set: {open_set_elements}\n")

    while not open_set.empty():
        current = open_set.get()[1]
        open_set_elements.remove(current)

        if log_callback:
            log_callback(f"Processing Node: {current}")
            log_callback(f"Open Set Before Processing: {open_set_elements}")

        if current == goal:
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            path.append(start)
            path.reverse()

            if log_callback:
                log_callback("Goal Reached!")
                log_callback(f"Final Path: {path}")

            return path, g_score[goal]

        for neighbor in graph.neighbors(current):
            tentative_g_score = g_score[current] + graph[current][neighbor]['weight']

            if tentative_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g_score
                f_score[neighbor] = g_score[neighbor] + heuristic(neighbor, goal)

                if neighbor not in open_set_elements:
                    open_set.put((f_score[neighbor], neighbor))
                    open_set_elements.add(neighbor)

        if log_callback:
            log_callback(f"Open Set After Processing: {open_set_elements}\n")

    if log_callback:
        log_callback("No Path Found!")

    return None, float('inf')


def visualizeAStar(graph, start, goal, path):
    """
    Visualizes a graph and highlights the path found by the A* algorithm.

    Parameters:
    - graph: A NetworkX graph object representing the graph to be visualized. 
            Each edge should have a 'weight' attribute.
    - start: The starting node of the A* algorithm (highlighted in red).
    - goal: The goal node of the A* algorithm (highlighted in green).
    - path: A list of nodes representing the path found by the A* algorithm 
            (highlighted in red). If no path is found, pass an empty list.

    Visualization:
    - Nodes are drawn in gray by default.
    - The start node is highlighted in red.
    - The goal node is highlighted in green.
    - Edges are drawn in gray, with their weights labeled.
    - The path is drawn as a red line connecting the nodes in the path.

    Returns:
    - None: The function displays the graph using matplotlib but does not return any value.
    """
    plt.figure(figsize=(10,8))
    pos = nx.spring_layout(graph)

    # all nodes
    nx.draw_networkx_nodes(graph, pos, node_color='grey', node_size=500)

    # start and goal node
    nx.draw_networkx_nodes(graph, pos, nodelist=[start], node_color='red', node_size=700)
    nx.draw_networkx_nodes(graph, pos, nodelist=[goal], node_color='green', node_size=700)


    # edges
    nx.draw_networkx_edges(graph, pos, edge_color='gray')

    # weights
    edge_labels = nx.get_edge_attributes(graph, 'weight')
    nx.draw_networkx_edge_labels(graph, pos, edge_labels=edge_labels)

    # path
    if path:
        edges = list(zip(path, path[1:]))
        nx.draw_networkx_edges(graph, pos, edgelist=edges, edge_color='red', width=2)

    # labels
    nx.draw_networkx_labels(graph, pos, font_size=12, font_color='black')
    plt.show()

# Test 
if __name__ == "__main__":
    random_graph = generator.generate_graph(num_nodes=10, edge_probability=0.3, weight_range=(1, 10))
    
    start_node = 0
    goal_node = 9

    start_time = time.time()
    path, cost = a_star_with_logging(random_graph, start_node, goal_node, random_heuristic)
    end_time = time.time()
    print(f"time (for random heuristic): {end_time - start_time:.6f} seconds")

    if path:
        print(f"shortest path from {start_node} to {goal_node}: {path}")
        print(f"total cost: {cost}")
    else:
        print(f"no path")

    #visualizeAStar(random_graph, start_node, goal_node, path)

    start_time = time.time()
    path, cost = a_star_weighted(random_graph, start_node, goal_node)
    end_time = time.time()
    print(f"time (weighted heuristic): {end_time - start_time:.6f} seconds")

    if path:
        print(f"shortest path found from {start_node} to {goal_node}: {path}")
        print(f"total cost: {cost}")
    else:
        print(f"no path")