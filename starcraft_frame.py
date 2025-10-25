import pygame

STARTCRAFT_PANE_DIMENSIONS = (120, 120)
current_astro_frame = 0
astro_frame_delay = 200
last_astro_update = pygame.time.get_ticks()

astro_frames = [
    pygame.transform.scale(
        pygame.image.load("assets/astronaut/back/back.png"), STARTCRAFT_PANE_DIMENSIONS
    ),
    pygame.transform.scale(
        pygame.image.load("assets/astronaut/front/front.png"),
        STARTCRAFT_PANE_DIMENSIONS,
    ),
    pygame.transform.scale(
        pygame.image.load("assets/astronaut/left/left.png"), STARTCRAFT_PANE_DIMENSIONS
    ),
    pygame.transform.scale(
        pygame.image.load("assets/astronaut/right/right.png"),
        STARTCRAFT_PANE_DIMENSIONS,
    ),
]


def draw_astronaut_animation(screen, SIDEPANEL_RECTS):
    global current_astro_frame, last_astro_update
    extra_panel = SIDEPANEL_RECTS["EXTRA"]

    now = pygame.time.get_ticks()
    if now - last_astro_update > astro_frame_delay:
        current_astro_frame = (current_astro_frame + 1) % len(astro_frames)
        last_astro_update = now

    frame = astro_frames[current_astro_frame]
    rect = frame.get_rect(center=extra_panel.center)
    screen.blit(frame, rect)
