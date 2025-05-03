# External imports
import numpy as np
import pygame
from collections import deque  # Fast append and pop

# Local imports
from utils import (
    WIDTH, HEIGHT, CENTER, AU, G, DEFAULT_SCALE, TIMESTEP,
    MAX_TIMESTEP, Colors, TRAIL_LENGTH
)

# Global variables
curr_scale = DEFAULT_SCALE
time_step = TIMESTEP

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

    Properties (getters/setters)
    ----------
    curr_scale : float
        Current scale factor for converting astronomical units to pixels.

    time_step : float
        Current time step for the simulation.
    """

    def __init__(self, name, mass, x, y, vx, vy, color, radius, curr_scale=DEFAULT_SCALE, time_step=TIMESTEP):
        
        self._name = name
        self.mass = mass
        self.pos = np.array([x, y], dtype='float64')
        self._vel = np.array([vx, vy], dtype='float64')
        self._color = color
        self._radius = radius
        self._orbit = deque(maxlen=TRAIL_LENGTH)  # Store only the last TRAIL_LENGTH positions
        self._curr_scale = curr_scale
        self._time_step = time_step

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

        # Calculate acceleration (by F=ma)
        acceleration = total_force / self.mass

        # Velocity Verlet integration
        self.pos += self._vel * self._time_step + 0.5 * acceleration * self._time_step**2

        # Update acceleration based on new position
        new_total_force = np.array([0.0, 0.0])
        for body in bodies:
            if body is self:
                continue

            r_vec = body.pos - self.pos
            distance = np.linalg.norm(r_vec)
            force_dir = r_vec / distance
            force_mag = G * self.mass * body.mass / distance**2
            new_total_force += force_dir * force_mag

        # Calculate new acceleration (by F=ma)
        new_acceleration = new_total_force / self.mass

        # Update velocity using the average of the old and new accelerations
        self._vel += 0.5 * (acceleration + new_acceleration) * self._time_step
        
        # Store the current position in the orbit trail
        self._orbit.append(self.pos.copy())

        # Remove oldest points from the orbit trail
        if len(self._orbit) > TRAIL_LENGTH:
            self._orbit.pop(0)
        

    def screen_pos(self):
        return CENTER + self.pos * self._curr_scale

    def draw(self, surface):
        # Get screen position
        x, y = self.screen_pos().astype(int)
        
        # Draw planet
        pygame.draw.circle(surface, self._color, (x, y), self._radius)

        # Draw orbit
        if len(self._orbit) > 2:
            points = [CENTER + pos * self._curr_scale for pos in self._orbit]
            # Make orbit trail smoother and less pixelated
            pygame.draw.aalines(surface, self._color, False, points, 1)

    @property
    def curr_scale(self):
        return self._curr_scale
    
    @curr_scale.setter
    def curr_scale(self, scale):
        self._curr_scale = scale

    @property
    def time_step(self):
        return self._time_step
    
    @time_step.setter
    def time_step(self, time_step):
        self._time_step = time_step