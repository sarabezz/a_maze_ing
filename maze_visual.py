# solo dibuja el laberinto no depende de generarlo
import os


def print_maze(maze, show_path=True):
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
            generate_func(maze)
            path_cells = BFS(maze)
            
        elif option == '2':
            show_path = not show_path
            
        elif option == '3':
            break
            
        else:
            print("Opción no válida")

def reset_maze(maze):
    for row in range(maze.height):
        for col in range(maze.width):
            cell = maze.grid[row][col]
            if not cell.blocked:    # no tocamos las celdas del "42"
                cell.visited = False
                cell.in_path = False
                cell.walls = {'N': True, 'S': True, 'E': True, 'W': True}