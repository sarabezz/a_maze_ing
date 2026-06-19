# A-MAZE-ING

A Python program that generates a random maze and finds the shortest path between two points — if one exists.

## About

A_maze_ing reads a configuration file provided by the user that defines the maze dimensions, entry and exit points, and whether the maze should be perfect or not. It generates a random maze using a recursive backtracker algorithm, then finds the shortest path between the two points using BFS. If no path exists, the program exits with an error. The result is displayed graphically using MiniLibX, where the user can regenerate the maze, show or hide the solution path, and change the wall colors.


## Algorithm

Step 1 — Maze generation (Recursive Backtracker)
The algorithm starts at the entry cell, marks it as visited, and pushes it onto a stack. It then picks a random unvisited neighbor, breaks the wall between them, marks the neighbor as visited, and moves to it. If a cell has no unvisited neighbors, it backtracks by popping the stack until it finds a cell that does. This repeats until every cell has been visited, producing a perfect maze — exactly one path between any two cells.

Step 2 — Maze solving (BFS)
Starting from the entry point defined in the config file, BFS explores the maze layer by layer — first all cells at distance 1, then distance 2, and so on. Each visited cell records where it came from in a parent dictionary. When the exit is reached, the path is reconstructed by following parent backwards from exit to entry and reversing it. Because BFS always processes closer cells first, the first path found is guaranteed to be the shortest.

## Functions

### Configuration (`a_maze_ing.py`)

| Function | Description |
|----------|-------------|
| `read_config` | Reads the configuration file and returns a dictionary with the maze parameters |
| `validate_config` | Validates all parameters — dimensions, entry and exit coordinates, and required keys |
| `add_loops` | Removes extra walls at random to create loops, used when `PERFECT=False` |
| `main` | Entry point — reads config, builds the maze, generates, solves, saves and displays it |

### Maze core (`maze_core.py`)

| Function | Description |
|----------|-------------|
| `Cell` | Represents a single maze cell with four walls and three state flags: `visited`, `in_path`, and `blocked` |
| `Maze` | Stores the full grid of cells, dimensions, and entry and exit coordinates |
| `generate_maze` | Generates a random perfect maze using the recursive backtracker algorithm |
| `BFS` | Finds the shortest path between entry and exit using Breadth First Search, storing each cell's parent to reconstruct the path |
| `hex_cells` | Encodes a cell's four walls as a single hexadecimal character for the output file |
| `save_maze` | Saves the maze grid in hex format, the entry and exit coordinates, and the solution path to a text file |
| `four2` | Blocks the cells that form the "42" pattern in the center of the maze |
| `mark_path` | Marks each cell belonging to the solution path with `in_path = True` |
| `reset_maze` | Resets all non-blocked cells to unvisited, removes the path, and closes all walls so the maze can be regenerated |

### Visualization (`maze_visual.py`)

| Function | Description |
|----------|-------------|
| `draw_rect` | Paints a rectangle of pixels of a given color at a given position in the image |
| `draw_maze` | Iterates over every cell and paints it pixel by pixel — walls, path, entry, exit and blocked cells |
| `menu` | Initializes the MLX window and handles user input: regenerate, show/hide path, change wall color, and exit |


## Usage

```bash
git clone https://github.com/sarabezz/a_maze_ing.git
cd a_maze_ing
python3 -m venv venv
source venv/bin/activate.fish  # fish shell
pip install mlx-2.2-py3-ubuntu-any.whl
```

Run the program:

```bash
python3 a_maze_ing.py config.txt
```

Or with make:

```bash
make run
```

The config file must define the following parameters:

```
WIDTH=21
HEIGHT=21
ENTRY=2,2
EXIT=3,4
OUTPUT_FILE=maze.txt
PERFECT=True
SEED=42        # optional
```


## Key concepts

- The maze is represented as a 2D grid where each cell stores its four walls as booleans and three state flags: `visited`, `in_path`, and `blocked`
- The recursive backtracker uses a stack to generate a perfect maze — every cell is reachable and there is exactly one path between any two cells
- BFS guarantees the shortest path by exploring cells layer by layer, always processing closer cells before further ones
- Each cell's walls are encoded as a single hexadecimal character in the output file — each bit represents one wall direction (N, E, S, W)
- MiniLibX renders the maze by writing pixels directly to an image buffer using `mlx_get_data_addr`, then displaying it with `mlx_put_image_to_window`
- When `PERFECT=False`, extra walls are removed at random to create loops — multiple paths between cells


## Project info

| | |
|---|---|
| Language | Python |
| School | 42 Madrid |
| Status | ✅ Completed |
