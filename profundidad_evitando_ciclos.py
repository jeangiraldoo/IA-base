import pygame
import time
import copy
from collections import deque

#  Colores definidos
COLORS = {
    0: (200, 200, 200),  # Terreno normal
    1: (50, 50, 50),  # Obstaculo
    2: (0, 0, 255),  # Astronauta normal
    3: (139, 69, 19),  # Rocoso
    4: (255, 69, 0),  # Volcanico
    5: (0, 255, 255),  # Nave
    6: (0, 255, 0),  # Muestra científica
    ".": (255, 255, 0),  # Camino normal
    "*": (160, 32, 240),  # Camino con nave
}

# Orden oficial de operadores
direcciones = [(-1, 0), (1, 0), (0, -1), (0, 1)]
nombres_mov = ["arriba", "abajo", "izquierda", "derecha"]


def es_valido(x, y, filas, columnas):
    return 0 <= x < filas and 0 <= y < columnas


# DFS evitando ciclos (visual)
def ejecutar_profundidad_animada(matrix):
    matrix_copy = copy.deepcopy(matrix)
    filas, columnas = len(matrix_copy), len(matrix_copy[0])

    # Buscar astronauta
    inicio = None
    for i in range(filas):
        for j in range(columnas):
            if matrix_copy[i][j] == 2:
                inicio = (i, j)
    total_muestras = sum(fila.count(6) for fila in matrix_copy)

    pila = deque()
    pila.append((inicio, []))
    visitados = []
    muestras_encontradas = []
    nodos_expandidos = 0
    profundidad_maxima = 0
    inicio_tiempo = time.time()

    pasos_nave = 0  # contador de movimientos con nave
    corriendo = True

    while pila and corriendo:
        (x, y), camino = pila.pop()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                corriendo = False
                return None

        if (x, y) in visitados:
            continue

        visitados.append((x, y))
        nodos_expandidos += 1
        profundidad_actual = len(camino)
        profundidad_maxima = max(profundidad_maxima, profundidad_actual)

        # Control de modo "nave"
        # Si pisa la nave, activa 20 pasos de modo especial
        if matrix_copy[x][y] == 5 and pasos_nave == 0:
            pasos_nave = 20

        # Solo reducir contador en los frames siguientes, no en el inicial
        elif pasos_nave > 0:
            pasos_nave -= 1

        # Pintar la casilla ---
        # Nunca pintar la posicion inicial ni la nave
        if matrix_copy[x][y] not in [2, 5, 6] and not isinstance(
            matrix_copy[x][y], str
        ):
            if pasos_nave > 0:
                matrix_copy[x][y] = "*"  # camino con nave
            else:
                matrix_copy[x][y] = "."  # camino normal

        time.sleep(0.5)

        # Detectar muestra
        if matrix_copy[x][y] == 6:
            num_muestra = len(muestras_encontradas) + 1
            muestras_encontradas.append((f"Muestra {num_muestra}", (x, y), camino))
            matrix_copy[x][y] = f"M{num_muestra}"  # reemplazar por texto
            if len(muestras_encontradas) == total_muestras:
                break

        # Expandir vecinos en orden
        for i, (dx, dy) in reversed(list(enumerate(direcciones))):
            nx, ny = x + dx, y + dy
            if not es_valido(nx, ny, filas, columnas):
                continue
            valor = matrix_copy[nx][ny]
            if valor == 1:
                continue
            # Se puede devolver por nave o muestra
            if valor not in [5, 6] and (nx, ny) in visitados:
                continue
            pila.append(((nx, ny), camino + [nombres_mov[i]]))

    fin_tiempo = time.time()
    print("Visitados:")
    print(visitados)
    return {
        "algorithm_name": "Profundidad",
        "expanded_nodes": nodos_expandidos,
        "depth": profundidad_maxima,
        "time": round(fin_tiempo - inicio_tiempo, 3),
        "samples": muestras_encontradas,
        "paths": visitados,
    }
