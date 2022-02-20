import pygame,random,math
import numpy as np
from painter import Painter
from contants import *
from cells import CellList
from grid import Grid
from movable import MovingThingy
from enemy_agents import RandomAgent, CloseFoodAgent
from fa_agent import FunctionApproximationAgent

# Pygame initialization
pygame.init()
pygame.display.set_caption(NAME)
clock = pygame.time.Clock()

try:
    font = pygame.font.Font("Ubuntu-B.ttf",20)
    big_font = pygame.font.Font("Ubuntu-B.ttf",24)
except:
    print("Font file not found: Ubuntu-B.ttf")
    font = pygame.font.SysFont('Ubuntu',20,True)
    big_font = pygame.font.SysFont('Ubuntu',24,True)

faMode = True
for i in range(10):

    # Initialize essential entities
    grid = Grid(MAIN_SURFACE)
    foods = CellList(MAIN_SURFACE, 50)

    player = MovingThingy(MAIN_SURFACE, font, True, "P", agent=FunctionApproximationAgent(alpha=0.01, epsilon=0.1, discount=0.99,get_legal_actions=get_all_actions))

    painter = Painter()
    painter.add(grid)
    painter.add(foods)
    painter.add(player)

    enemies = []

    number_of_enemies = random.randint(2,5)
    for i in range(number_of_enemies):
        if i == 0:
            enemy = MovingThingy(MAIN_SURFACE, font, False, "C", agent=CloseFoodAgent())
            enemies.append(enemy)
            painter.add(enemy)
        enemy = MovingThingy(MAIN_SURFACE, font, False, "R", agent=RandomAgent())
        enemies.append(enemy)
        painter.add(enemy)

    paintingMode = True

    previousState = None

    # Game main loop
    while(True):
        foods_for_state = []
        for f in foods.list:
            foods_for_state.append((f.x, f.y)) 
        player_for_state = {'r':player.radius, 'x':player.x, 'y':player.y}
        enemies_for_state = []
        for e in enemies:
            enemies_for_state.append({'r':e.radius, 'x':e.x, 'y':e.y})
        state = {'f':foods_for_state, 'p':player_for_state, 'e':enemies_for_state}

        if previousState is not None:
            reward = player.score - player.last_score
            if player.isDead:
                reward = -10
            player.agent.update(previousState, player.last_action, reward/100, state)  

        clock.tick(TICKS)
        # move
        # player.move() # if human playing
        player.move(False, state)
        for e in enemies:
            e.move(False, state)
        # collisions
        player.collisionDetection(foods.list, enemies)
        if player.isDead:
            closeEnemy= enemies[0]
            for e in enemies:
                if e.name == "C":
                    closeEnemy = e
            print("Player has diededed, scorePlayer and scoreClose: ", player.score, closeEnemy.score)
            break
        if len(foods_for_state) == 0 and len(enemies_for_state) == 0:
            print("Player has won, score: ", player.score)
            break
        for i in range(len(enemies)):
            enemies[i].collisionDetection(foods.list, enemies[:i] + enemies[i+1:])
        # check if dead in enemies and remove
        enemies_to_remove = []
        for e in enemies:
            if e.isDead:
                enemies_to_remove.append(e)
        for e in enemies_to_remove:
            enemies.remove(e)
            painter.paintings.remove(e)

        previousState = state

        # drawing
        MAIN_SURFACE.fill((242,251,255))
        
        if paintingMode == True:
            painter.paint()
            for e in pygame.event.get():
                if(e.type == pygame.KEYDOWN):
                    if(e.key == pygame.K_ESCAPE):
                        pygame.quit()
                        quit()
                if(e.type == pygame.QUIT):
                    pygame.quit()
                    quit()
            # Start calculating next frame
            pygame.display.flip()

if faMode:
    player.agent.print_w()