import tkinter as tk
from tkinter import Toplevel, Label, Entry, Button
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import networkx as nx
import matplotlib.pyplot as plt

from astar import a_star_with_logging
from generator import generate_graph

start_node = 0
goal_node = 1

default_nodes = 10
default_edge_probability = 0.3
default_weight_range = (1, 10)

class GraphApp:
    def __init__(self, root):
        self.root = root
        self.root.title("B351-G20")
        self.graph = generate_graph(default_nodes, default_edge_probability, default_weight_range)
        self.path = []
        self.pos = nx.spring_layout(self.graph)
        self.figure, self.ax = plt.subplots(figsize=(6, 4))
        self.canvas = FigureCanvasTkAgg(self.figure, master=root)
        self.canvas_widget = self.canvas.get_tk_widget()
        self.canvas_widget.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        controls_frame = tk.Frame(root)
        controls_frame.pack(side=tk.BOTTOM, fill=tk.X)

        self.start_button = tk.Button(controls_frame, text="Run A*", command=self.run_astar)
        self.start_button.pack(side=tk.LEFT, padx=5, pady=5)

        self.add_node_button = tk.Button(controls_frame, text="Add Node", command=self.open_add_node_window)
        self.add_node_button.pack(side=tk.LEFT, padx=5, pady=5)

        self.add_edge_button = tk.Button(controls_frame, text="Add Edge", command=self.open_add_edge_window)
        self.add_edge_button.pack(side=tk.LEFT, padx=5, pady=5)

        self.remove_node_button = tk.Button(controls_frame, text="Remove Node", command=self.open_remove_node_window)
        self.remove_node_button.pack(side=tk.LEFT, padx=5, pady=5)

        self.remove_edge_button = tk.Button(controls_frame, text="Remove Edge", command=self.open_remove_edge_window)
        self.remove_edge_button.pack(side=tk.LEFT, padx=5, pady=5)

        self.set_start_button = tk.Button(controls_frame, text="Set Start", command=self.open_set_start_window)
        self.set_start_button.pack(side=tk.LEFT, padx=5, pady=5)

        self.set_goal_button = tk.Button(controls_frame, text="Set Goal", command=self.open_set_goal_window)
        self.set_goal_button.pack(side=tk.LEFT, padx=5, pady=5)

        self.randomize_button = tk.Button(controls_frame, text="Randomize Graph", command=self.randomize_graph)
        self.randomize_button.pack(side=tk.LEFT, padx=5, pady=5)

        self.settings_button = tk.Button(controls_frame, text="Graph Settings", command=self.open_settings_window)
        self.settings_button.pack(side=tk.LEFT, padx=5, pady=5)

        self.info_text = tk.Text(root, height=10)
        self.info_text.pack(side=tk.BOTTOM, fill=tk.X)

        self.update_graph()

    def update_graph(self):
        """Updates the graph visualization."""
        global start_node, goal_node
        self.ax.clear()
        nx.draw(self.graph, self.pos, with_labels=True, ax=self.ax, node_color="lightblue", node_size=500)
        edge_labels = nx.get_edge_attributes(self.graph, 'weight')
        nx.draw_networkx_edge_labels(self.graph, self.pos, edge_labels=edge_labels, ax=self.ax)

        nx.draw_networkx_nodes(self.graph, self.pos, nodelist=[start_node], node_color="red", node_size=700, ax=self.ax)
        nx.draw_networkx_nodes(self.graph, self.pos, nodelist=[goal_node], node_color="green", node_size=700, ax=self.ax)

        if self.path:
            path_edges = list(zip(self.path, self.path[1:]))
            nx.draw_networkx_edges(self.graph, self.pos, edgelist=path_edges, edge_color='red', width=2, ax=self.ax)

        self.ax.set_title(f"Start: {start_node}, Goal: {goal_node}")
        self.canvas.draw()

    def run_astar(self):
        """Runs the A* algorithm and updates the visualization and info box."""
        global start_node, goal_node
        self.info_text.delete(1.0, tk.END)

        def log_callback(message):
            """Callback to log messages from A* algorithm."""
            self.info_text.insert(tk.END, message + "\n")
            self.info_text.see(tk.END)

        self.path, cost = a_star_with_logging(self.graph, start_node, goal_node, heuristic=lambda n, g: 0, log_callback=log_callback)

        if self.path:
            self.info_text.insert(tk.END, f"\nPath: {self.path}\nTotal cost: {cost}\n")
        else:
            self.info_text.insert(tk.END, "\nNo path found.\n")

        self.update_graph()

    def open_add_node_window(self):
        """Opens a window to add a node."""
        def add_node():
            try:
                node = int(node_entry.get())
                self.graph.add_node(node)
                self.pos = nx.spring_layout(self.graph, pos=self.pos, fixed=self.pos.keys())
                add_node_window.destroy()
                self.update_graph()
            except ValueError:
                self.info_text.insert(tk.END, "Invalid node ID.\n")

        add_node_window = Toplevel(self.root)
        add_node_window.title("Add Node")

        Label(add_node_window, text="Node ID:").grid(row=0, column=0, padx=5, pady=5)
        node_entry = Entry(add_node_window)
        node_entry.grid(row=0, column=1, padx=5, pady=5)

        Button(add_node_window, text="Add", command=add_node).grid(row=1, column=0, columnspan=2, pady=10)

    def open_add_edge_window(self):
        """Opens a window to add an edge."""
        def add_edge():
            try:
                u = int(start_node_entry.get())
                v = int(end_node_entry.get())
                weight = int(weight_entry.get())
                self.graph.add_edge(u, v, weight=weight)
                add_edge_window.destroy()
                self.update_graph()
            except ValueError:
                self.info_text.insert(tk.END, "Invalid edge input.\n")

        add_edge_window = Toplevel(self.root)
        add_edge_window.title("Add Edge")

        Label(add_edge_window, text="Start Node:").grid(row=0, column=0, padx=5, pady=5)
        start_node_entry = Entry(add_edge_window)
        start_node_entry.grid(row=0, column=1, padx=5, pady=5)

        Label(add_edge_window, text="End Node:").grid(row=1, column=0, padx=5, pady=5)
        end_node_entry = Entry(add_edge_window)
        end_node_entry.grid(row=1, column=1, padx=5, pady=5)

        Label(add_edge_window, text="Weight:").grid(row=2, column=0, padx=5, pady=5)
        weight_entry = Entry(add_edge_window)
        weight_entry.grid(row=2, column=1, padx=5, pady=5)

        Button(add_edge_window, text="Add", command=add_edge).grid(row=3, column=0, columnspan=2, pady=10)

    def open_remove_node_window(self):
        """Opens a window to remove a node."""
        def remove_node():
            try:
                node = int(node_entry.get())
                self.graph.remove_node(node)
                self.pos = nx.spring_layout(self.graph, pos=self.pos, fixed=self.pos.keys())
                remove_node_window.destroy()
                self.update_graph()
            except ValueError:
                self.info_text.insert(tk.END, "Invalid node ID.\n")

        remove_node_window = Toplevel(self.root)
        remove_node_window.title("Remove Node")

        Label(remove_node_window, text="Node ID:").grid(row=0, column=0, padx=5, pady=5)
        node_entry = Entry(remove_node_window)
        node_entry.grid(row=0, column=1, padx=5, pady=5)

        Button(remove_node_window, text="Remove", command=remove_node).grid(row=1, column=0, columnspan=2, pady=10)

    def open_remove_edge_window(self):
        """Opens a window to remove an edge."""
        def remove_edge():
            try:
                u = int(start_node_entry.get())
                v = int(end_node_entry.get())
                self.graph.remove_edge(u, v)
                remove_edge_window.destroy()
                self.update_graph()
            except ValueError:
                self.info_text.insert(tk.END, "Invalid edge input.\n")

        remove_edge_window = Toplevel(self.root)
        remove_edge_window.title("Remove Edge")

        Label(remove_edge_window, text="Start Node:").grid(row=0, column=0, padx=5, pady=5)
        start_node_entry = Entry(remove_edge_window)
        start_node_entry.grid(row=0, column=1, padx=5, pady=5)

        Label(remove_edge_window, text="End Node:").grid(row=1, column=0, padx=5, pady=5)
        end_node_entry = Entry(remove_edge_window)
        end_node_entry.grid(row=1, column=1, padx=5, pady=5)

        Button(remove_edge_window, text="Remove", command=remove_edge).grid(row=2, column=0, columnspan=2, pady=10)

    def open_set_start_window(self):
        """Opens a window to set the start node."""
        def set_start():
            try:
                global start_node
                node = int(node_entry.get())
                if node in self.graph:
                    start_node = node
                    set_start_window.destroy()
                    self.update_graph()
                else:
                    self.info_text.insert(tk.END, "Node not in graph.\n")
            except ValueError:
                self.info_text.insert(tk.END, "Invalid node ID.\n")

        set_start_window = Toplevel(self.root)
        set_start_window.title("Set Start Node")

        Label(set_start_window, text="Start Node ID:").grid(row=0, column=0, padx=5, pady=5)
        node_entry = Entry(set_start_window)
        node_entry.grid(row=0, column=1, padx=5, pady=5)

        Button(set_start_window, text="Set", command=set_start).grid(row=1, column=0, columnspan=2, pady=10)

    def open_set_goal_window(self):
        """Opens a window to set the goal node."""
        def set_goal():
            try:
                global goal_node
                node = int(node_entry.get())
                if node in self.graph:
                    goal_node = node
                    set_goal_window.destroy()
                    self.update_graph()
                else:
                    self.info_text.insert(tk.END, "Node not in graph.\n")
            except ValueError:
                self.info_text.insert(tk.END, "Invalid node ID.\n")

        set_goal_window = Toplevel(self.root)
        set_goal_window.title("Set Goal Node")

        Label(set_goal_window, text="Goal Node ID:").grid(row=0, column=0, padx=5, pady=5)
        node_entry = Entry(set_goal_window)
        node_entry.grid(row=0, column=1, padx=5, pady=5)

        Button(set_goal_window, text="Set", command=set_goal).grid(row=1, column=0, columnspan=2, pady=10)

    def randomize_graph(self):
        """Generates a new random graph."""
        global start_node, goal_node
        self.graph = generate_graph(default_nodes, default_edge_probability, default_weight_range)
        self.path = []
        self.pos = nx.spring_layout(self.graph)
        self.update_graph()

    def open_settings_window(self):
        """Opens a window to adjust graph settings."""
        def save_settings():
            try:
                global default_nodes, default_edge_probability, default_weight_range
                default_nodes = int(nodes_entry.get())
                default_edge_probability = float(edge_probability_entry.get())
                weight_min = int(weight_min_entry.get())
                weight_max = int(weight_max_entry.get())
                default_weight_range = (weight_min, weight_max)
                settings_window.destroy()
                self.randomize_graph()
            except ValueError:
                self.info_text.insert(tk.END, "Invalid settings values.\n")

        settings_window = Toplevel(self.root)
        settings_window.title("Graph Settings")
        settings_window.protocol("WM_DELETE_WINDOW", settings_window.destroy)

        Label(settings_window, text="Number of Nodes:").grid(row=0, column=0, padx=5, pady=5)
        nodes_entry = Entry(settings_window)
        nodes_entry.insert(0, str(default_nodes))
        nodes_entry.grid(row=0, column=1, padx=5, pady=5)

        Label(settings_window, text="Edge Probability:").grid(row=1, column=0, padx=5, pady=5)
        edge_probability_entry = Entry(settings_window)
        edge_probability_entry.insert(0, str(default_edge_probability))
        edge_probability_entry.grid(row=1, column=1, padx=5, pady=5)

        Label(settings_window, text="Min Edge Weight:").grid(row=2, column=0, padx=5, pady=5)
        weight_min_entry = Entry(settings_window)
        weight_min_entry.insert(0, str(default_weight_range[0]))
        weight_min_entry.grid(row=2, column=1, padx=5, pady=5)

        Label(settings_window, text="Max Edge Weight:").grid(row=3, column=0, padx=5, pady=5)
        weight_max_entry = Entry(settings_window)
        weight_max_entry.insert(0, str(default_weight_range[1]))
        weight_max_entry.grid(row=3, column=1, padx=5, pady=5)

        Button(settings_window, text="Save", command=save_settings).grid(row=4, column=0, columnspan=2, pady=10)

if __name__ == "__main__":
    root = tk.Tk()
    app = GraphApp(root)
    root.mainloop()
