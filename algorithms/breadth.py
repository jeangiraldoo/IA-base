# amplitud.py
import time
from collections import deque
from typing import List, Tuple, Optional

# --- Constantes del mundo ---
LIBRE = 0
OBSTACULO = 1
ASTRONAUTA = 2
ROCOSO = 3
VOLCANICO = 4
NAVE = 5
MUESTRA = 6

# Globals
MUNDO = None
POS_INICIAL_ASTRONAUTA = None
POS_MUESTRAS = None
POS_NAVE = None
NUM_MUESTRAS = 0
FILAS_MUNDO = 0
COLUMNAS_MUNDO = 0

def cargar_mundo_desde_matriz(mundo_raw: List[List[int]]) -> bool:
    """Carga los globals desde la matriz ya creada en memoria."""
    global MUNDO, POS_INICIAL_ASTRONAUTA, POS_MUESTRAS, POS_NAVE, NUM_MUESTRAS
    global FILAS_MUNDO, COLUMNAS_MUNDO

    if mundo_raw is None:
        return False

    pos_astronauta = None
    pos_nave = None
    muestras = []

    FILAS_MUNDO = len(mundo_raw)
    COLUMNAS_MUNDO = len(mundo_raw[0]) if FILAS_MUNDO > 0 else 0

    for i, fila in enumerate(mundo_raw):
        for j, valor in enumerate(fila):
            if valor == ASTRONAUTA:
                pos_astronauta = (i, j)
            elif valor == NAVE:
                pos_nave = (i, j)
            elif valor == MUESTRA:
                muestras.append((i, j))

    if pos_astronauta is None or pos_nave is None or not muestras:
        # No valid world
        return False

    # marca la casilla del astronauta como libre (el estado incluye la posicion)
    mundo_raw[pos_astronauta[0]][pos_astronauta[1]] = LIBRE

    MUNDO = mundo_raw
    POS_INICIAL_ASTRONAUTA = pos_astronauta
    POS_NAVE = pos_nave
    POS_MUESTRAS = tuple(muestras)
    NUM_MUESTRAS = len(POS_MUESTRAS)

    return True

def estado_inicial():
    pos = POS_INICIAL_ASTRONAUTA
    muestras_iniciales = [0] * NUM_MUESTRAS
    en_nave_inicial = (pos == POS_NAVE)
    combustible_inicial = 20 if en_nave_inicial else 0

    if pos in POS_MUESTRAS:
        idx = POS_MUESTRAS.index(pos)
        muestras_iniciales[idx] = 1

    return (pos, tuple(muestras_iniciales), en_nave_inicial, combustible_inicial)

def es_meta(estado):
    _, muestras_recolectadas, _, _ = estado
    return all(muestras_recolectadas)

def generar_sucesores(estado):
    sucesores = []
    (r, c), muestras, en_nave, combustible = estado
    movimientos = [((-1, 0), 'Norte'), ((1, 0), 'Sur'), ((0, -1), 'Oeste'), ((0, 1), 'Este')]

    for (dr, dc), accion in movimientos:
        r_n, c_n = r + dr, c + dc
        if not (0 <= r_n < FILAS_MUNDO and 0 <= c_n < COLUMNAS_MUNDO):
            continue
        if MUNDO[r_n][c_n] == OBSTACULO:
            continue

        pos_nueva = (r_n, c_n)
        nuevo_combustible = combustible
        nuevo_en_nave = en_nave

        if en_nave:
            if combustible > 0:
                nuevo_combustible -= 1
            else:
                nuevo_en_nave = False

        if pos_nueva == POS_NAVE:
            nuevo_en_nave = True
            nuevo_combustible = 20

        nuevas_muestras = list(muestras)
        if pos_nueva in POS_MUESTRAS:
            idx = POS_MUESTRAS.index(pos_nueva)
            nuevas_muestras[idx] = 1

        nuevo_estado = (pos_nueva, tuple(nuevas_muestras), nuevo_en_nave, nuevo_combustible)
        sucesores.append((nuevo_estado, accion))

    return sucesores

def reconstruir_camino(padres, estado_fin):
    camino = []
    actual = estado_fin
    while actual is not None:
        padre, accion = padres.get(actual, (None, None))
        camino.append((actual, accion))
        actual = padre
    camino.reverse()
    return camino  # lista de (estado, accion)

def ejecutar_amplitud_desde_matriz(matrix) -> Optional[dict]:
    """
    Ejecuta BFS sobre la matrix proporcionada y devuelve un diccionario con:
      - algorithm_name, cost, paths (lista de (r,c)), expanded_nodes, time, profundidad, muestras
    Si no puede cargar el mundo o no hay solución devuelve None o dict con None.
    """
    if not cargar_mundo_desde_matriz(matrix):
        return None

    tiempo_inicio = time.perf_counter()
    inicial = estado_inicial()

    frontera = deque([inicial])
    visitados = {(inicial[0], inicial[1])}
    padres = {inicial: (None, None)}
    nodos_expandidos = 0

    while frontera:
        actual = frontera.popleft()

        if es_meta(actual):
            camino = reconstruir_camino(padres, actual)
            # extraer sólo las posiciones en orden
            path_positions = [estado[0] for estado, _ in camino]
            profundidad = max(0, len(path_positions) - 1)
            tiempo_total = time.perf_counter() - tiempo_inicio

            return {
                "algorithm_name": "Amplitud",
                "cost": profundidad,
                "paths": path_positions,
                "expanded_nodes": nodos_expandidos,
                "time": round(tiempo_total, 3),
                "profundidad": profundidad,
                "muestras": NUM_MUESTRAS,
            }

        nodos_expandidos += 1

        for nuevo_estado, accion in generar_sucesores(actual):
            sig_nuevo = (nuevo_estado[0], nuevo_estado[1])
            if sig_nuevo not in visitados:
                visitados.add(sig_nuevo)
                padres[nuevo_estado] = (actual, accion)
                frontera.append(nuevo_estado)

    # sin solución
    tiempo_total = time.perf_counter() - tiempo_inicio
    return {
        "algorithm_name": "Amplitud",
        "cost": None,
        "paths": [],
        "expanded_nodes": nodos_expandidos,
        "time": round(tiempo_total, 3),
        "profundidad": None,
        "muestras": NUM_MUESTRAS,
    }

# Para pruebas rápidas
if __name__ == "__main__":
    # si quieres, aquí puedes colocar una matriz de prueba y ejecutar
    pass
