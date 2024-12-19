#  Shortest Path on Random Node Maps

This program uses the A* algorithm to find the shortest path in a graph and provides an interactive graphical interface for visualizing and customizing graphs. Users can dynamically modify graph structures, set start and goal nodes, and observe the algorithm in action.

---

## Functionality

The following **required** functionality is completed:

* [x] Implement a basic random node graph generator.
* [x] Implement and test the standard A* algorithm.
* [x] Integrate the A* algorithm with the random graph generator for initial path testing.


The following **extensions** are implemented:

* [x] Implement dynamic visualization of the search process by using NetworkX.
* [x] Optimize algorithm performance and complete implementation of dynamic weight changes.

## Dependencies

Before running the program, ensure that you have installed the needed Python packages:

```bash
pip install -r .\requirements.txt
```

---

## File Structure
### 1. `astar.py`
- **Functionality**: Implements the A* algorithm and its variants for shortest pathfinding in graphs.
- **Key Functions**:
  - `a_star`: Standard A* algorithm implementation.
  - `random_heuristic`: A heuristic function returning random values.
  - `heuristic_weighted_graph`: Heuristic considering graph edge weights.
  - `a_star_with_logging`: Logs the A* algorithm's decisions for debugging and analysis.
  - `visualizeAStar`: Visualizes A* results using Matplotlib.

### 2. `generator.py`
- **Functionality**: Provides random graph generation capabilities.
- **Key Functions**:
  - `generate_graph`: Generates an undirected graph with customizable edge probability and weights.
  - `visualize_graph`: Visualizes the generated undirected graph.
  - `generate_directed_graph`: Generates a directed graph.
  - `visualize_directed_graph`: Visualizes the directed graph.

### 3. `main.py`
- **Functionality**: Provides a Tkinter-based graphical interface for user interaction, integrating graph generation and pathfinding capabilities.
- **Key Features**:
  - Run A* algorithm and display results dynamically.
  - Add or remove nodes and edges interactively.
  - Set start and goal nodes.
  - Generate random graphs or customize graph settings.
  - Real-time graph visualization updates.

---

## Quick Start
### 1. Running the GUI
Launch the application by running:
```bash
python main.py
```

After launching, the interactive window allows you to:
- Click `Run A*` to execute the algorithm and view results.
- Use the bottom buttons to add nodes/edges or adjust the start and goal nodes.
- Click `Randomize Graph` to generate a random graph.
- Customize graph settings with `Graph Settings`.

### 2. Running A* Algorithm Directly
To run the algorithm in the console, modify the test code in `astar.py`:
```python
random_graph = generator.generate_graph(num_nodes=10, edge_probability=0.3, weight_range=(1, 10))
start_node = 0
goal_node = 9
path, cost = a_star_with_logging(random_graph, start_node, goal_node, heuristic=random_heuristic)
print(f"Path: {path}, Cost: {cost}")
```
Then execute:
```bash
python astar.py
```

---


## License
    Copyright 2024 Chuanhao Lin

    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at

        http://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.