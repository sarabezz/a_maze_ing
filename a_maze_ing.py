# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    a_maze_ing.py                                      :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: sarabermudez <sarabermudez@student.42.f    +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2026/01/14 13:35:54 by sarabermude       #+#    #+#              #
#    Updated: 2026/06/03 17:10:35 by sarabermude      ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

# leer el config, validar parámetros, llamar a maze_core.py, y gestionar errores
import sys # intercatuar con el sistema, leer argumentos, salir del programa
import random
from maze_core import Maze, four2, generate_maze, BFS, save_maze, mark_path, DIRECTIONS, OPPOSITE 
from maze_visual import menu


def read_config(filename):
    config = {} # aquí guardaremos los datos del maze
    
    try:
        with open(filename, 'r') as f:
            for line in f:
                line = line.strip() # quita espacios y saltos de línea
                
                # ignoramos líneas vacías y comentarios
                if not line or line.startswith('#'):
                    continue
                
                # comprobamos que la línea tiene el formato KEY=VALUE
                if '=' not in line:
                    raise ValueError(f"Invalid line: '{line}'")
                
                key, value = line.split('=', 1) # (dónde cortar, n max de cortes) ej "A=B=C" -> ['A', 'B=C']
                config[key.strip()] = value.strip()
                
    except FileNotFoundError:
        print(f"Error: file not found '{filename}'")
        sys.exit(1)
    
    return config

def validate_config(config):
    required = ['WIDTH', 'HEIGHT', 'ENTRY', 'EXIT', 'OUTPUT_FILE', 'PERFECT']
    
    # comprobamos que están todas las claves obligatorias
    for key in required:
        if key not in config:
            print(f"Error: missing key '{key}' in config")
            sys.exit(1)
    
    try:
        width = int(config['WIDTH'])
        height = int(config['HEIGHT'])
    except ValueError:
        print("Error: WIDTH y HEIGHT must be numbers")
        sys.exit(1)
    
    if width < 1 or height < 1:
        print("Error: WIDTH y HEIGHT must be higher than 0")
        sys.exit(1)
    
    try:
        entry_x, entry_y = map(int, config['ENTRY'].split(',')) # convierte "3,5" → (3,5)
        exit_x, exit_y = map(int, config['EXIT'].split(','))
    except ValueError:
        print("Error: ENTRY y EXIT must have the format x,y")
        sys.exit(1)
    
    # comprobamos que están dentro del laberinto
    if not (0 <= entry_x < width and 0 <= entry_y < height):
        print("Error: ENTRY out of maze limits")
        sys.exit(1)
    
    if not (0 <= exit_x < width and 0 <= exit_y < height):
        print("Error: EXIT out of maze limits")
        sys.exit(1)
    
    if (entry_x, entry_y) == (exit_x, exit_y):
        print("Error: ENTRY y EXIT cannot be same cell")
        sys.exit(1)
    
    perfect = config['PERFECT'].lower()
    if perfect not in ('true', 'false'):
        print("Error: PERFECT must be True or False")
        sys.exit(1)
    
    # devolvemos los valores ya convertidos
    return {
        'width': width,
        'height': height,
        'start': (entry_y, entry_x),   # convertimos x,y → fila,col
        'end': (exit_y, exit_x),        # convertimos x,y → fila,col
        'output_file': config['OUTPUT_FILE'],
        'perfect': perfect == 'true',
        'seed': config.get('SEED', None)  # opcional
    }

def add_loops(maze, num_loops=10):
    for _ in range(num_loops):
        row = random.randint(0, maze.height - 2)
        col = random.randint(0, maze.width - 2)
        cell = maze.grid[row][col]
        
        if not cell.blocked:
            # abrimos una pared aleatoria hacia el Sur o el Este
            direction = random.choice(['S', 'E'])
            drow, dcol = DIRECTIONS[direction]
            nrow, ncol = row + drow, col + dcol
            neighbor = maze.grid[nrow][ncol]
            
            if not neighbor.blocked:
                cell.walls[direction] = False
                neighbor.walls[OPPOSITE[direction]] = False

def main():
    if len(sys.argv) != 2:
        print(f"Use: python3 a_maze_ing.py config.txt")
        sys.exit(1)
    
    config = read_config(sys.argv[1])
    params = validate_config(config)
    
    # semilla para reproducibilidad
    if params['seed']:
        random.seed(params['seed'])
    
    # creamos el laberinto
    maze = Maze(params['width'], params['height'], params['start'], params['end'])
    
    # patrón "42"
    four2(maze)
    
    # generamos
    generate_maze(maze)
    
    # si no es perfecto añadimos bucles extra
    if not params['perfect']:
        add_loops(maze)
    
    # resolvemos
    path = BFS(maze)
    if path is None:
        print("Error: path not found between start and end")
        sys.exit(1)
    
    mark_path(maze, path)
    
    # guardamos
    save_maze(maze, path, params['output_file'])
    
    # mostramos
    menu(maze, path, lambda m: generate_maze(m))

if __name__ == "__main__":
    main()