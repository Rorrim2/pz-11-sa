from drawable import Drawable
import pygame
from contants import *

class Grid(Drawable):
    """Used to represent the backgroun grid.
    """
    def __init__(self, surface):
        super().__init__(surface)
        self.color = (230,240,240)

    def draw(self):
        # A grid is a set of horizontal and vertical lines
        for i in range(0,(PLATFORM_WIDTH+1), 10):
            pygame.draw.line(self.surface, self.color, (i*RATIO, 0), (i*RATIO, PLATFORM_WIDTH*RATIO), 2) # vertical
            pygame.draw.line(self.surface, self.color, (0, i*RATIO), (PLATFORM_WIDTH*RATIO, i*RATIO), 2) # horizontal
