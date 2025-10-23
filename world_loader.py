with open("Prueba1.txt", "r") as file:
    file_lines = file.readlines()

def build_matrix_from_txt_file(file_lines):
    matrix = []
    for line in file_lines:
        stripped_line: str = line.replace("\n", "").replace(" ", "")

        new_row: list[int] = [int(x) for x in stripped_line]
        matrix.append(new_row)

    return matrix

print("Result")
print(build_matrix_from_txt_file(file_lines))
