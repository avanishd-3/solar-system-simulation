# External imports
import pygame
import numpy as np
from collections import deque # Fast append and pop

# Local imports
from utils import (
    WIDTH, HEIGHT, CENTER, AU, G, DEFAULT_SCALE, TIMESTEP,
    Colors,
    TRAIL_LENGTH
)

# Global variables
curr_scale = DEFAULT_SCALE

class Body:
    """
    Class representing a celestial body in the simulation.

    Attributes
    ----------
    name : str
        Name of the celestial body.
    mass : float
        Mass of the celestial body in kg.
    pos : np.ndarray
        Position of the celestial body in 2D space (x, y).
    vel : np.ndarray
        Velocity of the celestial body in 2D space (vx, vy).
    color : tuple
        Color of the celestial body in RGB format.
    radius : int
        Radius of the celestial body in pixels.
    orbit : list
        List of positions representing the orbit trail of the celestial body.

    Methods
    -------
    update_position(bodies)
        Updates the position and velocity of the celestial body based on gravitational forces from other bodies.
    screen_pos()
        Converts the position of the celestial body to screen coordinates.
    draw(surface)
        Draws the celestial body and its orbit on the given surface.
    """

    def __init__(self, name, mass, x, y, vx, vy, color, radius):
        self.name = name
        self.mass = mass
        self.pos = np.array([x, y], dtype='float64')
        self.vel = np.array([vx, vy], dtype='float64')
        self.color = color
        self.radius = radius
        self.orbit = deque(maxlen=TRAIL_LENGTH)  # Store only the last TRAIL_LENGTH positions

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
        self.orbit.append(self.pos.copy())

        # Remove oldest points from the orbit trail
        if len(self.orbit) > TRAIL_LENGTH:
            self.orbit.pop(0)
        

    def screen_pos(self):
        return CENTER + self.pos * curr_scale

    def draw(self, surface):
        x, y = self.screen_pos().astype(int)
        pygame.draw.circle(surface, self.color, (x, y), self.radius)

        # Draw orbit
        if len(self.orbit) > 2:
            points = [CENTER + pos * curr_scale for pos in self.orbit]
            # Make orbit trail smoother and less pixelated
            pygame.draw.aalines(surface, self.color, False, points, 1)


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

# Add sun to the body list for gravitational interaction
all_bodies = [sun] + planets

# Comet with hyperbolic orbit
comet = Body("Comet", 1e14, -2 * AU, 0.5 * AU, 60000 / 2, 15000 / 2, Colors.COMET_COLOR, 3)

# Main loop
running = True
paused = False
while running:
    clock.tick(60)
    screen.fill((0, 0, 0))

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            running = False

        # Zoom controls
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_EQUALS or event.key == pygame.K_PLUS or event.key == pygame.K_UP: # Zoom in
                curr_scale *= 1.1

            elif event.key == pygame.K_MINUS or event.key == pygame.K_UNDERSCORE or event.key == pygame.K_DOWN: # Zoom out
                curr_scale /= 1.1

            elif event.key == pygame.K_r: # Reset scale
                curr_scale = DEFAULT_SCALE

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

    # Display current scale
    scale_text = font.render(f"Scale: {curr_scale / DEFAULT_SCALE:.2f}x", True, Colors.WHITE)
    screen.blit(scale_text, (10, 10))
    pygame.display.flip()

pygame.quit()
