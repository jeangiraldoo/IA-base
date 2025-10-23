from enum import Enum
import pygame
from ui import ui_loop


class WORLD_ITEMS(Enum):
    EMPTY = 0
    OBSTACLE = 1
    ASTRONAUT = 2
    ROCKY_TERRAIN = 3
    VOLCANIC_TERRAIN = 4
    SHIP = 5
    SCIENTIFIC_SAMPLE = 6


WORLD_ITEMS_SPRITES = {
    WORLD_ITEMS.EMPTY.value: pygame.image.load("./assets/grass.jpeg"),
    WORLD_ITEMS.OBSTACLE.value: pygame.image.load("./assets/obstacle.png"),
    WORLD_ITEMS.ASTRONAUT.value: pygame.image.load("./assets/astronaut.png"),
    WORLD_ITEMS.ROCKY_TERRAIN.value: pygame.image.load("./assets/astronaut.png"),
    WORLD_ITEMS.VOLCANIC_TERRAIN.value: pygame.image.load("./assets/volcan.jpg"),
    WORLD_ITEMS.SHIP.value: pygame.image.load("./assets/astronaut.png"),
    WORLD_ITEMS.SCIENTIFIC_SAMPLE.value: pygame.image.load("./assets/astronaut.png"),
}


def build_matrix_from_txt_file():
    with open("Prueba1.txt", "r") as file:
        file_lines = file.readlines()

    matrix = []
    for line in file_lines:
        stripped_line: str = line.replace("\n", "").replace(" ", "")

        new_row: list[int] = [int(x) for x in stripped_line]
        matrix.append(new_row)

    return matrix


def build_map_from_matrix(matrix):
    map = []
    for row in matrix:
        map_row = []
        for column in row:
            column_image = WORLD_ITEMS_SPRITES[column]
            map_row.append(column_image)
        map.append(map_row)

    return map
