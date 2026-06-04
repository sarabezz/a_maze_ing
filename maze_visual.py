# solo dibuja el laberinto no depende de generarlo
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'mlx_CLXV/python/src'))
from mlx import Mlx
from maze_core import BFS, mark_path, reset_maze, DIRECTIONS

# colores
BLACK  = 0x000000
GOLD   = 0xB8860B
CYAN   = 0x00BFFF
PINK   = 0xFF69B4
RED    = 0xFF0000
GRAY   = 0xBBBBBB

WALL_COLORS = [GOLD, 0x4169E1, 0x228B22, 0xAA0000]  # lista de colores para cambiar

def draw_rect(data, sl, x, y, w, h, color):
    pixel = (0xFF000000 | color).to_bytes(4, 'little')
    for dy in range(h):
        for dx in range(w):
            offset = (y + dy) * sl + (x + dx) * 4
            data[offset:offset+4] = pixel

def draw_maze(data, sl, maze, cell_size, show_path, wall_color):
    wall_thickness = max(2, cell_size // 5)

    for row in range(maze.height):
        for col in range(maze.width):
            cell  = maze.grid[row][col]
            x = col * cell_size
            y = row * cell_size

            # rellenamos la celda entera de negro
            draw_rect(data, sl, x, y, cell_size, cell_size, BLACK)

            if cell.blocked:
                draw_rect(data, sl, x, y, cell_size, cell_size, GRAY)
                continue

            # camino
            if show_path and cell.in_path:
                draw_rect(data, sl, x, y, cell_size, cell_size, CYAN)

            # entrada y salida
            if (row, col) == maze.start:
                draw_rect(data, sl, x, y, cell_size, cell_size, PINK)
            if (row, col) == maze.end:
                draw_rect(data, sl, x, y, cell_size, cell_size, RED)

            # paredes
            if cell.walls['N']:
                draw_rect(data, sl, x, y, cell_size, wall_thickness, wall_color)
            if cell.walls['S']:
                draw_rect(data, sl, x, y + cell_size - wall_thickness, cell_size, wall_thickness, wall_color)
            if cell.walls['W']:
                draw_rect(data, sl, x, y, wall_thickness, cell_size, wall_color)
            if cell.walls['E']:
                draw_rect(data, sl, x + cell_size - wall_thickness, y, wall_thickness, cell_size, wall_color)

def menu(maze, path_cells, generate_func):
    cell_size = min(800 // maze.width, 800 // maze.height)
    win_w = maze.width * cell_size
    menu_height = 40
    win_h = maze.height * cell_size + menu_height

    mlx = Mlx()
    mlx_ptr = mlx.mlx_init()
    win = mlx.mlx_new_window(mlx_ptr, win_w, win_h, "a_maze_ing")
    img = mlx.mlx_new_image(mlx_ptr, win_w, win_h)
    data, bpp, sl, iformat = mlx.mlx_get_data_addr(img)

    show_path = [True]       # lista para poder modificarlo dentro del hook
    color_index = [0]        # índice del color actual

    def redraw():
        draw_maze(data, sl, maze, cell_size, show_path[0], WALL_COLORS[color_index[0]])
        mlx.mlx_put_image_to_window(mlx_ptr, win, img, 0, 0)
        mlx.mlx_string_put(mlx_ptr, win, 10, maze.height * cell_size + 10, 0xFFFFFF, "1-Regenerar  2-Camino  3-Color  ESC-Salir")

    def key_hook(key, unused):
        if key == 49:    # tecla 1 — regenerar
            reset_maze(maze)
            generate_func(maze)
            path = BFS(maze)
            mark_path(maze, path)
            redraw()
        elif key == 50:  # tecla 2 — mostrar/ocultar camino
            show_path[0] = not show_path[0]
            redraw()
        elif key == 51:  # tecla 3 — cambiar color
            color_index[0] = (color_index[0] + 1) % len(WALL_COLORS)
            redraw()
        elif key == 65307:  # ESC — salir
            mlx.mlx_loop_exit(mlx_ptr)

    redraw()
    mlx.mlx_key_hook(win, key_hook, None)
    mlx.mlx_hook(win, 33, 0, lambda unused: mlx.mlx_loop_exit(mlx_ptr), None)
    mlx.mlx_loop(mlx_ptr)




"""def print_maze(maze, show_path=True):
    for row in range(maze.height): # voy fila por fila
        
        # parte superior de la fila — pared Norte
        for col in range(maze.width): #recorro cada columna de cada fila
            cell = maze.grid[row][col]
            print('+', end='')
            print('---' if cell.walls['N'] else '   ', end='')
        print('+')

        # parte del contenido — paredes Oeste/Este y contenido
        for col in range(maze.width):
            cell = maze.grid[row][col]
            print('|' if cell.walls['W'] else ' ', end='')
            
            if cell.blocked:
                print('###', end='')
            elif (row, col) == maze.start:
                print(' S ', end='')
            elif (row, col) == maze.end:
                print(' E ', end='')
            elif show_path and cell.in_path:
                print(' * ', end='')
            else:
                print('   ', end='')
        
        # cerramos la última celda de la fila con su pared Este
        print('|' if maze.grid[row][-1].walls['E'] else ' ')

    # última fila — pared Sur de la última fila
    for col in range(maze.width):
        print('+', end='')
        print('---' if maze.grid[maze.height - 1][col].walls['S'] else '   ', end='')
    print('+')

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def menu(maze, path_cells, generate_func):
    show_path = True
    wall_color = ''      # para ASCII usamos caracteres, no colores aún
    
    while True:
        clear_screen()
        print_maze(maze, show_path)
        print("\nOpciones:")
        print("  1 — Regenerar laberinto")
        print("  2 — Mostrar/Ocultar camino")
        print("  3 — Salir")
        
        option = input("\nElige una opción: ").strip()
        
        if option == '1':
            reset_maze(maze)
            generate_func(maze)
            path_cells = BFS(maze)
            mark_path(maze, path_cells)
            
        elif option == '2':
            show_path = not show_path
            
        elif option == '3':
            break
            
        else:
            print("Opción no válida")"""
