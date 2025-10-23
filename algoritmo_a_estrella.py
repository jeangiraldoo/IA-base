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
    if value == 0 or value == 2 or value == 5 or value == 6:
        return 1
    elif value == 3:
        return 3
    elif value == 4:
        return 5
    elif value == 1:
        return math.inf
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
# Algoritmo A*
# ---------------------------------------------
def a_star(matrix, start, goal):
    start_time = time.time()

    open_list = []
    heappush(open_list, (0, start))
    came_from = {}
    g_score = {start: 0}
    expanded_nodes = 0

    while open_list:
        _, current = heappop(open_list)
        expanded_nodes += 1

        if current == goal:
            elapsed = time.time() - start_time
            path = reconstruct_path(came_from, start, goal)
            return {
                "path": path,
                "cost": g_score[current],
                "expanded_nodes": expanded_nodes,
                "depth": len(path),
                "time": elapsed
            }

        for neighbor in get_neighbors(matrix, current):
            tentative_g = g_score[current] + terrain_cost(matrix, neighbor)

            if neighbor not in g_score or tentative_g < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g
                f_score = tentative_g + heuristic(neighbor, goal)
                heappush(open_list, (f_score, neighbor))

    return None