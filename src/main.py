# External imports
import pygame
import numpy as np
from collections import deque # Fast append and pop

# Local imports
from utils import (
    WIDTH, HEIGHT, CENTER, AU, G, DEFAULT_SCALE, TIMESTEP,
    MAX_TIMESTEP, Colors, TRAIL_LENGTH
)

from simulation_logic import Body


# Pygame setup
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Solar System Simulation")
clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 16)

curr_scale = DEFAULT_SCALE

# Sun (stationary)
sun = Body("Sun", 1.989e30, 0, 0, 0, 0, Colors.YELLOW, 20)

# Planets
planets = [
    Body("Mercury", 3.3e23, 0, 0.387 * AU, 47000, 0, Colors.GREY, 4),
    Body("Venus", 4.87e24, 0, 0.723 * AU, 35000, 0, Colors.PINK, 6),
    Body("Earth", 5.97e24, 0, 1.0 * AU, 29780, 0, Colors.BLUE, 6),
    Body("Mars", 6.42e23, 0, 1.52 * AU, 24070, 0, Colors.RED, 5),
    Body("Jupiter", 1.90e27, 0, 5.2 * AU, 13070, 0, Colors.ORANGE, 10),
    Body("Saturn", 5.68e26, 0, 9.52 * AU, 9680, 0, Colors.SATURN_YELLOW, 9),
    Body("Uranus", 8.68e25, 0, 19.22 * AU, 6800, 0, Colors.URANUS_BLUE, 8),
    Body("Neptune", 1.02e26, 0, 30.09 * AU, 5400, 0, Colors.NEPTUNE_BLUE, 8),
]

# Comet with hyperbolic orbit
comet = Body("Comet", 1e14, -2 * AU, 0.5 * AU, 60000 / 2, 15000 / 2, Colors.COMET_COLOR, 3)

# Keep track of every celestial body
all_bodies = [sun] + planets + [comet]

# Main loop
running = True
paused = False
fullscreen = False
while running:
    clock.tick(60)
    screen.fill((0, 0, 0))

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            running = False

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_EQUALS or event.key == pygame.K_PLUS or event.key == pygame.K_UP: # Zoom in
                curr_scale = all_bodies[0].curr_scale
                curr_scale *= 1.1

                for body in all_bodies:
                    body.curr_scale = curr_scale

            elif event.key == pygame.K_MINUS or event.key == pygame.K_UNDERSCORE or event.key == pygame.K_DOWN: # Zoom out
                curr_scale = all_bodies[0].curr_scale
                curr_scale /= 1.1

                for body in all_bodies:
                    body.curr_scale = curr_scale

            elif event.key == pygame.K_LEFT: # Slow down simulation
                time_step = all_bodies[0].time_step
                time_step /= 1.1

                for body in all_bodies:
                    body.time_step = time_step

            elif event.key == pygame.K_RIGHT: # Speed up simulation
                time_step = all_bodies[0].time_step
                time_step *= 1.1
                time_step = min(MAX_TIMESTEP, time_step) # Cap the time step to a maximum value

                for body in all_bodies:
                    body.time_step = time_step

            elif event.key == pygame.K_r: # Reset scale
                for body in all_bodies:
                    body.curr_scale = DEFAULT_SCALE

            elif event.key == pygame.K_t: # Reset time step
                for body in all_bodies:
                    body.time_step = TIMESTEP

            elif event.key == pygame.K_f: # Toggle fullscreen
                fullscreen = not fullscreen
                if fullscreen:
                    screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
                else:
                    screen = pygame.display.set_mode((WIDTH, HEIGHT))

            elif event.key == pygame.K_SPACE: # Pause/Unpause
                paused = not paused

    # Update and draw planets (and comet)
    if not paused:         
    
        for body in planets:
            body.update_position([sun])
            body.draw(screen)

        # Update and draw comet
        comet.update_position([sun])
        comet.draw(screen)
    else:
        # Draw planets and comet without updating
        for body in planets:
            body.draw(screen)
        comet.draw(screen)

    # Draw sun (doesn't move)
    sun.draw(screen)

    # Display current scale and speed
    scale_text = font.render(f"Scale: {all_bodies[0].curr_scale / DEFAULT_SCALE:.2f}x", True, Colors.WHITE)
    time_text = font.render(f"Speed: {all_bodies[0].time_step / TIMESTEP:.2f}x", True, Colors.WHITE)
    screen.blit(scale_text, (10, 10))
    screen.blit(time_text, (10, 30))
    # See FPS for more info
    fps_text = font.render(f"FPS: {int(clock.get_fps())}", True, Colors.WHITE)
    screen.blit(fps_text, (10, 50))
    
    # Display the screen
    pygame.display.flip()

pygame.quit()
