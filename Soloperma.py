import pygame
import numpy as np
from enum import IntEnum
from copy import copy
from pygame import display

from pygame.color import Color

class UnitCaseOwner(IntEnum):
    NOBODY = 0
    OUTSIDE = 1
    PLAYER0 = 2
    PLAYER1 = 3
    PLAYER2 = 4
    PLAYER3 = 5
    PLAYER4 = 6
    PLAYER5 = 7
    PLAYER6 = 8
    PLAYER7 = 9

class Territory:
    """ Class that represent a territory """
    def __init__(self, owner: UnitCaseOwner, owningPerTurnMax: int = 1):
        self._owner = owner
        self._owningPerTurnMax = owningPerTurnMax
        self._owningPerTurn = self._owningPerTurnMax
        self._ownedUnitCase = []
        self._isAnnexed = False
    
    def ownCase(self, casePos):
        self._ownedUnitCase.append(casePos)
        self._owningPerTurn -= 1
    
    def loseCase(self, casePos):
        self._ownedUnitCase.remove(casePos)
        if not self._ownedUnitCase:
            self._isAnnexed = True

    def ownedCase(self):
        return tuple(self._ownedUnitCase)

    def ownerIs(self):
        return copy(self._owner)

    def howManyPerTurn(self):
        return copy(self._owningPerTurn)

    def resetOwningPerTurn(self):
        self._owningPerTurn = self._owningPerTurnMax

    def AnnexTerritory(self):
        self._owningPerTurnMax +=1

    def isAnnexed(self):
        return self._isAnnexed

    _owner = UnitCaseOwner.NOBODY
    _ownedUnitCase = []
    _owningPerTurn = 0
    _owningPerTurnMax = 0
    _isAnnexed = False
    

WINDOW_HEIGHT = 1080
WINDOW_LENGHT = 1080

UNIT_CASE_SIZE = 30

MAP_LENGTH = WINDOW_LENGHT // UNIT_CASE_SIZE
MAP_HEIGHT = WINDOW_HEIGHT // UNIT_CASE_SIZE

MAP_BACKGROUND = pygame.Color('white')

gameMap = np.full((MAP_HEIGHT, MAP_LENGTH), UnitCaseOwner.NOBODY)

player0 = Territory(UnitCaseOwner.PLAYER0)
player1 = Territory(UnitCaseOwner.PLAYER1)
player2 = Territory(UnitCaseOwner.PLAYER2)
player3 = Territory(UnitCaseOwner.PLAYER3)
player4 = Territory(UnitCaseOwner.PLAYER4)
player5 = Territory(UnitCaseOwner.PLAYER5)
player6 = Territory(UnitCaseOwner.PLAYER6)
player7 = Territory(UnitCaseOwner.PLAYER7)

gameMap[5:10, 10] = player0.ownerIs()
gameMap[0, 0:5] = player1.ownerIs()
gameMap[35, 35] = player2.ownerIs()
gameMap[15, 5] = player3.ownerIs()
gameMap[35, 10] = player4.ownerIs()
gameMap[22, 22] = player5.ownerIs()
gameMap[5, 35] = player6.ownerIs()
gameMap[17, 17] = player7.ownerIs()

for k in range(6):
    player0.ownCase((5 + k, 10))
    player1.ownCase((0, k))

player2.ownCase((35, 35))
player3.ownCase((15, 5))
player4.ownCase((35, 10))
player5.ownCase((22, 22))
player6.ownCase((5, 35))
player7.ownCase((17, 17))

player0.resetOwningPerTurn()
player1.resetOwningPerTurn()
player2.resetOwningPerTurn()
player3.resetOwningPerTurn()
player4.resetOwningPerTurn()
player5.resetOwningPerTurn()
player6.resetOwningPerTurn()
player7.resetOwningPerTurn()

def unitCaseColor(unitCase):
    if unitCase == player0.ownerIs():
        return pygame.Color('orange')
    if unitCase == player1.ownerIs():
        return pygame.Color('red')
    if unitCase == player2.ownerIs():
        return pygame.Color('black')
    if unitCase == player3.ownerIs():
        return pygame.Color('green')
    if unitCase == player4.ownerIs():
        return pygame.Color('brown')
    if unitCase == player5.ownerIs():
        return pygame.Color('blue')
    if unitCase == player6.ownerIs():
        return pygame.Color('purple')
    if unitCase == player7.ownerIs():
        return pygame.Color('cyan')
    return pygame.Color('white')

