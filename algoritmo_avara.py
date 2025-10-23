from heapq import heappush, heappop
import math
import time

# ---------------------------------------------
# Heurística: distancia Manhattan
# ---------------------------------------------
def heuristic(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


# ---------------------------------------------
# Costo del terreno (solo se usa para evitar obstáculos)
# ---------------------------------------------
def terrain_cost(matrix, pos):
    value = matrix[pos[0]][pos[1]]
    if value == 1:
        return math.inf  # obstáculo
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
            if matrix[nx][ny] != 1:  # no obstáculo
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
# Algoritmo Avara (Greedy Best-First Search)
# ---------------------------------------------
def greedy_best_first_search(matrix, start, goal):
    start_time = time.time()

    open_list = []
    heappush(open_list, (0, start))
    came_from = {}
    visited = set()
    expanded_nodes = 0

    while open_list:
        _, current = heappop(open_list)
        expanded_nodes += 1

        if current == goal:
            elapsed = time.time() - start_time
            path = reconstruct_path(came_from, start, goal)
            return {
                "path": path,
                "cost": len(path),
                "expanded_nodes": expanded_nodes,
                "depth": len(path),
                "time": elapsed
            }

        visited.add(current)

        for neighbor in get_neighbors(matrix, current):
            if neighbor not in visited:
                came_from[neighbor] = current
                priority = heuristic(neighbor, goal)
                heappush(open_list, (priority, neighbor))

    return None  # si no encuentra camino