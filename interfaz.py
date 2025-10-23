import pygame
from profundidad_evitando_ciclos import ejecutar_profundidad_animada
from world_loader import build_matrix_from_txt_file

pygame.init()
WHITE, BLACK, GRAY, BLUE = (255, 255, 255), (0, 0, 0), (200, 200, 200), (100, 149, 237)
FONT = pygame.font.SysFont("Arial", 24)
MENU_SIZE = (600, 400)

def draw_button(screen, text, rect, color):
    pygame.draw.rect(screen, color, rect)
    text_surface = FONT.render(text, True, BLACK)
    screen.blit(text_surface, (rect.x + 20, rect.y + 10))

def menu_principal():
    screen = pygame.display.set_mode(MENU_SIZE)
    pygame.display.set_caption("Proyecto IA - Menu Principal")
    while True:
        screen.fill(WHITE)
        draw_button(screen, "Busqueda No Informada", pygame.Rect(180, 120, 240, 50), GRAY)
        draw_button(screen, "Busqueda Informada", pygame.Rect(180, 200, 240, 50), GRAY)
        draw_button(screen, "Salir", pygame.Rect(180, 280, 240, 50), GRAY)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); return
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                if 180 <= x <= 420:
                    if 120 <= y <= 170:
                        menu_no_informada()
                    elif 200 <= y <= 250:
                        print("Busqueda informada en desarrollo")
                    elif 280 <= y <= 330:
                        pygame.quit(); return

def menu_no_informada():
    screen = pygame.display.set_mode(MENU_SIZE)
    pygame.display.set_caption("Busqueda No Informada")
    while True:
        screen.fill(WHITE)
        draw_button(screen, "Amplitud", pygame.Rect(180, 100, 240, 50), GRAY)
        draw_button(screen, "Costo Uniforme", pygame.Rect(180, 180, 240, 50), GRAY)
        draw_button(screen, "Profundidad (Evitar Ciclos)", pygame.Rect(130, 260, 340, 50), BLUE)
        draw_button(screen, "Volver al menu", pygame.Rect(180, 340, 240, 50), GRAY)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT: return
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                if 130 <= x <= 470 and 260 <= y <= 310:
                    ejecutar_profundidad_visual()
                elif 180 <= x <= 420 and 340 <= y <= 390:
                    return

def mostrar_reporte(screen, reporte):
    screen.fill(WHITE)
    pygame.display.set_caption("Reporte de Profundidad Evitando Ciclos")
    font = pygame.font.SysFont("Arial", 20)
    y = 60
    screen.blit(font.render(f"Nodos expandidos: {reporte['nodos']}", True, BLACK), (30, y)); y += 30
    screen.blit(font.render(f"Profundidad alcanzada: {reporte['profundidad']}", True, BLACK), (30, y)); y += 30
    screen.blit(font.render(f"Tiempo de computo: {reporte['tiempo']} s", True, BLACK), (30, y)); y += 40
    for muestra, pos, _ in reporte["muestras"]:
        screen.blit(font.render(f"{muestra} en {pos}", True, (0, 150, 0)), (30, y)); y += 30

    draw_button(screen, "Volver al menu", pygame.Rect(200, 340, 200, 40), BLUE)
    pygame.display.flip()

    esperando = True
    while esperando:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: esperando = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if 200 <= event.pos[0] <= 400 and 340 <= event.pos[1] <= 380:
                    esperando = False; menu_principal()

def ejecutar_profundidad_visual():
    with open("Prueba1.txt", "r") as f:
        file_lines = f.readlines()
    mundo = build_matrix_from_txt_file(file_lines)
    screen = pygame.display.set_mode((600, 600))
    pygame.display.set_caption("Profundidad Evitando Ciclos")
    reporte = ejecutar_profundidad_animada(screen, mundo)
    if reporte: mostrar_reporte(screen, reporte)

if __name__ == "__main__":
    menu_principal()
