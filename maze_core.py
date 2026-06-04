# genera el laberinto no depende de nada externo
from collections import deque
import random


class Cell:
    def __init__(self):
        self.walls = { # True = pared cerrada
            'N': True,
            'S': True,
            'E': True,
            'W': True
        }
        self.visited = False
        self.in_path = False
        self.blocked = False


class Maze:
    def __init__(self, width, height, start, end):
        self.width = width
        self.height = height
        self.grid = [[Cell() for _ in range(width)] for _ in range(height)]
        self.start = start # guardamos como (fila, columna) = (y, x)
        self.end = end

DIRECTIONS = {
    'N': (-1, 0),  # fila - 1
    'S': (1, 0),   # fila + 1
    'E': (0, 1),   # columna + 1
    'W': (0, -1)   # columna - 1
}

OPPOSITE = {
    'N': 'S',
    'S': 'N',
    'E': 'W',
    'W': 'E'
}

def generate_maze(maze): # solo generar el laberinto aleatoriamente, vamos construyendo un camino
    stack = []

    # start está guardado como (fila, columna)
    row, col = maze.start
    maze.grid[row][col].visited = True
    stack.append((row, col))

    while stack:
        row, col = stack[-1] # miramos la celda actual sin sacarla (ult celda)
        current = maze.grid[row][col]

        # buscamos vecinos válidos
        neighbors = []
        for direction, (drow, dcol) in DIRECTIONS.items():
            nrow, ncol = row + drow, col + dcol
            if 0 <= nrow < maze.height and 0 <= ncol < maze.width:
                neighbor = maze.grid[nrow][ncol]
                if not neighbor.visited and not neighbor.blocked:
                    neighbors.append((direction, nrow, ncol)) # tupla [('N', 2, 3), ('E', 1, 4), ('S', 2, 3)]
    
        if neighbors:
            direction, nrow, ncol = random.choice(neighbors)
            neighbor = maze.grid[nrow][ncol]

            current.walls[direction] = False
            neighbor.walls[OPPOSITE[direction]] = False

            neighbor.visited = True
            stack.append((nrow, ncol))

        else:
            stack.pop()
        
def BFS(maze):
    start = maze.start
    end = maze.end

    queue = deque() # cola de celdas por explorar
    queue.append(start)

    visited = set() # conjunto de celdas ya exploradas
    visited.add(start)

    parent = {} # dic que recuerda de dónde venimos

    while queue:
        x, y = queue.popleft()
        current = maze.grid[x][y]

        for direction, (dx, dy) in DIRECTIONS.items():
            if current.walls[direction]:
                continue # comprobamos las direc y en las que tenga pared pasamos y comprobamos otra direc
            
            nx, ny = x + dx, y + dy
            if 0 <= nx < maze.height and 0 <= ny < maze.width:
                if (nx, ny) not in visited:
                    visited.add((nx, ny))
                    parent[(nx, ny)] = (x, y)
                    queue.append((nx, ny))
    
    if end not in parent and end != start:
        print("Path not found")
        return None

    # si lo hemos encontrado reconstruimos el camino
    path = []
    current = end

    while current != start:
        px, py = parent[current]

        dx = current[0] - px
        dy = current[1] - py

        if dx == -1: path.append('N')
        if dx == 1:  path.append('S')
        if dy == -1: path.append('W')
        if dy == 1:  path.append('E')

        current = (px, py)

    path.reverse()
    return path

def hex_cells(cell):
    bits = 0
    bits |= cell.walls['N'] << 0  # bit 0
    bits |= cell.walls['E'] << 1  # bit 1
    bits |= cell.walls['S'] << 2  # bit 2
    bits |= cell.walls['W'] << 3  # bit 3
    return hex(bits)[2:].upper()

def save_maze(maze, path_cells, filename='maze.txt'):
    with open(filename, 'w') as f:
        
        # guardamos el grid fila por fila
        for row in maze.grid:
            line = ''.join([hex_cells(cell) for cell in row])
            f.write(line + '\n')
        
        f.write('\n')
        
        # convertimos de (fila, col) interno a (x, y) del subject
        start_row, start_col = maze.start
        end_row, end_col = maze.end
        
        f.write(f"{start_col},{start_row}\n")  # x,y = col,fila
        f.write(f"{end_col},{end_row}\n")       # x,y = col,fila
        f.write(''.join(path_cells) + '\n')

def four2(maze):
    if maze.height < 7 or maze.width < 9:
        print("Error: maze not big enough")
        return

    # calculamos la esquina superior izquierda del patrón
    # lo centramos en el laberinto
    start_row = maze.height // 2 - 2
    start_col = maze.width // 2 - 4

    # patrón del 4 — coordenadas relativas (fila, columna)
    four = [
        (0, 0), (0, 2),          # fila 0: X . X
        (1, 0), (1, 2),          # fila 1: X . X
        (2, 0), (2, 1), (2, 2),  # fila 2: X X X
                (3, 2),          # fila 3: . . X
                (4, 2),          # fila 4: . . X
    ]

    # patrón del 2 — empieza 4 columnas a la derecha del 4
    two = [
        (0, 0), (0, 1), (0, 2),  # fila 0: X X X
                        (1, 2),  # fila 1: . . X
        (2, 0), (2, 1), (2, 2),  # fila 2: X X X
        (3, 0),                  # fila 3: X . .
        (4, 0), (4, 1), (4, 2),  # fila 4: X X X
    ]

    # bloqueamos las celdas del 4
    for drow, dcol in four:
        row = start_row + drow
        col = start_col + dcol
        cell = maze.grid[row][col]
        cell.blocked = True
        cell.visited = True
        cell.walls = {'N': True, 'S': True, 'E': True, 'W': True}

    # bloqueamos las celdas del 2 (desplazadas 4 columnas a la derecha)
    for drow, dcol in two:
        row = start_row + drow
        col = start_col + dcol + 4
        cell = maze.grid[row][col]
        cell.blocked = True
        cell.visited = True
        cell.walls = {'N': True, 'S': True, 'E': True, 'W': True}

def mark_path(maze, path):
    row, col = maze.start
    maze.grid[row][col].in_path = True
    for direction in path:
        drow, dcol = DIRECTIONS[direction]
        row += drow
        col += dcol
        maze.grid[row][col].in_path = True

def reset_maze(maze):
    for row in range(maze.height):
        for col in range(maze.width):
            cell = maze.grid[row][col]
            if not cell.blocked:    # no tocamos las celdas del "42"
                cell.visited = False
                cell.in_path = False
                cell.walls = {'N': True, 'S': True, 'E': True, 'W': True}