from world_loader import build_map_from_matrix, build_matrix_from_txt_file, ui_loop

raw_matrix = build_matrix_from_txt_file()
print(raw_matrix)
game_map = build_map_from_matrix(raw_matrix)
ui_loop(game_map)
