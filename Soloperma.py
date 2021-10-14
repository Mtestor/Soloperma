from typing import Tuple
import pygame
import numpy as np
from enum import IntEnum

from pygame.color import Color

class unitCaseOwner(IntEnum):
    NOBODY = 0
    OUTSIDE = 1
    PLAYER = 2
    COMPUTER1 = 3
    COMPUTER2 = 4
    COMPUTER3 = 5
    COMPUTER4 = 6
    COMPUTER5 = 7
    COMPUTER6 = 8
    COMPUTER7 = 9

WINDOW_HEIGHT = 1080
WINDOW_LENGHT = 1080

UNIT_CASE_SIZE = 30

MAP_LENGTH = WINDOW_LENGHT // UNIT_CASE_SIZE
MAP_HEIGHT = WINDOW_HEIGHT // UNIT_CASE_SIZE

MAP_BACKGROUND = pygame.Color('white')

gameMap = np.full((MAP_HEIGHT, MAP_LENGTH), unitCaseOwner.NOBODY)

gameMap[5:10, 10] = unitCaseOwner.PLAYER 
gameMap[0, 0:5] = unitCaseOwner.COMPUTER1
gameMap[35, 35] = unitCaseOwner.COMPUTER2
gameMap[15, 0:5] = unitCaseOwner.COMPUTER3
gameMap[35, 0:10] = unitCaseOwner.COMPUTER4
gameMap[22, 22] = unitCaseOwner.COMPUTER5
gameMap[0:5, 35] = unitCaseOwner.COMPUTER6
gameMap[17, 17] = unitCaseOwner.COMPUTER7

def unitCaseColor(unitCase):
    if unitCase == unitCaseOwner.PLAYER:
        return pygame.Color('orange')
    if unitCase == unitCaseOwner.COMPUTER1:
        return pygame.Color('red')
    if unitCase == unitCaseOwner.COMPUTER2:
        return pygame.Color('black')
    if unitCase == unitCaseOwner.COMPUTER3:
        return pygame.Color('green')
    if unitCase == unitCaseOwner.COMPUTER4:
        return pygame.Color('brown')
    if unitCase == unitCaseOwner.COMPUTER5:
        return pygame.Color('blue')
    if unitCase == unitCaseOwner.COMPUTER6:
        return pygame.Color('purple')
    if unitCase == unitCaseOwner.COMPUTER7:
        return pygame.Color('cyan')
    return pygame.Color('white')

# Convert pixel position in pixelPos to grid position
def pixelPosToGridPos(pixelPos):
    return (pixelPos[0] // UNIT_CASE_SIZE, pixelPos[1] // UNIT_CASE_SIZE)

# Return if the unit case at casePos is owned by a territory
def isCaseOwnable(casePos):
    return True if gameMap[casePos[0], casePos[1]] == unitCaseOwner.NOBODY else False

# Return a tuple of adjacent unit case owner to the unit case as casePos position
# The returned tuple is formated in this form : (left case, up case, right case, down case)
# If a adjacent unit case is out of map it return unitCaseOwner.OUTSIDE
def adjacentCase(casePos):
    adjacentCaseTuple = []
    if casePos[1] == 0:
        adjacentCaseTuple.append(unitCaseOwner.OUTSIDE)
    else:
        adjacentCaseTuple.append(gameMap[casePos[0], casePos[1] - 1])
    if casePos[0] == 0:
        adjacentCaseTuple.append(unitCaseOwner.OUTSIDE)
    else:
        adjacentCaseTuple.append(gameMap[casePos[0] - 1, casePos[1]])
    if casePos[1] == MAP_LENGTH - 1:
        adjacentCaseTuple.append(unitCaseOwner.OUTSIDE)
    else:
        adjacentCaseTuple.append(gameMap[casePos[0], casePos[1] + 1])
    if casePos[0] == MAP_HEIGHT - 1:
        adjacentCaseTuple.append(unitCaseOwner.OUTSIDE)
    else:
        adjacentCaseTuple.append(gameMap[casePos[0] + 1, casePos[1]])
    return tuple(adjacentCaseTuple)


# Return if one bordering unit case of the unit case at casePos position is owned by owner
def isBorderingCase(casePos, owner):
    for unitCase in adjacentCase(casePos):
        if unitCase == owner:
            return True
    return False

def drawMap():
    for row in range(MAP_HEIGHT):
        for column in range(MAP_LENGTH):
            unitCase = gameMap[row, column]
            if unitCase != unitCaseOwner.NOBODY:
                screen.fill(unitCaseColor(unitCase), (row * UNIT_CASE_SIZE, column * UNIT_CASE_SIZE, UNIT_CASE_SIZE, UNIT_CASE_SIZE))

pygame.init()

screen = pygame.display.set_mode((WINDOW_LENGHT, WINDOW_HEIGHT))
screen.fill(MAP_BACKGROUND)
pygame.display.set_caption("Soloperma")

IS_GAMELOOP_STOPPED = False
fpsLimiter = pygame.time.Clock()

LEFT = 1

while not IS_GAMELOOP_STOPPED:
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                IS_GAMELOOP_STOPPED = True
        elif event.type == pygame.QUIT:
            IS_GAMELOOP_STOPPED = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == LEFT:
                posCase = pixelPosToGridPos(event.pos)
                if isCaseOwnable(posCase) and isBorderingCase(posCase, unitCaseOwner.PLAYER):
                    gameMap[posCase[0], posCase[1]] = unitCaseOwner.PLAYER

    
    screen.fill(MAP_BACKGROUND)
    drawMap()
    pygame.display.flip()
    fpsLimiter.tick(10)