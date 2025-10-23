import pygame
import time
from collections import deque
from world_loader import build_matrix_from_txt_file

#  Colores definidos 
COLORS = {
    0: (200, 200, 200),   # Terreno normal
    1: (50, 50, 50),      # Obstaculo
    2: (0, 0, 255),       # Astronauta normal
    3: (139, 69, 19),     # Rocoso
    4: (255, 69, 0),      # Volcanico
    5: (0, 255, 255),     # Nave
    6: (0, 255, 0),       # Muestra científica
    ".": (255, 255, 0),   # Camino normal
    "*": (160, 32, 240),  # Camino con nave 
}

# Orden oficial de operadores 
direcciones = [(-1, 0), (1, 0), (0, -1), (0, 1)]  
nombres_mov = ["arriba", "abajo", "izquierda", "derecha"]

# Funcion para dibujar el mundo 
def mostrar_mundo_pygame(screen, mundo, cell_size, fuente, pasos_nave):
    for i, fila in enumerate(mundo):
        for j, valor in enumerate(fila):
            # Color base de la celda
            color = COLORS.get(valor, (255, 255, 255))
            pygame.draw.rect(screen, color, (j * cell_size, i * cell_size, cell_size, cell_size))
            pygame.draw.rect(screen, (0, 0, 0), (j * cell_size, i * cell_size, cell_size, cell_size), 1)

            # Mostrar texto "M1", "M2", etc.
            if isinstance(valor, str) and valor.startswith("M"):
                texto = fuente.render(valor, True, (0, 0, 0))
                screen.blit(texto, (j * cell_size + cell_size // 4, i * cell_size + cell_size // 6))

            # Astronauta visual
            if valor == 2:
                color_astronauta = COLORS["*"] if pasos_nave > 0 else COLORS[2]
                pygame.draw.circle(screen, color_astronauta,
                                   (j * cell_size + cell_size // 2, i * cell_size + cell_size // 2),
                                   cell_size // 3)

    pygame.display.flip()

def es_valido(x, y, filas, columnas):
    return 0 <= x < filas and 0 <= y < columnas

# DFS evitando ciclos (visual) 
def ejecutar_profundidad_animada(screen, mundo):
    filas, columnas = len(mundo), len(mundo[0])
    cell_size = min(600 // columnas, 600 // filas)
    fuente = pygame.font.SysFont("Arial", 16)

    # Buscar astronauta
    inicio = None
    for i in range(filas):
        for j in range(columnas):
            if mundo[i][j] == 2:
                inicio = (i, j)
    total_muestras = sum(fila.count(6) for fila in mundo)

    pila = deque()
    pila.append((inicio, []))
    visitados = set()
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

        visitados.add((x, y))
        nodos_expandidos += 1
        profundidad_actual = len(camino)
        profundidad_maxima = max(profundidad_maxima, profundidad_actual)

        # Control de modo "nave" 
        # Si pisa la nave, activa 20 pasos de modo especial
        if mundo[x][y] == 5 and pasos_nave == 0:
            pasos_nave = 20
            
        # Solo reducir contador en los frames siguientes, no en el inicial
        elif pasos_nave > 0:
            pasos_nave -= 1

        # Pintar la casilla ---
        # Nunca pintar la posicion inicial ni la nave
        if mundo[x][y] not in [2, 5, 6] and not isinstance(mundo[x][y], str):
            if pasos_nave > 0:
                mundo[x][y] = '*'  # camino con nave
            else:
                mundo[x][y] = '.'  # camino normal

        # Mostrar mundo actualizado
        screen.fill((255, 255, 255))
        mostrar_mundo_pygame(screen, mundo, cell_size, fuente, pasos_nave)
        time.sleep(0.5)

        # Detectar muestra
        if mundo[x][y] == 6:
            num_muestra = len(muestras_encontradas) + 1
            muestras_encontradas.append((f"Muestra {num_muestra}", (x, y), camino))
            mundo[x][y] = f"M{num_muestra}"  # reemplazar por texto
            if len(muestras_encontradas) == total_muestras:
                break

        # Expandir vecinos en orden 
        for i, (dx, dy) in reversed(list(enumerate(direcciones))):
            nx, ny = x + dx, y + dy
            if not es_valido(nx, ny, filas, columnas):
                continue
            valor = mundo[nx][ny]
            if valor == 1:
                continue
            # Se puede devolver por nave o muestra
            if valor not in [5, 6] and (nx, ny) in visitados:
                continue
            pila.append(((nx, ny), camino + [nombres_mov[i]]))

    fin_tiempo = time.time()
    return {
        "nodos": nodos_expandidos,
        "profundidad": profundidad_maxima,
        "tiempo": round(fin_tiempo - inicio_tiempo, 3),
        "muestras": muestras_encontradas
    }
