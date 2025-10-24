import pygame
import sys
from algoritmo_avara import greedy_best_first_search
from algoritmo_a_estrella import a_star
from profundidad_evitando_ciclos import ejecutar_profundidad_animada

from world_loader import build_map_from_matrix, build_matrix_from_txt_file
# from ui import ui_loop

matrix = build_matrix_from_txt_file()
print(matrix)
game_map = build_map_from_matrix(matrix)
print(game_map)
# ui_loop(game_map)
info_data = {"algorithm_name": "", "cost": ""}

GAME_NAME = "Smart Astronaut"
WIDTH, HEIGHT = 1000, 600
MAP_SIZE = 10
GRID_MARGIN = 1
BG_COLOR = (255, 255, 255)

COLOURS = {
    "RED": (255, 0, 0),
    "YELLOW": (255, 255, 0),
    "CYAN": (0, 200, 255),
    "GREEN": (0, 255, 0),
    "MAGENTA": (255, 0, 255),
    "LIGHT_GRAY": (220, 220, 220),
    "ORANGE": (255, 165, 0),
    "BLACK": (0, 0, 0),
}

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption(GAME_NAME)
font = pygame.font.SysFont(None, 28)

TOP_BAR_HEIGHT = 60
RIGHT_PANEL_WIDTH = 200

MAP_AREA = pygame.Rect(
    0, TOP_BAR_HEIGHT, WIDTH - RIGHT_PANEL_WIDTH, HEIGHT - TOP_BAR_HEIGHT
)

SIDEPANEL_RECTS = {
    "SUMMARY": pygame.Rect(
        WIDTH - RIGHT_PANEL_WIDTH, TOP_BAR_HEIGHT, RIGHT_PANEL_WIDTH, 150
    ),
    "INFO": pygame.Rect(
        WIDTH - RIGHT_PANEL_WIDTH, TOP_BAR_HEIGHT + 150, RIGHT_PANEL_WIDTH, 250
    ),
    "EXTRA": pygame.Rect(
        WIDTH - RIGHT_PANEL_WIDTH,
        TOP_BAR_HEIGHT + 400,
        RIGHT_PANEL_WIDTH,
        HEIGHT - (TOP_BAR_HEIGHT + 400),
    ),
}


class Button:
    def __init__(self, rect, color, text, on_click):
        self.rect = pygame.Rect(rect)
        self.color = color
        self.text = text
        self.on_click = on_click

    def draw(self, surface, font, COLOURS):
        pygame.draw.rect(surface, self.color, self.rect)
        label = font.render(self.text, True, COLOURS["BLACK"])
        surface.blit(label, (self.rect.x + 15, self.rect.y + 15))

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                self.on_click()


def draw_map(surface, area, grid_size, map):
    cell_width = area.width // grid_size
    cell_height = area.height // grid_size

    for row_number in range(len(map)):
        row = map[row_number]
        for col_number in range(len(row)):
            image = row[col_number]
            x_position = area.left + (col_number * cell_width)
            y_position = area.top + (row_number * cell_height)
            rect = pygame.Rect(x_position, y_position, cell_width, cell_height)
            surface.blit(image, rect)


def draw_sidepanel(info_data):
    summary_panel = SIDEPANEL_RECTS["SUMMARY"]
    info_panel = SIDEPANEL_RECTS["INFO"]
    extra_panel = SIDEPANEL_RECTS["EXTRA"]

    pygame.draw.rect(screen, COLOURS["MAGENTA"], summary_panel)
    pygame.draw.rect(screen, COLOURS["LIGHT_GRAY"], info_panel)
    pygame.draw.rect(screen, COLOURS["ORANGE"], extra_panel)

    screen.blit(
        font.render("Resumen", True, COLOURS["BLACK"]),
        (summary_panel.x + 20, summary_panel.y + 20),
    )
    screen.blit(
        font.render("Configuración", True, COLOURS["BLACK"]),
        (summary_panel.x + 20, summary_panel.y + 50),
    )
    screen.blit(
        font.render("Info", True, COLOURS["BLACK"]),
        (info_panel.x + 20, info_panel.y + 20),
    )
    screen.blit(
        font.render("Extra: Animación", True, COLOURS["BLACK"]),
        (extra_panel.x + 20, extra_panel.y + 20),
    )

    if not info_data:
        return

    y_pos = info_panel.y + 60
    print(info_data)
    spanish_keys = {
        "algorithm_name": "Algoritmo",
        "cost": "Costo",
        "path": "Camino",
        "paths": "Caminos",
        "expanded_nodes": "Nodos expandidos",
        "time": "Tiempo",
        "depth": "Profundidad",
        "samples": "Muestras",
    }

    for key, value in info_data.items():
        text = f"{spanish_keys[key]}: {value}"
        screen.blit(
            font.render(text, True, COLOURS["BLACK"]), (info_panel.x + 20, y_pos)
        )
        y_pos += 30


