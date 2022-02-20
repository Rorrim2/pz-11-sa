from drawable import Drawable
import pygame
from contants import *
import random
import numpy as np


def drawText(message,pos,font,color=(255,255,255)):
    """Blits text to main (global) screen.
    """
    MAIN_SURFACE.blit(font.render(message,1,color),pos)

def getDistance(a, b):
    """Calculates Euclidean distance between given points.
    """
    return (((a[0]-b[0])**2)+((a[1]-b[1])**2))**(0.5)

class MovingThingy(Drawable):
    """Used to represent the concept of a player.
    """
    FONT_COLOR = (50, 50, 50)
    
    def __init__(self, surface, font, isPlayer=True, name = "", agent=None):
        super().__init__(surface)
        gc = lambda : random.randint(100,150)
        self.font = font
        self.x = random.randint(0,200)
        self.y = random.randint(0,200)
        self.radius = 1
        self.score = 0
        self.delta = 1/TICKS
        self.isPlayer = isPlayer
        self.isDead = False
        self.color = (gc(),gc(),255) if isPlayer else (255,gc(),gc())
        if name: self.name = name
        else: self.name = "A"
        self.agent = agent

    def velocity(self, radius):
        log_value = np.log(radius) + 1
        return float(MAX_VELOCITY - max(0, min(log_value, MAX_VELOCITY - 1))) # clamp

    def collisionDetection(self, foods, others):
        """Detects cells being inside the radius of current player.
        Those cells are eaten.
        """
        self.last_score= self.score
        # update eaten foods
        foods_to_remove = [f for f in foods if getDistance((f.x,f.y), (self.x, self.y)) <= self.radius] 
        self.eat_food(len(foods_to_remove))
        for f in foods_to_remove:
            foods.remove(f)
        # update eaten enemies
        enemies_to_remove = []
        for o in others:
            if getDistance((o.x,o.y), (self.x, self.y)) <= self.radius:
                if o.radius<self.radius:
                    enemies_to_remove.append(o)
                elif o.radius == self.radius:
                    continue
                else:
                    self.isDead = True
                    break
        self.eat_other_players(enemies_to_remove)
        for e in enemies_to_remove:
            e.isDead = True

    def get_pos_after_actio(self, x,y,action):
        nx,ny = x,y
        if 'U' in action: #UP
            ny += self.velocity(self.radius) * self.delta
        if 'D' in action: #DOWN
            ny -= self.velocity(self.radius) * self.delta
        if 'L' in action: #LEFT
            nx  -= self.velocity(self.radius) * self.delta
        if 'R' in action: #RIGHT
            nx  += self.velocity(self.radius) * self.delta

        nx  = float(np.clip(nx , 0, PLATFORM_WIDTH))
        ny = float(np.clip(ny, 0, PLATFORM_HEIGHT))
        return nx,ny

    def move(self, playerModeOn=True, state=None):
        """Updates players current position depending on player's mouse relative position.
        """
        directions = {'U': False, 'D':False, 'L':False, 'R':False}
        
        if playerModeOn:
            dX, dY = pygame.mouse.get_pos()[0]/4,pygame.mouse.get_pos()[1]/4
            if dX > (self.x+self.radius): directions['R'] = True
            elif dX < (self.x-self.radius):directions['L'] = True
            if dY > (self.y+self.radius): directions['U'] = True
            elif dY < (self.y-self.radius):directions['D'] = True
        else:
            direction = self.agent.get_action(state, False, self.x,self.y,self.radius,self)
            self.last_action = direction
            for d in direction:
                directions[d] = True

        if directions['U']: #UP
            self.y += self.velocity(self.radius) * self.delta
        if directions['D']: #DOWN
            self.y -= self.velocity(self.radius) * self.delta
        if directions['L']: #LEFT
            self.x  -= self.velocity(self.radius) * self.delta
        if directions['R']: #RIGHT
            self.x  += self.velocity(self.radius) * self.delta

        self.x  = float(np.clip(self.x , 0, PLATFORM_WIDTH))
        self.y = float(np.clip(self.y, 0, PLATFORM_HEIGHT))
        
    def draw(self):
        """Draws the player as an outlined circle.
        """
        pygame.draw.circle(self.surface, self.color, (self.x*RATIO,self.y*RATIO), self.radius*RATIO)
        # Draw player's name
        fw, fh = self.font.size(self.name)
        drawText(self.name, (self.x*RATIO - int(fw/2), self.y*RATIO - int(fh/2)), self.font, MovingThingy.FONT_COLOR)

    def update_radius(self):
        self.radius = float(np.sqrt(self.score))
        self.radius = 1 if self.radius < 1 else self.radius

    def eat_food(self, number_of_eaten_food: int):
        self.score += number_of_eaten_food
        self.update_radius()

    def eat_other_players(self, other_players):
        players_total_score = sum((p.score if p.score > 0 else 1) for p in other_players)
        self.score += int(players_total_score)
        self.update_radius()