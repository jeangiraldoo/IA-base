from heapq import heappush, heappop
import math
import time

# ---------------------------------------------
# Heurística: distancia Manhattan
# ---------------------------------------------
def heuristic(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


# ---------------------------------------------
# Costo según el terreno
# ---------------------------------------------
def terrain_cost(matrix, pos):
    value = matrix[pos[0]][pos[1]]
    if value == 1:  # obstáculo
        return math.inf
    elif value == 3:  # rocoso
        return 3
    elif value == 4:  # volcánico
        return 5
    else:
        return 1


# ---------------------------------------------
# Vecinos válidos
# ---------------------------------------------
def get_neighbors(matrix, pos):
    x, y = pos
    directions = [(1,0), (-1,0), (0,1), (0,-1)]
    neighbors = []

    for dx, dy in directions:
        nx, ny = x + dx, y + dy
        if 0 <= nx < len(matrix) and 0 <= ny < len(matrix[0]):
            if matrix[nx][ny] != 1:
                neighbors.append((nx, ny))
    return neighbors


# ---------------------------------------------
# Reconstrucción del camino
# ---------------------------------------------
def reconstruct_path(came_from, start, goal):
    path = [goal]
    while path[-1] != start:
        path.append(came_from[path[-1]])
    path.reverse()
    return path


# ---------------------------------------------
# A* normal entre dos puntos
# ---------------------------------------------
def a_star_single(matrix, start, goal):
    open_list = []
    heappush(open_list, (0, start))
    came_from = {}
    g_score = {start: 0}

    while open_list:
        _, current = heappop(open_list)

        if current == goal:
            return reconstruct_path(came_from, start, goal), g_score[current]

        for neighbor in get_neighbors(matrix, current):
            tentative_g = g_score[current] + terrain_cost(matrix, neighbor)
            if neighbor not in g_score or tentative_g < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g
                f_score = tentative_g + heuristic(neighbor, goal)
                heappush(open_list, (f_score, neighbor))
    return None, math.inf


# ---------------------------------------------
# A* MULTI-OBJETIVO: de 2 → 6 → 6 → 6
# ---------------------------------------------
def a_star(matrix, start, goals):
    start_time = time.time()
    total_cost = 0
    all_paths = []
    expanded_nodes = 0
    depth_total = 0

    current = start
    pending_goals = goals.copy()

    while pending_goals:
        # Escoge el más cercano por heurística
        nearest = min(pending_goals, key=lambda g: heuristic(current, g))
        path, cost = a_star_single(matrix, current, nearest)
        if not path:
            break
        all_paths.append(path)
        total_cost += cost
        depth_total += len(path)
        expanded_nodes += len(path)
        pending_goals.remove(nearest)
        current = nearest

    elapsed = time.time() - start_time

    return {
        "paths": all_paths,
        "cost": total_cost,
        "depth": depth_total,
        "expanded_nodes": expanded_nodes,
        "time": round(elapsed, 4)
    }
