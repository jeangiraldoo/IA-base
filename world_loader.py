from enum import Enum
import os
import pygame


class WORLD_ITEMS(Enum):
    EMPTY = 0
    OBSTACLE = 1
    ASTRONAUT = 2
    ROCKY_TERRAIN = 3
    VOLCANIC_TERRAIN = 4
    SHIP = 5
    SCIENTIFIC_SAMPLE = 6

# Build absolute path to the assets directory next to this module
ASSETS_DIR = os.path.join(os.path.dirname(__file__), "assets")

def _load_image(filename):
    path = os.path.join(ASSETS_DIR, filename)
    if not os.path.isfile(path):
        raise FileNotFoundError(f"Asset not found: {path}")
    return pygame.image.load(path)

WORLD_ITEMS_SPRITES = {
    WORLD_ITEMS.EMPTY.value: _load_image("ground.png"),
    WORLD_ITEMS.OBSTACLE.value: _load_image("obstacle.png"),
    WORLD_ITEMS.ASTRONAUT.value: _load_image("astronaut.png"),
    WORLD_ITEMS.ROCKY_TERRAIN.value: _load_image("rocky_terrain.png"),
    WORLD_ITEMS.VOLCANIC_TERRAIN.value: _load_image("volcan.png"),
    WORLD_ITEMS.SHIP.value: _load_image("ship.png"),
    WORLD_ITEMS.SCIENTIFIC_SAMPLE.value: _load_image("scientific_sample.png"),
}

def build_matrix_from_txt_file():
    
    ASSETS_DIR = os.path.join(os.path.dirname(__file__), "Prueba1.txt")
    with open(ASSETS_DIR, "r") as file:
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
