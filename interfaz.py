import pygame
import sys

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
    """Simple clickable button."""

    def __init__(self, rect, color, text, on_click):
        self.rect = pygame.Rect(rect)
        self.color = color
        self.text = text
        self.on_click = on_click

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)
        label = font.render(self.text, True, COLOURS["BLACK"])
        surface.blit(label, (self.rect.x + 15, self.rect.y + 15))

    def handle_event(self, event):
        """Check if button is clicked and call its callback."""
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                self.on_click()


def draw_map(surface, area, grid_size):
    """Draws a grid map."""
    cell_width = area.width // grid_size
    cell_height = area.height // grid_size

    for row in range(grid_size):
        for col in range(grid_size):
            x_position = area.left + (col * cell_width)
            y_position = area.top + (row * cell_height)
            rect = pygame.Rect(x_position, y_position, cell_width, cell_height)
            pygame.draw.rect(surface, COLOURS["GREEN"], rect, 0)


def draw_sidepanel():
    """Draws the right-hand side panels."""
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


def on_uninformed_search_click():
    print("Uninformed search button was clicked!")


def on_informed_search_click():
    print("Informed searh button was clicked!")


BUTTON_WIDTH = 150
BUTTON_HEIGHT = TOP_BAR_HEIGHT

buttons = [
    Button(
        (0, 0, BUTTON_WIDTH, BUTTON_HEIGHT),
        COLOURS["RED"],
        "No informada",
        on_uninformed_search_click,
    ),
    Button(
        (BUTTON_WIDTH, 0, BUTTON_WIDTH, BUTTON_HEIGHT),
        COLOURS["YELLOW"],
        "Informada",
        on_informed_search_click,
    ),
]


def ui_loop():
    clock = pygame.time.Clock()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            for button in buttons:
                button.handle_event(event)

        screen.fill(BG_COLOR)

        for button in buttons:
            button.draw(screen)

        draw_map(screen, MAP_AREA, MAP_SIZE)
        draw_sidepanel()

        pygame.display.flip()
        clock.tick(60)


ui_loop()
