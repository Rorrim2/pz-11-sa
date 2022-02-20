from drawable import Drawable
import pygame, random
from contants import *


class Cell(Drawable):
    """ Food - is green(ish)
    """
    def __init__(self, surface):
        super().__init__(surface)
        gimme_color = lambda : random.randint(50,100)
        self.x = random.randint(2,PLATFORM_WIDTH)
        self.y = random.randint(2,PLATFORM_HEIGHT)
        self.mass = 1
        self.color = (gimme_color(), 200, gimme_color())

    def draw(self):
        """Draws a cell as a simple circle.
        """
        pygame.draw.circle(self.surface, self.color, (self.x*RATIO,self.y*RATIO), int(self.mass*RATIO))
        
class CellList(Drawable):
    """Used to group and organize cells.
    It is also keeping track of living/ dead cells.
    """
    def __init__(self, surface, numOfCells):
        super().__init__(surface)
        self.count = numOfCells
        self.list = []
        for i in range(self.count): self.list.append(Cell(self.surface))

    def draw(self):
        for cell in self.list:
            cell.draw()