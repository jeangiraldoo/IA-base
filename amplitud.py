import time
from collections import deque
from world_loader import build_matrix_from_txt_file 

# --- Constantes del mundo ---
LIBRE = 0
OBSTACULO = 1
ASTRONAUTA = 2
ROCOSO = 3
VOLCANICO = 4
NAVE = 5
MUESTRA = 6

MUNDO = None
POS_INICIAL_ASTRONAUTA = None
POS_MUESTRAS = None  
POS_NAVE = None
NUM_MUESTRAS = 0
FILAS_MUNDO = 0
COLUMNAS_MUNDO = 0


def cargar_mundo_local(nombre_archivo: str) -> bool:
    
    global MUNDO, POS_INICIAL_ASTRONAUTA, POS_MUESTRAS, POS_NAVE, NUM_MUESTRAS
    global FILAS_MUNDO, COLUMNAS_MUNDO

    mundo_raw = build_matrix_from_txt_file()
    if mundo_raw is None:
        print("Error: no se pudo construir la matriz del mundo.")
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

    if pos_astronauta is None:
        print("Error: no se encontró la posición del astronauta (2).")
        return False
    if pos_nave is None:
        print("Error: no se encontró la nave (5).")
        return False
    if not muestras:
        print("Error: no se encontraron muestras (6).")
        return False

    mundo_raw[pos_astronauta[0]][pos_astronauta[1]] = LIBRE

    MUNDO = mundo_raw
    POS_INICIAL_ASTRONAUTA = pos_astronauta
    POS_NAVE = pos_nave
    POS_MUESTRAS = tuple(muestras) 
    NUM_MUESTRAS = len(POS_MUESTRAS)

    return True

def estado_inicial():
    """
    Calcula el estado inicial completo.
    """
    pos = POS_INICIAL_ASTRONAUTA
    muestras_iniciales = [0] * NUM_MUESTRAS
    
    en_nave_inicial = (pos == POS_NAVE)
    combustible_inicial = 20 if en_nave_inicial else 0

    # Comprobar si el astronauta empieza SOBRE una muestra
    if pos in POS_MUESTRAS:
        idx = POS_MUESTRAS.index(pos)
        muestras_iniciales[idx] = 1

    return (pos, tuple(muestras_iniciales), en_nave_inicial, combustible_inicial)


def es_meta(estado):
    """
    La meta es tener todas las muestras.
    """
    _, muestras_recolectadas, _, _ = estado
    return all(muestras_recolectadas) # all( (1, 1, 1) ) es True


def generar_sucesores(estado):
    """
    Genera sucesores válidos 
    Devuelve lista de tuplas: [(nuevo_estado, accion_str), ...]
    """
    sucesores = []
    (r, c), muestras, en_nave, combustible = estado
    
    movimientos = [((-1, 0), 'Norte'), ((1, 0), 'Sur'), ((0, -1), 'Oeste'), ((0, 1), 'Este')]

    for (dr, dc), accion in movimientos:
        r_n, c_n = r + dr, c + dc
        
        # 1. Verifica límites del mundo
        if not (0 <= r_n < FILAS_MUNDO and 0 <= c_n < COLUMNAS_MUNDO):
            continue
            
        # 2. Verifica obstáculos
        if MUNDO[r_n][c_n] == OBSTACULO:
            continue

        pos_nueva = (r_n, c_n)

        # 3. Calcular nuevo estado de nave y combustible
        nuevo_combustible = combustible
        nuevo_en_nave = en_nave

        if en_nave:
            if combustible > 0:
                nuevo_combustible -= 1  # Gasta combustible
            else:
                nuevo_en_nave = False  # Se acaba el combustible, sigue a pie

        # 4. Verificar si llega a la nave (recarga)
        if pos_nueva == POS_NAVE:
            nuevo_en_nave = True
            nuevo_combustible = 20

        # 5. Actualizar muestras si se pisa una casilla de muestra
        nuevas_muestras = list(muestras)
        if pos_nueva in POS_MUESTRAS:
            idx = POS_MUESTRAS.index(pos_nueva)
            nuevas_muestras[idx] = 1
            
        # 6. Crear el estado sucesor completo
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
    return camino