def find_positions(matrix, start_value=2, goal_value=6):
    start = None
    goals = []

    for i in range(len(matrix)):
        for j in range(len(matrix[0])):
            if matrix[i][j] == start_value:
                start = (i, j)
            elif matrix[i][j] == goal_value:
                goals.append((i, j))

    return start, goals


BUTTON_HEIGHT = TOP_BAR_HEIGHT
BUTTON_WIDTH = 150


ALGORITHM_TYPE_BUTTONS = [
    Button(
        (0, 0, BUTTON_WIDTH, BUTTON_HEIGHT),
        COLOURS["RED"],
        "No informada",
        lambda: show_uninformed_buttons(),
    ),
    Button(
        (BUTTON_WIDTH, 0, BUTTON_WIDTH, BUTTON_HEIGHT),
        COLOURS["YELLOW"],
        "Informada",
        lambda: show_informed_buttons(matrix),
    ),
]

current_buttons = []


def set_buttons(new_buttons):
    global current_buttons
    current_buttons = new_buttons


def on_depth_click(matrix):
    global info_data
    print("Ejecutando algoritmo profundidad...")
    # reset_map_visual()
    start, goal = find_positions(matrix)

    if not start or not goal:
        print("❌ No se encontraron posiciones de inicio o meta en el mapa.")
        return

    resultado = ejecutar_profundidad_animada(screen, matrix)
    if not resultado:
        print("⚠️ No se encontró un camino.")
        return

    print("🔹 Resultado Avara:", resultado)
    # paint_path_on_map(map_visual, resultado["path"])
    info_data = resultado


def show_uninformed_buttons():
    set_buttons(
        [
            Button(
                (0, 0, BUTTON_WIDTH, BUTTON_HEIGHT),
                COLOURS["GREEN"],
                "Amplitud",
                lambda: print("Amplitud"),
            ),
            Button(
                (BUTTON_WIDTH, 0, BUTTON_WIDTH, BUTTON_HEIGHT),
                COLOURS["CYAN"],
                "Profundidad",
                lambda: on_depth_click(matrix),
            ),
            Button(
                (BUTTON_WIDTH * 2, 0, BUTTON_WIDTH, BUTTON_HEIGHT),
                COLOURS["MAGENTA"],
                "C. uniforme",
                lambda: print("Costo uniforme"),
            ),
            Button(
                (BUTTON_WIDTH * 3, 0, BUTTON_WIDTH, BUTTON_HEIGHT),
                COLOURS["LIGHT_GRAY"],
                "Regresar",
                lambda: set_buttons(ALGORITHM_TYPE_BUTTONS),
            ),
        ]
    )


def on_avara_click(matrix):
    global info_data
    print("Ejecutando algoritmo Avara...")
    # reset_map_visual()
    start, goal = find_positions(matrix)

    if not start or not goal:
        print("❌ No se encontraron posiciones de inicio o meta en el mapa.")
        return

    resultado = greedy_best_first_search(matrix, start, goal)
    if not resultado:
        print("⚠️ No se encontró un camino.")
        return

    print("🔹 Resultado Avara:", resultado)
    # paint_path_on_map(map_visual, resultado["path"])
    info_data = resultado


def on_a_estrella_click(matrix):
    global info_data
    print("Ejecutando algoritmo A*...")
    # reset_map_visual()
    start, goal = find_positions(matrix)

    if not start or not goal:
        print("❌ No se encontraron posiciones de inicio o meta en el mapa.")
        return

    resultado = a_star(matrix, start, goal)
    if not resultado:
        print("⚠️ No se encontró un camino.")
        return

    print("🔹 Resultado A*:", resultado)
    # paint_path_on_map(map_visual, resultado["path"])
    info_data = resultado


def show_informed_buttons(matrix):
    set_buttons(
        [
            Button(
                (0, 0, BUTTON_WIDTH, BUTTON_HEIGHT),
                COLOURS["GREEN"],
                "Avara",
                lambda: on_avara_click(matrix),
            ),
            Button(
                (BUTTON_WIDTH, 0, BUTTON_WIDTH, BUTTON_HEIGHT),
                COLOURS["CYAN"],
                "A*",
                lambda: on_a_estrella_click(matrix),
            ),
            Button(
                (BUTTON_WIDTH * 2, 0, BUTTON_WIDTH, BUTTON_HEIGHT),
                COLOURS["MAGENTA"],
                "Regresar",
                lambda: set_buttons(ALGORITHM_TYPE_BUTTONS),
            ),
        ]
    )


