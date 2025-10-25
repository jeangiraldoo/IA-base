from heapq import heappush, heappop
import math
import time

# ---------------------------------------------
# Heurística: distancia Manhattan
# ---------------------------------------------
def heuristic(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


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
# Avara entre dos puntos
# ---------------------------------------------
def greedy_single(matrix, start, goal):
    open_list = []
    heappush(open_list, (heuristic(start, goal), start))
    came_from = {}
    visited = set()
    expanded_nodes = 0

    while open_list:
        _, current = heappop(open_list)
        expanded_nodes += 1

        if current == goal:
            return reconstruct_path(came_from, start, goal), expanded_nodes

        visited.add(current)

        for neighbor in get_neighbors(matrix, current):
            if neighbor not in visited:
                came_from[neighbor] = current
                priority = heuristic(neighbor, goal)
                heappush(open_list, (priority, neighbor))

    return None, expanded_nodes


# ---------------------------------------------
# Algoritmo Avara MULTI-OBJETIVO (2 → 6 → 6 → 6)
# ---------------------------------------------
def greedy_best_first_search(matrix, start, goals):
    start_time = time.time()
    all_paths = []
    total_nodes = 0
    total_depth = 0

    current = start
    pending_goals = goals.copy()

    while pending_goals:
        nearest = min(pending_goals, key=lambda g: heuristic(current, g))
        path, nodes = greedy_single(matrix, current, nearest)
        if not path:
            break
        all_paths.append(path)
        total_nodes += nodes
        total_depth += len(path)
        pending_goals.remove(nearest)
        current = nearest

    elapsed = time.time() - start_time

    return {
        "paths": all_paths,
        "cost": sum(len(p) for p in all_paths),
        "depth": total_depth,
        "expanded_nodes": total_nodes,
        "time": round(elapsed, 4)
    }
