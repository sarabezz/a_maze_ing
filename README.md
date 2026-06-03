*Este proyecto ha sido creado como parte del currículo de 42 por sarabermudez.*

# A-Maze-ing

## Descripción
A-Maze-ing es un generador y solucionador de laberintos implementado en **Python**.  
El objetivo del proyecto es construir laberintos aleatorios de cualquier tamaño definido por el usuario, generar rutas óptimas desde un punto de inicio hasta un punto final utilizando el algoritmo **BFS**, y guardar los laberintos en formato hexadecimal.  

Además, se incluye un **patrón especial “4-2”** que bloquea ciertas celdas del centro del laberinto, agregando dificultad y variabilidad a la generación del laberinto.

El proyecto permite:
- Generar laberintos de tamaño configurable.
- Marcar automáticamente la ruta más corta desde el inicio hasta la salida.
- Imprimir laberintos en la consola, mostrando paredes, celdas bloqueadas y el camino encontrado.
- Guardar laberintos y rutas en un archivo `maze.txt` para análisis o uso posterior.

## Instrucciones

### Requisitos
- Python 3.9 o superior
- Virtualenv (opcional, recomendado)

### Instalación
1. Crear un entorno virtual (opcional pero recomendado):
```bash
python3 -m venv venv39
source venv39/bin/activate