set_buttons(ALGORITHM_TYPE_BUTTONS)  # For the informed/uninformed buttons


def ui_loop(map):
    clock = pygame.time.Clock()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            for button in current_buttons:
                button.handle_event(event)

        screen.fill(BG_COLOR)

        for button in current_buttons:
            button.draw(screen, font, COLOURS)

        draw_map(screen, MAP_AREA, MAP_SIZE, map)
        draw_sidepanel(info_data)

        pygame.display.flip()
        clock.tick(60)


ui_loop(game_map)


# import pygame
# import sys
# from algoritmo_a_estrella import a_star
# from algoritmo_avara import greedy_best_first_search
#
# # ---------------------------------------------
# # CONFIGURACIÓN DE LA INTERFAZ
# # ---------------------------------------------
# GAME_NAME = "Smart Astronaut"
# WIDTH, HEIGHT = 1000, 600
# MAP_SIZE = 10
# GRID_MARGIN = 1
# BG_COLOR = (255, 255, 255)
#
# COLOURS = {
#     "RED": (255, 0, 0),         # Astronauta
#     "YELLOW": (255, 255, 0),    # Rocoso
#     "CYAN": (0, 200, 255),      # Camino
#     "GREEN": (0, 255, 0),       # Meta
#     "MAGENTA": (255, 0, 255),   # Nave
#     "LIGHT_GRAY": (220, 220, 220),  # Libre
#     "ORANGE": (255, 165, 0),    # Volcánico
#     "BLACK": (0, 0, 0),         # Obstáculo
#     "WHITE": (255, 255, 255),
# }
#
# pygame.init()
# screen = pygame.display.set_mode((WIDTH, HEIGHT))
# pygame.display.set_caption(GAME_NAME)
# font = pygame.font.SysFont(None, 28)
#
# TOP_BAR_HEIGHT = 60
# RIGHT_PANEL_WIDTH = 200
#
# MAP_AREA = pygame.Rect(
#     0, TOP_BAR_HEIGHT, WIDTH - RIGHT_PANEL_WIDTH, HEIGHT - TOP_BAR_HEIGHT
# )
#
# SIDEPANEL_RECTS = {
#     "SUMMARY": pygame.Rect(WIDTH - RIGHT_PANEL_WIDTH, TOP_BAR_HEIGHT, RIGHT_PANEL_WIDTH, 150),
#     "INFO": pygame.Rect(WIDTH - RIGHT_PANEL_WIDTH, TOP_BAR_HEIGHT + 150, RIGHT_PANEL_WIDTH, 250),
#     "EXTRA": pygame.Rect(WIDTH - RIGHT_PANEL_WIDTH, TOP_BAR_HEIGHT + 400, RIGHT_PANEL_WIDTH, HEIGHT - (TOP_BAR_HEIGHT + 400)),
# }
#
# # ---------------------------------------------
# # CLASE BOTÓN
# # ---------------------------------------------
# class Button:
#     def __init__(self, rect, color, text, on_click):
#         self.rect = pygame.Rect(rect)
#         self.color = color
#         self.text = text
#         self.on_click = on_click
#
#     def draw(self, surface, font, COLOURS):
#         pygame.draw.rect(surface, self.color, self.rect)
#         label = font.render(self.text, True, COLOURS["BLACK"])
#         surface.blit(label, (self.rect.x + 15, self.rect.y + 15))
#
#     def handle_event(self, event):
#         if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
#             if self.rect.collidepoint(event.pos):
#                 self.on_click()
#
#
# # ---------------------------------------------
# # FUNCIONES DE DIBUJO
# # ---------------------------------------------
# def draw_map(surface, area, grid_size, map):
#     cell_width = area.width // grid_size
#     cell_height = area.height // grid_size
#
#     for row_number in range(len(map)):
#         row = map[row_number]
#         for col_number in range(len(row)):
#             image = row[col_number]
#             x_position = area.left + (col_number * cell_width)
#             y_position = area.top + (row_number * cell_height)
#             rect = pygame.Rect(x_position, y_position, cell_width, cell_height)
#             surface.blit(image, rect)
#
#
# def draw_sidepanel(info_data):
#     summary_panel = SIDEPANEL_RECTS["SUMMARY"]
#     info_panel = SIDEPANEL_RECTS["INFO"]
#     extra_panel = SIDEPANEL_RECTS["EXTRA"]
#
#     pygame.draw.rect(screen, COLOURS["MAGENTA"], summary_panel)
#     pygame.draw.rect(screen, COLOURS["LIGHT_GRAY"], info_panel)
#     pygame.draw.rect(screen, COLOURS["ORANGE"], extra_panel)
#
#     # Textos principales
#     screen.blit(font.render("Resumen", True, COLOURS["BLACK"]), (summary_panel.x + 20, summary_panel.y + 20))
#     screen.blit(font.render("Configuración", True, COLOURS["BLACK"]), (summary_panel.x + 20, summary_panel.y + 50))
#     screen.blit(font.render("Info", True, COLOURS["BLACK"]), (info_panel.x + 20, info_panel.y + 20))
#     screen.blit(font.render("Extra: Animación", True, COLOURS["BLACK"]), (extra_panel.x + 20, extra_panel.y + 20))
#
#     # Mostrar los datos del algoritmo
#     if info_data:
#         y_pos = info_panel.y + 60
#         for key, value in info_data.items():
#             text = f"{key.capitalize()}: {value}"
#             screen.blit(font.render(text, True, COLOURS["BLACK"]), (info_panel.x + 20, y_pos))
#             y_pos += 30
#
#
# # ---------------------------------------------
# # BOTONES PRINCIPALES
# # ---------------------------------------------
# BUTTON_HEIGHT = TOP_BAR_HEIGHT
# BUTTON_WIDTH = 150
#
# def on_uninformed_search_click():
#     show_uninformed_buttons()
#
# def on_informed_search_click():
#     show_informed_buttons()
#
# ALGORITHM_TYPE_BUTTONS = [
#     Button((0, 0, BUTTON_WIDTH, BUTTON_HEIGHT), COLOURS["RED"], "No informada", on_uninformed_search_click),
#     Button((BUTTON_WIDTH, 0, BUTTON_WIDTH, BUTTON_HEIGHT), COLOURS["YELLOW"], "Informada", on_informed_search_click),
# ]
#
# current_buttons = []
# info_data = {}
#
# def set_buttons(new_buttons):
#     global current_buttons
#     current_buttons = new_buttons
#
# def show_main_buttons():
#     set_buttons(ALGORITHM_TYPE_BUTTONS)
#
# def show_uninformed_buttons():
#     set_buttons([
#         Button((0, 0, BUTTON_WIDTH, BUTTON_HEIGHT), COLOURS["GREEN"], "Amplitud", lambda: print("Amplitud")),
#         Button((BUTTON_WIDTH, 0, BUTTON_WIDTH, BUTTON_HEIGHT), COLOURS["CYAN"], "Profundidad", lambda: print("Profundidad")),
#         Button((BUTTON_WIDTH * 2, 0, BUTTON_WIDTH, BUTTON_HEIGHT), COLOURS["MAGENTA"], "C. uniforme", lambda: print("Costo uniforme")),
#         Button((BUTTON_WIDTH * 3, 0, BUTTON_WIDTH, BUTTON_HEIGHT), COLOURS["LIGHT_GRAY"], "Regresar", show_main_buttons),
#     ])
#
# # ---------------------------------------------
# # FUNCIONES DE APOYO
# # ---------------------------------------------
# def find_positions(matrix, start_value=2, goal_value=6):
#     start = None
#     goal = None
#     for i in range(len(matrix)):
#         for j in range(len(matrix[0])):
#             if matrix[i][j] == start_value:
#                 start = (i, j)
#             elif matrix[i][j] == goal_value:
#                 goal = (i, j)
#     return start, goal
#
#
# def paint_path_on_map(matrix_visual, path):
#     for pos in path:
#         x, y = pos
#         matrix_visual[x][y].fill(COLOURS["CYAN"])  # pinta el camino de azul celeste
#
#
# def reset_map_visual():
#     """Restaura los colores originales del mapa antes de ejecutar otro algoritmo."""
#     cell_width = (WIDTH - RIGHT_PANEL_WIDTH) // MAP_SIZE
#     cell_height = (HEIGHT - TOP_BAR_HEIGHT) // MAP_SIZE
#
#     for i in range(len(matrix_real)):
#         for j in range(len(matrix_real[0])):
#             value = matrix_real[i][j]
#             surface = pygame.Surface((cell_width, cell_height))
#             if value == 0:
#                 surface.fill(COLOURS["LIGHT_GRAY"])
#             elif value == 1:
#                 surface.fill(COLOURS["BLACK"])
#             elif value == 2:
#                 surface.fill(COLOURS["RED"])
#             elif value == 3:
#                 surface.fill(COLOURS["YELLOW"])
#             elif value == 4:
#                 surface.fill(COLOURS["ORANGE"])
#             elif value == 5:
#                 surface.fill(COLOURS["MAGENTA"])
#             elif value == 6:
#                 surface.fill(COLOURS["GREEN"])
#             map_visual[i][j] = surface
#
#
# # ---------------------------------------------
# # FUNCIONES DE LOS BOTONES INFORMADOS
# # ---------------------------------------------
# def on_avara_click():
#     global info_data
#     print("Ejecutando algoritmo Avara...")
#     reset_map_visual()
#     start, goal = find_positions(matrix_real)
#
#     if not start or not goal:
#         print("❌ No se encontraron posiciones de inicio o meta en el mapa.")
#         return
#
#     resultado = greedy_best_first_search(matrix_real, start, goal)
#     if resultado:
#         print("🔹 Resultado Avara:", resultado)
#         paint_path_on_map(map_visual, resultado["path"])
#         info_data = {
#             "Algoritmo": "Avara",
#             "Costo": resultado["cost"],
#             "Profundidad": resultado["depth"],
#             "Nodos": resultado["expanded_nodes"],
#             "Tiempo": round(resultado["time"], 4),
#         }
#     else:
#         print("⚠️ No se encontró un camino.")
#
#
# def on_a_estrella_click():
#     global info_data
#     print("Ejecutando algoritmo A*...")
#     reset_map_visual()
#     start, goal = find_positions(matrix_real)
#
#     if not start or not goal:
#         print("❌ No se encontraron posiciones de inicio o meta en el mapa.")
#         return
#
#     resultado = a_star(matrix_real, start, goal)
#     if resultado:
#         print("🔹 Resultado A*:", resultado)
#         paint_path_on_map(map_visual, resultado["path"])
#         info_data = {
#             "Algoritmo": "A*",
#             "Costo": resultado["cost"],
#             "Profundidad": resultado["depth"],
#             "Nodos": resultado["expanded_nodes"],
#             "Tiempo": round(resultado["time"], 4),
#         }
#     else:
#         print("⚠️ No se encontró un camino.")
#
#
# def show_informed_buttons():
#     set_buttons([
#         Button((0, 0, BUTTON_WIDTH, BUTTON_HEIGHT), COLOURS["GREEN"], "Avara", on_avara_click),
#         Button((BUTTON_WIDTH, 0, BUTTON_WIDTH, BUTTON_HEIGHT), COLOURS["CYAN"], "A*", on_a_estrella_click),
#         Button((BUTTON_WIDTH * 2, 0, BUTTON_WIDTH, BUTTON_HEIGHT), COLOURS["MAGENTA"], "Regresar", show_main_buttons),
#     ])
#
#
# # ---------------------------------------------
# # CARGAR MAPA DESDE ARCHIVO
# # ---------------------------------------------
# def build_matrix_from_txt_file(filename="Prueba1.txt"):
#     with open(filename, "r") as file:
#         file_lines = file.readlines()
#
#     matrix = []
#     for line in file_lines:
#         stripped_line = line.strip().replace(" ", "")
#         new_row = [int(x) for x in stripped_line]
#         matrix.append(new_row)
#     return matrix
#
#
# # ---------------------------------------------
# # BUCLE PRINCIPAL
# # ---------------------------------------------
# def ui_loop(map):
#     clock = pygame.time.Clock()
#
#     while True:
#         for event in pygame.event.get():
#             if event.type == pygame.QUIT:
#                 pygame.quit()
#                 sys.exit()
#
#             for button in current_buttons:
#                 button.handle_event(event)
#
#         screen.fill(BG_COLOR)
#
#         for button in current_buttons:
#             button.draw(screen, font, COLOURS)
#
#         draw_map(screen, MAP_AREA, MAP_SIZE, map)
#         draw_sidepanel(info_data)
#
#         pygame.display.flip()
#         clock.tick(60)
#
#
# # ---------------------------------------------
# # EJECUCIÓN PRINCIPAL
# # ---------------------------------------------
# if __name__ == "__main__":
#     matrix_real = build_matrix_from_txt_file("Prueba1.txt")
#
#     cell_width = (WIDTH - RIGHT_PANEL_WIDTH) // MAP_SIZE
#     cell_height = (HEIGHT - TOP_BAR_HEIGHT) // MAP_SIZE
#
#     map_visual = []
#     for row in matrix_real:
#         visual_row = []
#         for value in row:
#             surface = pygame.Surface((cell_width, cell_height))
#             if value == 0:
#                 surface.fill(COLOURS["LIGHT_GRAY"])
#             elif value == 1:
#                 surface.fill(COLOURS["BLACK"])
#             elif value == 2:
#                 surface.fill(COLOURS["RED"])
#             elif value == 3:
#                 surface.fill(COLOURS["YELLOW"])
#             elif value == 4:
#                 surface.fill(COLOURS["ORANGE"])
#             elif value == 5:
#                 surface.fill(COLOURS["MAGENTA"])
#             elif value == 6:
#                 surface.fill(COLOURS["GREEN"])
#             visual_row.append(surface)
#         map_visual.append(visual_row)
#
#     set_buttons(ALGORITHM_TYPE_BUTTONS)
#     info_data = {}
#     ui_loop(map_visual)