# Convert pixel position in pixelPos to grid position
def pixelPosToGridPos(pixelPos):
    return (pixelPos[0] // UNIT_CASE_SIZE, pixelPos[1] // UNIT_CASE_SIZE)

# Return if the unit case at casePos is owned by a territory
def isCaseOwnable(casePos):
    return True if gameMap[casePos[0], casePos[1]] == UnitCaseOwner.NOBODY else False

# Return a tuple of adjacent unit case owner to the unit case as casePos position
# The returned tuple is formated in this form : (left case, up case, right case, down case)
# If a adjacent unit case is out of map it return UnitCaseOwner.OUTSIDE
def adjacentCase(casePos):
    adjacentCaseTuple = []
    if casePos[1] == 0:
        adjacentCaseTuple.append(UnitCaseOwner.OUTSIDE)
    else:
        adjacentCaseTuple.append(gameMap[casePos[0], casePos[1] - 1])
    if casePos[0] == 0:
        adjacentCaseTuple.append(UnitCaseOwner.OUTSIDE)
    else:
        adjacentCaseTuple.append(gameMap[casePos[0] - 1, casePos[1]])
    if casePos[1] == MAP_LENGTH - 1:
        adjacentCaseTuple.append(UnitCaseOwner.OUTSIDE)
    else:
        adjacentCaseTuple.append(gameMap[casePos[0], casePos[1] + 1])
    if casePos[0] == MAP_HEIGHT - 1:
        adjacentCaseTuple.append(UnitCaseOwner.OUTSIDE)
    else:
        adjacentCaseTuple.append(gameMap[casePos[0] + 1, casePos[1]])
    return tuple(adjacentCaseTuple)


# Return if one bordering unit case of the unit case at casePos position is owned by owner
def isBorderingCase(casePos, owner):
    for unitCase in adjacentCase(casePos):
        if unitCase == owner:
            return True
    return False

def basicAnnexingAi(player: Territory, annexedOwner: UnitCaseOwner):
    isItBreak = True
    while player.howManyPerTurn() > 0 and isItBreak:
        isItBreak = False
        for unitCase in player.ownedCase():
            if isItBreak:
                break
            neighborsCase = adjacentCase(unitCase)
            i = 0
            for neighborCase in neighborsCase:
                if neighborCase == annexedOwner:
                    casePos = (unitCase[0], unitCase[1] - 1) if i == 0 else (unitCase[0] - 1 , unitCase[1]) if i == 1 else (unitCase[0], unitCase[1] + 1) if i == 2 else (unitCase[0] + 1, unitCase[1])
                    gameMap[casePos] = player.ownerIs()
                    player.ownCase(casePos)
                    isItBreak = True
                    break
                i += 1

def drawMap():
    for row in range(MAP_HEIGHT):
        for column in range(MAP_LENGTH):
            unitCase = gameMap[row, column]
            if unitCase != UnitCaseOwner.NOBODY:
                screen.fill(unitCaseColor(unitCase), (row * UNIT_CASE_SIZE, column * UNIT_CASE_SIZE, UNIT_CASE_SIZE, UNIT_CASE_SIZE))

pygame.init()

screen = pygame.display.set_mode((WINDOW_LENGHT, WINDOW_HEIGHT))
screen.fill(MAP_BACKGROUND)
pygame.display.set_caption("Soloperma")

IS_GAMELOOP_STOPPED = False
fpsLimiter = pygame.time.Clock()

turnStack = [player1, player2, player3, player4, player5, player6, player7]

font = pygame.font.Font(None, 32)
textWin = font.render('You have win!', True, Color('black'), Color('white'))
textLost = font.render('You have lost!', True, Color('black'), Color('white'))
textRect = textLost.get_rect()
textRect.center = (WINDOW_LENGHT // 2, WINDOW_HEIGHT // 2)

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
                if isCaseOwnable(posCase) and isBorderingCase(posCase, player0.ownerIs()) and player0.howManyPerTurn() > 0:
                    gameMap[posCase[0], posCase[1]] = player0.ownerIs()
                    player0.ownCase(posCase)

    if player0.howManyPerTurn() <= 0:
        for player in turnStack:
            player.resetOwningPerTurn()
            basicAnnexingAi(player, UnitCaseOwner.NOBODY)
        player0.resetOwningPerTurn()
    
    if not turnStack or player1.isAnnexed():
        screen.fill(Color('white'))
        screen.blit(textLost, textRect) if player1.isAnnexed() else screen.blit(textWin, textRect)
        pygame.display.flip()
        pygame.time.wait(3000)
        IS_GAMELOOP_STOPPED = True


    screen.fill(MAP_BACKGROUND)
    drawMap()
    pygame.display.flip()
    fpsLimiter.tick(10)