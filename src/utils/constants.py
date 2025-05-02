from collections import namedtuple
import numpy as np

# Constants
WIDTH, HEIGHT = 1000, 800
CENTER = np.array([WIDTH // 2, HEIGHT // 2])
AU = 1.496e11  # Astronomical Unit in meters (distance from Earth to Sun)
G = 6.67430e-11  # Gravitational constant
DEFAULT_SCALE = 250 / AU  # Pixels per meter (scaled for screen)
TIMESTEP = 60 * 60 * 24  # One day in seconds

# Colors

color_tuple = namedtuple('Colors', ['WHITE', 'YELLOW', 'BLUE', 'RED', 'GREY', 'PINK', 'ORANGE', 'SATURN_YELLOW',
                                    'URANUS_BLUE', 'NEPTUNE_BLUE',
                                    'COMET_COLOR'])

Colors = color_tuple(
    WHITE=(255, 255, 255),
    YELLOW=(255, 255, 0),
    BLUE=(100, 149, 237),
    RED=(188, 39, 50),
    GREY=(80, 78, 81),
    PINK=(255, 192, 203),
    ORANGE=(255, 165, 0),
    SATURN_YELLOW=(255, 255, 102),
    URANUS_BLUE=(178, 214, 219),
    NEPTUNE_BLUE=(41, 144, 181),
    COMET_COLOR=(200, 255, 255)
)

# Trail length
TRAIL_LENGTH = 300