# import pygame
# import sys
# import time
# from algoritmo_a_estrella import a_star
# from algoritmo_avara import greedy_best_first_search
#
# # ---------------------------------------------
# # CONFIGURACIÓN DE LA INTERFAZ
# # ---------------------------------------------
# GAME_NAME = "Smart Astronaut"
# WIDTH, HEIGHT = 1000, 600
# MAP_SIZE = 10
# GRID_MARGIN = 1
# BG_COLOR = (255, 255, 255)
#
# COLOURS = {
#     "RED": (255, 0, 0),         # Astronauta
#     "YELLOW": (255, 255, 0),    # Rocoso
#     "CYAN": (0, 200, 255),      # Camino 1
#     "GREEN": (0, 255, 0),       # Meta
#     "MAGENTA": (255, 0, 255),   # Nave
#     "LIGHT_GRAY": (220, 220, 220),  # Libre
#     "ORANGE": (255, 165, 0),    # Volcánico
#     "BLACK": (0, 0, 0),         # Obstáculo
#     "WHITE": (255, 255, 255),
#     "BLUE": (0, 0, 255),        # Camino 2
#     "PINK": (255, 105, 180),    # Camino 3
# }
#
# pygame.init()
# screen = pygame.display.set_mode((WIDTH, HEIGHT))
# pygame.display.set_caption(GAME_NAME)
# font = pygame.font.SysFont(None, 28)
#
# TOP_BAR_HEIGHT = 60
# RIGHT_PANEL_WIDTH = 200
#
# MAP_AREA = pygame.Rect(
#     0, TOP_BAR_HEIGHT, WIDTH - RIGHT_PANEL_WIDTH, HEIGHT - TOP_BAR_HEIGHT
# )
#
# SIDEPANEL_RECTS = {
#     "SUMMARY": pygame.Rect(WIDTH - RIGHT_PANEL_WIDTH, TOP_BAR_HEIGHT, RIGHT_PANEL_WIDTH, 150),
#     "INFO": pygame.Rect(WIDTH - RIGHT_PANEL_WIDTH, TOP_BAR_HEIGHT + 150, RIGHT_PANEL_WIDTH, 250),
#     "EXTRA": pygame.Rect(WIDTH - RIGHT_PANEL_WIDTH, TOP_BAR_HEIGHT + 400, RIGHT_PANEL_WIDTH, HEIGHT - (TOP_BAR_HEIGHT + 400)),
# }
#
# # ---------------------------------------------
# # CLASE BOTÓN
# # ---------------------------------------------
# class Button:
#     def __init__(self, rect, color, text, on_click):
#         self.rect = pygame.Rect(rect)
#         self.color = color
#         self.text = text
#         self.on_click = on_click
#
#     def draw(self, surface, font, COLOURS):
#         pygame.draw.rect(surface, self.color, self.rect)
#         label = font.render(self.text, True, COLOURS["BLACK"])
#         surface.blit(label, (self.rect.x + 15, self.rect.y + 15))
#
#     def handle_event(self, event):
#         if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
#             if self.rect.collidepoint(event.pos):
#                 self.on_click()
#
#
# # ---------------------------------------------
# # FUNCIONES DE DIBUJO
# # ---------------------------------------------
# def draw_map(surface, area, grid_size, map):
#     cell_width = area.width // grid_size
#     cell_height = area.height // grid_size
#
#     for row_number in range(len(map)):
#         row = map[row_number]
#         for col_number in range(len(row)):
#             image = row[col_number]
#             x_position = area.left + (col_number * cell_width)
#             y_position = area.top + (row_number * cell_height)
#             rect = pygame.Rect(x_position, y_position, cell_width, cell_height)
#             surface.blit(image, rect)
#
#
# def draw_sidepanel(info_data):
#     summary_panel = SIDEPANEL_RECTS["SUMMARY"]
#     info_panel = SIDEPANEL_RECTS["INFO"]
#     extra_panel = SIDEPANEL_RECTS["EXTRA"]
#
#     pygame.draw.rect(screen, COLOURS["MAGENTA"], summary_panel)
#     pygame.draw.rect(screen, COLOURS["LIGHT_GRAY"], info_panel)
#     pygame.draw.rect(screen, COLOURS["ORANGE"], extra_panel)
#
#     screen.blit(font.render("Resumen", True, COLOURS["BLACK"]), (summary_panel.x + 20, summary_panel.y + 20))
#     screen.blit(font.render("Configuración", True, COLOURS["BLACK"]), (summary_panel.x + 20, summary_panel.y + 50))
#     screen.blit(font.render("Info", True, COLOURS["BLACK"]), (info_panel.x + 20, info_panel.y + 20))
#     screen.blit(font.render("Extra: Animación", True, COLOURS["BLACK"]), (extra_panel.x + 20, extra_panel.y + 20))
#
#     if info_data:
#         y_pos = info_panel.y + 60
#         for key, value in info_data.items():
#             text = f"{key.capitalize()}: {value}"
#             screen.blit(font.render(text, True, COLOURS["BLACK"]), (info_panel.x + 20, y_pos))
#             y_pos += 30
#
#
# # ---------------------------------------------
# # BOTONES
# # ---------------------------------------------
# BUTTON_HEIGHT = TOP_BAR_HEIGHT
# BUTTON_WIDTH = 150
#
# def on_uninformed_search_click():
#     show_uninformed_buttons()
#
# def on_informed_search_click():
#     show_informed_buttons()
#
# ALGORITHM_TYPE_BUTTONS = [
#     Button((0, 0, BUTTON_WIDTH, BUTTON_HEIGHT), COLOURS["RED"], "No informada", on_uninformed_search_click),
#     Button((BUTTON_WIDTH, 0, BUTTON_WIDTH, BUTTON_HEIGHT), COLOURS["YELLOW"], "Informada", on_informed_search_click),
# ]
#
# current_buttons = []
# info_data = {}
# sim_paths = []
#
# def set_buttons(new_buttons):
#     global current_buttons
#     current_buttons = new_buttons
#
# def show_main_buttons():
#     set_buttons(ALGORITHM_TYPE_BUTTONS)
#
#
# def show_uninformed_buttons():
#     set_buttons([
#         Button((0, 0, BUTTON_WIDTH, BUTTON_HEIGHT), COLOURS["GREEN"], "Amplitud", lambda: print("Amplitud")),
#         Button((BUTTON_WIDTH, 0, BUTTON_WIDTH, BUTTON_HEIGHT), COLOURS["CYAN"], "Profundidad", lambda: print("Profundidad")),
#         Button((BUTTON_WIDTH * 2, 0, BUTTON_WIDTH, BUTTON_HEIGHT), COLOURS["MAGENTA"], "C. uniforme", lambda: print("Costo uniforme")),
#         Button((BUTTON_WIDTH * 3, 0, BUTTON_WIDTH, BUTTON_HEIGHT), COLOURS["LIGHT_GRAY"], "Regresar", show_main_buttons),
#     ])
#
#
# # ---------------------------------------------
# # FUNCIONES DE APOYO
# # ---------------------------------------------
# def find_positions(matrix, start_value=2, goal_value=6):
#     start = None
#     goals = []
#     for i in range(len(matrix)):
#         for j in range(len(matrix[0])):
#             if matrix[i][j] == start_value:
#                 start = (i, j)
#             elif matrix[i][j] == goal_value:
#                 goals.append((i, j))
#     return start, goals
#
#
# def paint_paths_on_map(matrix_visual, paths):
#     colors = [COLOURS["CYAN"], COLOURS["BLUE"], COLOURS["PINK"]]
#     for i, path in enumerate(paths):
#         for x, y in path:
#             matrix_visual[x][y].fill(colors[i % len(colors)])
#
#
# def reset_map_visual():
#     cell_width = (WIDTH - RIGHT_PANEL_WIDTH) // MAP_SIZE
#     cell_height = (HEIGHT - TOP_BAR_HEIGHT) // MAP_SIZE
#
#     for i in range(len(matrix_real)):
#         for j in range(len(matrix_real[0])):
#             value = matrix_real[i][j]
#             surface = pygame.Surface((cell_width, cell_height))
#             if value == 0:
#                 surface.fill(COLOURS["LIGHT_GRAY"])
#             elif value == 1:
#                 surface.fill(COLOURS["BLACK"])
#             elif value == 2:
#                 surface.fill(COLOURS["RED"])
#             elif value == 3:
#                 surface.fill(COLOURS["YELLOW"])
#             elif value == 4:
#                 surface.fill(COLOURS["ORANGE"])
#             elif value == 5:
#                 surface.fill(COLOURS["MAGENTA"])
#             elif value == 6:
#                 surface.fill(COLOURS["GREEN"])
#             map_visual[i][j] = surface
#
#
# # ---------------------------------------------
# # BOTONES DE LOS ALGORITMOS
# # ---------------------------------------------
# def on_a_estrella_click():
#     global info_data, sim_paths
#     reset_map_visual()
#     start, goals = find_positions(matrix_real)
#     resultado = a_star(matrix_real, start, goals)
#     if resultado:
#         paint_paths_on_map(map_visual, resultado["paths"])
#         sim_paths = resultado["paths"]
#         info_data = {
#             "Algoritmo": "A*",
#             "Costo total": resultado["cost"],
#             "Profundidad": resultado["depth"],
#             "Nodos": resultado["expanded_nodes"],
#             "Tiempo": round(resultado["time"], 4),
#         }
#         add_simulate_button()
#     else:
#         print("⚠️ No se encontró un camino.")
#
#
# def on_avara_click():
#     global info_data, sim_paths
#     reset_map_visual()
#     start, goals = find_positions(matrix_real)
#     resultado = greedy_best_first_search(matrix_real, start, goals)
#     if resultado:
#         paint_paths_on_map(map_visual, resultado["paths"])
#         sim_paths = resultado["paths"]
#         info_data = {
#             "Algoritmo": "Avara",
#             "Costo total": resultado["cost"],
#             "Profundidad": resultado["depth"],
#             "Nodos": resultado["expanded_nodes"],
#             "Tiempo": round(resultado["time"], 4),
#         }
#         add_simulate_button()
#     else:
#         print("⚠️ No se encontró un camino.")
#
#
# def simulate_path():
#     reset_map_visual()
#     cell_width = (WIDTH - RIGHT_PANEL_WIDTH) // MAP_SIZE
#     cell_height = (HEIGHT - TOP_BAR_HEIGHT) // MAP_SIZE
#
#     for path in sim_paths:
#         for (x, y) in path:
#             map_visual[x][y].fill(COLOURS["CYAN"])
#             draw_map(screen, MAP_AREA, MAP_SIZE, map_visual)
#             draw_sidepanel(info_data)
#             pygame.display.flip()
#             time.sleep(0.1)
#
#
# def add_simulate_button():
#     current_buttons.append(
#         Button((BUTTON_WIDTH * 3, 0, BUTTON_WIDTH, BUTTON_HEIGHT), COLOURS["YELLOW"], "Simular", simulate_path)
#     )
#
#
# def show_informed_buttons():
#     set_buttons([
#         Button((0, 0, BUTTON_WIDTH, BUTTON_HEIGHT), COLOURS["GREEN"], "Avara", on_avara_click),
#         Button((BUTTON_WIDTH, 0, BUTTON_WIDTH, BUTTON_HEIGHT), COLOURS["CYAN"], "A*", on_a_estrella_click),
#         Button((BUTTON_WIDTH * 2, 0, BUTTON_WIDTH, BUTTON_HEIGHT), COLOURS["MAGENTA"], "Regresar", show_main_buttons),
#     ])
#
#
# # ---------------------------------------------
# # CARGAR MAPA
# # ---------------------------------------------
# def build_matrix_from_txt_file(filename="Prueba1.txt"):
#     with open(filename, "r") as file:
#         lines = file.readlines()
#
#     return [[int(x) for x in line.strip().replace(" ", "")] for line in lines]
#
#
# # ---------------------------------------------
# # BUCLE PRINCIPAL
# # ---------------------------------------------
# def ui_loop(map):
#     clock = pygame.time.Clock()
#     while True:
#         for event in pygame.event.get():
#             if event.type == pygame.QUIT:
#                 pygame.quit()
#                 sys.exit()
#
#             for button in current_buttons:
#                 button.handle_event(event)
#
#         screen.fill(BG_COLOR)
#         for button in current_buttons:
#             button.draw(screen, font, COLOURS)
#
#         draw_map(screen, MAP_AREA, MAP_SIZE, map)
#         draw_sidepanel(info_data)
#
#         pygame.display.flip()
#         clock.tick(60)
#
#
# # ---------------------------------------------
# # EJECUCIÓN PRINCIPAL
# # ---------------------------------------------
# if __name__ == "__main__":
#     matrix_real = build_matrix_from_txt_file("Prueba1.txt")
#     cell_width = (WIDTH - RIGHT_PANEL_WIDTH) // MAP_SIZE
#     cell_height = (HEIGHT - TOP_BAR_HEIGHT) // MAP_SIZE
#
#     map_visual = []
#     for row in matrix_real:
#         visual_row = []
#         for value in row:
#             surface = pygame.Surface((cell_width, cell_height))
#             if value == 0:
#                 surface.fill(COLOURS["LIGHT_GRAY"])
#             elif value == 1:
#                 surface.fill(COLOURS["BLACK"])
#             elif value == 2:
#                 surface.fill(COLOURS["RED"])
#             elif value == 3:
#                 surface.fill(COLOURS["YELLOW"])
#             elif value == 4:
#                 surface.fill(COLOURS["ORANGE"])
#             elif value == 5:
#                 surface.fill(COLOURS["MAGENTA"])
#             elif value == 6:
#                 surface.fill(COLOURS["GREEN"])
#             visual_row.append(surface)
#         map_visual.append(visual_row)
#
#     set_buttons(ALGORITHM_TYPE_BUTTONS)
#     info_data = {}
#     ui_loop(map_visual)