def mostrar_mundo_inicial():

    if MUNDO is None:
        if not cargar_mundo_local("Prueba1.txt"):
            print("El mundo no está cargado.")
            return

    print("\n--- ESTADO INICIAL DEL MUNDO ---")
    simbolos = {
        LIBRE: "·", OBSTACULO: "█", ROCOSO: "R",
        VOLCANICO: "V", NAVE: "N", MUESTRA: "M"
    }
    
    # Encabezados de columnas
    encabezado = "   "
    for i in range(COLUMNAS_MUNDO):
        encabezado += f" {i:1}" # Asume < 10 columnas, ajusta si es necesario
    print(encabezado)
    print("  " + "-"*(COLUMNAS_MUNDO*2 + 3))

    for i, fila in enumerate(MUNDO):
        linea = f"{i:2d} |" # {i:2d} para alinear números de 0-99
        for j, valor in enumerate(fila):
            pos = (i, j)
            if pos == POS_INICIAL_ASTRONAUTA:
                linea += " A"
            elif pos == POS_NAVE:
                linea += " N"
            elif pos in POS_MUESTRAS:
                linea += " M"
            else:
                linea += f" {simbolos[valor]}"
        print(linea)
    print("  " + "-"*(COLUMNAS_MUNDO*2 + 3))


def imprimir_reporte_local(algoritmo_tipo, estado_meta, nodos_expandidos, tiempo_inicio, padres):
    """
    Imprime el reporte, ahora mostrando el estado completo para mejor visualización.
    """
    tiempo_total = time.perf_counter() - tiempo_inicio

    print("\n" + "="*60)
    print(f" REPORTE DE BÚSQUEDA: {algoritmo_tipo}")
    print("="*60)
    
    if estado_meta is None:
        print(f"  Fracaso. No se encontró solución.")
        print(f"  Nodos Expandidos:   {nodos_expandidos}")
        print(f"  Tiempo de Cómputo:  {tiempo_total:.6f} segundos")
        print("="*60 + "\n")
        return

    print(f"  Éxito. Solución encontrada.")
    print(f"  Nodos Expandidos:   {nodos_expandidos}")
    
    camino = reconstruir_camino(padres, estado_meta)
    profundidad = max(0, len(camino) - 1)
    
    print(f"  Profundidad Árbol:  {profundidad} movimientos")
    print(f"  Tiempo de Cómputo:  {tiempo_total:.6f} segundos")

    print("\n  --- Animación de Movimientos y Posiciones ---")
    for i, (estado, accion) in enumerate(camino):
        pos, muestras, en_nave, combustible = estado
        
        muestras_str = f"Muestras: {sum(muestras)}/{NUM_MUESTRAS}"
        nave_str = "EN NAVE" if en_nave else "A PIE   "
        comb_str = f"Comb: {combustible:02d}"
        
        if i == 0:
            print(f"  Paso {i:02d}: Inicio  -> {str(pos):<8} | {muestras_str} | {nave_str} | {comb_str}")
        else:
            print(f"  Paso {i:02d}: {accion:<6} en {str(pos):<8} | {muestras_str} | {nave_str} | {comb_str}")

    print(f"  Fin en {camino[-1][0][0]}")
    print("="*60 + "\n")


def ejecutar_amplitud():
    """
    Ejecuta la Búsqueda por Amplitud (BFS) con el estado completo.
    """
    print("\nIniciando Búsqueda por Amplitud (BFS)...")
    if not cargar_mundo_local("Prueba1.txt"):
        print("Fracaso: no se pudo cargar el mundo.")
        return False

    tiempo_inicio = time.perf_counter()
    inicial = estado_inicial()

    frontera = deque([inicial])
    visitados = {(inicial[0], inicial[1])}
    padres = {inicial: (None, None)}  # estado -> (padre, accion)
    nodos_expandidos = 0

    while frontera:
        print(f"Frontera: {frontera}, nodo expandido: {nodos_expandidos}")
        actual = frontera.popleft()


        if es_meta(actual):
            print("¡Solución encontrada!")
            imprimir_reporte_local('Amplitud', actual, nodos_expandidos, tiempo_inicio, padres)
            
            return {
                "nodos": nodos_expandidos,
                "profundidad": len(padres),
                "tiempo": round(time.perf_counter() - tiempo_inicio, 3),
                "muestras": 3
            }

        # Incrementar contador de expansión
        nodos_expandidos += 1

        # Si no es meta, generar sucesores
        for nuevo_estado, accion in generar_sucesores(actual):
            sig_nuevo = (nuevo_estado[0], nuevo_estado[1])
            if sig_nuevo not in visitados:
                visitados.add(sig_nuevo)
                padres[nuevo_estado] = (actual, accion)
                frontera.append(nuevo_estado)

    # Si la frontera se vacía, no hay solución
    print(f"Fracaso: No se encontró solución.")
    imprimir_reporte_local('Amplitud', None, nodos_expandidos, tiempo_inicio, padres)
    return False


# --- Punto de entrada para probar ---
if __name__ == "__main__":
    mostrar_mundo_inicial()
    ejecutar_amplitud()