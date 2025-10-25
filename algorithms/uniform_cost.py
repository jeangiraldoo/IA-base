import time
import heapq
from typing import Optional, Tuple, Set, FrozenSet

NUM_MUESTRAS = 3


def ejecutar_costo_uniforme_desde_matriz(matrix) -> Optional[dict]:
    """
    Ejecuta Uniform Cost Search usando únicamente la 'matrix' como entrada.
    Devuelve un diccionario con las mismas llaves que tu función de amplitud:
      - algorithm_name, cost, paths (lista de (r,c)), expanded_nodes, time, profundidad, muestras
    Si la matrix no contiene un estado inicial válido (valor 2) devuelve None.
    """
    tiempo_inicio = time.perf_counter()

    if not matrix or not isinstance(matrix, (list, tuple)) or not matrix[0]:
        return None
    n_rows = len(matrix)
    n_cols = len(matrix[0])

    start = None
    sample_positions = set()
    for r in range(n_rows):
        for c in range(n_cols):
            val = matrix[r][c]
            if val == 2:
                start = (r, c)
            if val == 6:
                sample_positions.add((r, c))
    if start is None:
        return None

    def costo_base_de_celda(cell_value: int) -> float:
        # 0: libre  -> 1
        # 1: obstáculo -> no aplicable (imposible entrar)
        # 2: astronauta (inicio) -> tratar como libre -> 1
        # 3: rocoso -> 3
        # 4: volcánico -> 5
        # 5: nave -> tratar como libre -> 1
        # 6: muestra -> tratar como libre -> 1
        if cell_value == 3:
            return 3.0
        if cell_value == 4:
            return 5.0

        return 1.0

    MOVES = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    inicial_estado = (start[0], start[1], 0, frozenset())

    frontera = []
    heapq.heappush(frontera, (0.0, inicial_estado))

    costos = {inicial_estado: 0.0}
    padres = {inicial_estado: (None, None)}
    nodos_expandidos = 0

    def es_meta(estado) -> bool:
        _, _, _, collected = estado
        return len(collected) >= NUM_MUESTRAS

    def reconstruir_camino(padres_map, estado_final) -> list:
        camino = []
        cur = estado_final
        while cur is not None:
            padre, accion = padres_map.get(cur, (None, None))
            camino.append(((cur[0], cur[1]), accion))
            cur = padre
        camino.reverse()
        return camino

    def es_transitable(r: int, c: int) -> bool:
        if r < 0 or r >= n_rows or c < 0 or c >= n_cols:
            return False
        return matrix[r][c] != 1

    while frontera:
        costo_actual, actual = heapq.heappop(frontera)
        if costos.get(actual, float("inf")) < costo_actual - 1e-9:
            continue

        nodos_expandidos += 1

        if es_meta(actual):
            camino = reconstruir_camino(padres, actual)
            path_positions = [estado_pos for estado_pos, _ in camino]
            profundidad = max(0, len(path_positions) - 1)
            tiempo_total = time.perf_counter() - tiempo_inicio
            return {
                "algorithm_name": "Costo Uniforme",
                "cost": round(costo_actual, 3),
                "paths": path_positions,
                "expanded_nodes": nodos_expandidos,
                "time": round(tiempo_total, 3),
                "depth": profundidad,
                "samples": NUM_MUESTRAS,
            }

        r, c, fuel_rem, collected_fs = actual
        collected: Set[Tuple[int, int]] = set(collected_fs)

        for dr, dc in MOVES:
            nr, nc = r + dr, c + dc
            if not es_transitable(nr, nc):
                continue

            cell_val = matrix[nr][nc]
            base_cost = costo_base_de_celda(cell_val)

            if fuel_rem > 0:
                movimiento_cost = base_cost / 2.0
                nuevo_fuel = fuel_rem - 1
            else:
                movimiento_cost = base_cost
                nuevo_fuel = 0

            nuevo_costo = costo_actual + movimiento_cost

            if cell_val == 5:
                nuevo_fuel = 20

            nuevo_collected = set(collected)
            if cell_val == 6:
                nuevo_collected.add((nr, nc))

            nuevo_estado = (nr, nc, nuevo_fuel, frozenset(nuevo_collected))

            if nuevo_estado not in costos or nuevo_costo + 1e-9 < costos[nuevo_estado]:
                costos[nuevo_estado] = nuevo_costo
                padres[nuevo_estado] = (actual, (nr, nc))
                heapq.heappush(frontera, (nuevo_costo, nuevo_estado))

    tiempo_total = time.perf_counter() - tiempo_inicio
    return {
        "algorithm_name": "Costo Uniforme",
        "cost": None,
        "paths": [],
        "expanded_nodes": nodos_expandidos,
        "time": round(tiempo_total, 3),
        "depth": None,
        "samples": NUM_MUESTRAS,
    }
