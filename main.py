import pygame
import numpy as np
import math

# Constants
WIDTH, HEIGHT = 1000, 800
CENTER = np.array([WIDTH // 2, HEIGHT // 2])
AU = 1.496e11  # Astronomical Unit in meters
G = 6.67430e-11  # Gravitational constant
SCALE = 250 / AU  # Pixels per meter (scaled for screen)
TIMESTEP = 60 * 60 * 24  # One day in seconds

# Pygame setup
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Solar System Simulation")
clock = pygame.time.Clock()

# Colors
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
BLUE = (100, 149, 237)
RED = (188, 39, 50)
GREY = (80, 78, 81)
ORANGE = (255, 165, 0)
COMET_COLOR = (200, 255, 255)

class Body:
    def __init__(self, name, mass, x, y, vx, vy, color, radius):
        self.name = name
        self.mass = mass
        self.pos = np.array([x, y], dtype='float64')
        self.vel = np.array([vx, vy], dtype='float64')
        self.color = color
        self.radius = radius
        self.orbit = []

    def update_position(self, bodies):
        total_force = np.array([0.0, 0.0])
        for body in bodies:
            if body is self:
                continue
            r_vec = body.pos - self.pos
            distance = np.linalg.norm(r_vec)
            force_dir = r_vec / distance
            force_mag = G * self.mass * body.mass / distance**2
            total_force += force_dir * force_mag

        acceleration = total_force / self.mass
        self.vel += acceleration * TIMESTEP
        self.pos += self.vel * TIMESTEP
        self.orbit.append(self.screen_pos())

    def screen_pos(self):
        return CENTER + self.pos * SCALE

    def draw(self, surface):
        x, y = self.screen_pos().astype(int)
        pygame.draw.circle(surface, self.color, (x, y), self.radius)
        if len(self.orbit) > 2:
            pygame.draw.lines(surface, self.color, False, self.orbit[-300:], 1)

# Sun (stationary)
sun = Body("Sun", 1.989e30, 0, 0, 0, 0, YELLOW, 20)

# Planets
planets = [
    Body("Mercury", 3.3e23, 0, 0.387 * AU, 47000, 0, GREY, 4),
    Body("Venus", 4.87e24, 0, 0.723 * AU, 35000, 0, ORANGE, 6),
    Body("Earth", 5.97e24, 0, 1.0 * AU, 29780, 0, BLUE, 6),
    Body("Mars", 6.42e23, 0, 1.52 * AU, 24070, 0, RED, 5),
]

# Add sun to the body list for gravitational interaction
all_bodies = [sun] + planets

# Comet with hyperbolic orbit
comet = Body("Comet", 1e14, -2 * AU, 0.5 * AU, 60000 / 2, 15000 / 2, COMET_COLOR, 3)

# Main loop
running = True
while running:
    clock.tick(60)
    screen.fill((0, 0, 0))

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Update and draw sun and planets
    for body in planets:
        body.update_position([sun])
        body.draw(screen)

    # Draw sun (doesn't move)
    sun.draw(screen)

    # Update and draw comet
    comet.update_position([sun])
    comet.draw(screen)

    pygame.display.flip()

pygame.quit()
