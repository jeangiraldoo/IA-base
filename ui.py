import pygame
import time
import sys
from algoritmo_avara import greedy_best_first_search
from algoritmo_a_estrella import a_star
from profundidad_evitando_ciclos import ejecutar_profundidad_animada
from amplitud import ejecutar_amplitud_desde_matriz


from world_loader import build_map_from_matrix, build_matrix_from_txt_file
# from ui import ui_loop

matrix = build_matrix_from_txt_file()
print(matrix)
game_map = build_map_from_matrix(matrix)
print(game_map)
# ui_loop(game_map)
info_data = {"algorithm_name": "", "cost": ""}
drawn_steps = []

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
    print("Drawing map")
    cell_width = area.width // grid_size
    cell_height = area.height // grid_size

    for row_number in range(len(map)):
        row = map[row_number]
        for col_number in range(len(row)):
            image = row[col_number]
            
            image = pygame.transform.scale(image, (cell_width, cell_height))
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


def draw_steps(steps):
    global drawn_steps
    drawn_steps = steps


def find_positions(matrix, start_value=2, goal_value=6):
    print("Find positions")
    print(matrix)
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
    Button(
        (BUTTON_WIDTH * 2, 0, BUTTON_WIDTH, BUTTON_HEIGHT),
        COLOURS["LIGHT_GRAY"],
        "Regresar",
        lambda: set_buttons(ALGORITHM_TYPE_BUTTONS),
    ),
]

current_buttons = []


def set_buttons(new_buttons):
    global current_buttons
    current_buttons = new_buttons


def on_depth_click(matrix):
    global info_data
    print("Ejecutando algoritmo profundidad...")
    start, goal = find_positions(matrix)

    if not start or not goal:
        print("❌ No se encontraron posiciones de inicio o meta en el mapa.")
        return

    resultado = ejecutar_profundidad_animada(matrix)
    if not resultado:
        print("⚠️ No se encontró un camino.")
        return

    print("🔹 Resultado Avara:", resultado)
    draw_steps(resultado["paths"])
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
                lambda: reset_to_main_menu(),
            ),
        ]
    )


def on_avara_click(matrix):
    global info_data
    print("Ejecutando algoritmo Avara...")
    start, goal = find_positions(matrix)

    if not start or not goal:
        print("❌ No se encontraron posiciones de inicio o meta en el mapa.")
        return

    resultado = greedy_best_first_search(matrix, start, goal)
    if not resultado:
        print("⚠️ No se encontró un camino.")
        return

    print("🔹 Resultado Avara:", resultado)
    draw_steps(resultado["paths"])
    info_data = resultado


def on_a_estrella_click(matrix):
    global info_data
    print("Ejecutando algoritmo A*...")
    start, goal = find_positions(matrix)

    if not start or not goal:
        print("❌ No se encontraron posiciones de inicio o meta en el mapa.")
        return

    resultado = a_star(matrix, start, goal)
    if not resultado:
        print("⚠️ No se encontró un camino.")
        return

    print("🔹 Resultado A*:", resultado)
    draw_steps(resultado["paths"])
    info_data = resultado


def reset_to_main_menu():
    global drawn_steps, info_data
    drawn_steps = []
    info_data = {}
    set_buttons(ALGORITHM_TYPE_BUTTONS)


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
                lambda: reset_to_main_menu(),
            ),
        ]
    )


set_buttons(ALGORITHM_TYPE_BUTTONS)  # For the informed/uninformed buttons


def draw_cell(row, col, cell_width, cell_height):
    x = MAP_AREA.left + col * cell_width
    y = MAP_AREA.top + row * cell_height
    rect = pygame.Rect(x, y, cell_width, cell_height)
    pygame.draw.rect(screen, COLOURS["CYAN"], rect)

    pygame.display.update(rect)
    pygame.time.delay(100)


def draw_algorithm_path():
    cell_width = MAP_AREA.width // MAP_SIZE
    cell_height = MAP_AREA.height // MAP_SIZE
    if isinstance(drawn_steps[0], list):
        for l in drawn_steps:
            for row, col in l:
                draw_cell(row, col, cell_width, cell_height)
    elif isinstance(drawn_steps[0], tuple):
        for row, col in drawn_steps:
            draw_cell(row, col, cell_width, cell_height)


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

        if drawn_steps:
            draw_algorithm_path()

        draw_sidepanel(info_data)
        pygame.display.flip()
        clock.tick(60)


ui_loop(game_map)
