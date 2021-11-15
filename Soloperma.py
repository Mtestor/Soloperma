from numpy.core.fromnumeric import size
import pygame
from numpy import full
from numpy.random import default_rng
from enum import IntEnum
from copy import copy

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
        self._playersInConflict = []
    
    def ownCase(self, casePos):
        self._ownedUnitCase.append(casePos)
        self._owningPerTurn -= 1
    
    def loseCase(self, casePos):
        self._ownedUnitCase.remove(casePos)
        if not self._ownedUnitCase:
            self._isAnnexed = True
            self._playersInConflict = []

    def ownedCase(self):
        return tuple(self._ownedUnitCase)

    def ownerIs(self):
        return copy(self._owner)

    def howManyPerTurn(self):
        return copy(self._owningPerTurn)

    def resetOwningPerTurn(self):
        self._owningPerTurn = self._owningPerTurnMax

    def cantDoAnything(self):
        self._owningPerTurn -= 1

    def annexTerritory(self):
        self._owningPerTurnMax +=1

    def isAnnexed(self):
        return self._isAnnexed

    def playersInConflict(self):
        return copy(self._playersInConflict)

    def isInConflict(self):
        return True if self._playersInConflict else False

    def addPlayerToConflict(self, player):
        if player in self._playersInConflict or player == self:
            return
        self._playersInConflict.append(player)
        player.addPlayerToConflict(self)
    
    def playerAnnexed(self, player):
        self._playersInConflict.remove(player)
        self.annexTerritory()

    def sumOfConflict(self):
        return sum((len(player.ownedCase()) for player in self.playersInConflict()))

    def size(self):
        return len(self.ownedCase())

    _owner = UnitCaseOwner.NOBODY
    _ownedUnitCase = []
    _owningPerTurn = 0
    _owningPerTurnMax = 0
    _isAnnexed = False
    _playersInConflict = []
    

WINDOW_HEIGHT = 570
WINDOW_LENGHT = 570

UNIT_CASE_SIZE = 30

MAP_LENGTH = WINDOW_LENGHT // UNIT_CASE_SIZE
MAP_HEIGHT = WINDOW_HEIGHT // UNIT_CASE_SIZE

MAP_BACKGROUND = pygame.Color('white')

gameMap = full((MAP_HEIGHT, MAP_LENGTH), UnitCaseOwner.NOBODY)

player0 = Territory(UnitCaseOwner.PLAYER0)
player1 = Territory(UnitCaseOwner.PLAYER1)
player2 = Territory(UnitCaseOwner.PLAYER2)
player3 = Territory(UnitCaseOwner.PLAYER3)
player4 = Territory(UnitCaseOwner.PLAYER4)
player5 = Territory(UnitCaseOwner.PLAYER5)
player6 = Territory(UnitCaseOwner.PLAYER6)
player7 = Territory(UnitCaseOwner.PLAYER7)

def unitCaseOwnerToPlayer(unitCaseOwner: UnitCaseOwner):
    if unitCaseOwner == UnitCaseOwner.PLAYER0:
        return player0
    if unitCaseOwner == UnitCaseOwner.PLAYER1:
        return player1
    if unitCaseOwner == UnitCaseOwner.PLAYER2:
        return player2
    if unitCaseOwner == UnitCaseOwner.PLAYER3:
        return player3
    if unitCaseOwner == UnitCaseOwner.PLAYER4:
        return player4
    if unitCaseOwner == UnitCaseOwner.PLAYER5:
        return player5
    if unitCaseOwner == UnitCaseOwner.PLAYER6:
        return player6
    else :
        return player7

def annexCase(casePos: tuple, player: Territory):
    gameMap[casePos] = player.ownerIs()
    player.ownCase(casePos)

rng = default_rng()

def randomPlacer(player: Territory, takenCase: list):
    (x, y) = (rng.integers(MAP_LENGTH), rng.integers(MAP_HEIGHT))
    while((x, y) in takenCase):
        (x, y) = (rng.integers(MAP_LENGTH), rng.integers(MAP_HEIGHT))
    annexCase((x, y), player)
    takenCase.append((x, y))
    takenCase.append((x+1, y))
    takenCase.append((x, y+1))
    takenCase.append((x-1, y))
    takenCase.append((x, y-1))

takenCase = []

# annexCase((0, 9), player0)
# annexCase((0, 10), player0)
# annexCase((0, 11), player0)
# annexCase((0, 3) , player1)
# annexCase((0, 4) , player1)
# annexCase((0, 5) , player1)
# annexCase((0, 6) , player1)
# annexCase((0, 7) , player1)
# annexCase((0, 8) , player1)
# annexCase((0, 0) , player2)
# annexCase((0, 1) , player2)
# annexCase((0, 2) , player2)

randomPlacer(player0, takenCase)
randomPlacer(player1, takenCase)
randomPlacer(player2, takenCase)
randomPlacer(player3, takenCase)
randomPlacer(player4, takenCase)
randomPlacer(player5, takenCase)
randomPlacer(player6, takenCase)
randomPlacer(player7, takenCase)

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

def basicAnnexingAi(player: Territory, annexedOwner):
    isItBreak = True
    while player.howManyPerTurn() > 0 and isItBreak:
        isItBreak = False
        if player.isInConflict() and UnitCaseOwner.NOBODY in annexedOwner:
            break
        for unitCase in player.ownedCase():
            if isItBreak:
                break
            neighborsCase = adjacentCase(unitCase)
            i = 0
            for neighborCase in neighborsCase:
                if neighborCase in annexedOwner:
                    casePos = (unitCase[0], unitCase[1] - 1) if i == 0 else (unitCase[0] - 1 , unitCase[1]) if i == 1 else (unitCase[0], unitCase[1] + 1) if i == 2 else (unitCase[0] + 1, unitCase[1])
                    if neighborCase == UnitCaseOwner.NOBODY:
                        annexCase(casePos, player)
                    elif neighborCase != UnitCaseOwner.NOBODY and (player.size() >= player.sumOfConflict() or unitCaseOwnerToPlayer(neighborCase).sumOfConflict() > unitCaseOwnerToPlayer(neighborCase).size()):
                        playerConflict = unitCaseOwnerToPlayer(neighborCase)
                        annexCase(casePos, player)
                        # print(player.ownerIs())
                        # print(playerConflict.ownerIs())
                        # print(casePos)
                        playerConflict.loseCase(casePos)
                        if playerConflict.isAnnexed():
                            player.playerAnnexed(playerConflict)
                            if playerConflict != player0:
                                turnStack.remove(playerConflict)
                    else:
                        # print(unitCaseOwnerToPlayer(neighborCase).ownerIs())
                        # print(player.ownerIs())
                        # print(unitCaseOwnerToPlayer(neighborCase).sumOfConflict())
                        # print(unitCaseOwnerToPlayer(neighborCase).size())
                        i += 1
                        continue
                    for unitCaseAd in adjacentCase(casePos):
                        if unitCaseAd != UnitCaseOwner.NOBODY and unitCaseAd != UnitCaseOwner.OUTSIDE:
                            player.addPlayerToConflict(unitCaseOwnerToPlayer(unitCaseAd))
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

screen = pygame.display.set_mode((WINDOW_LENGHT, WINDOW_HEIGHT), 0)
screen.fill(MAP_BACKGROUND)
pygame.display.set_caption("Soloperma")
icon = pygame.image.load("Soloperma.bmp")
pygame.display.set_icon(icon)

IS_GAMELOOP_STOPPED = False
fpsLimiter = pygame.time.Clock()

turnStack = [player1, player2, player3, player4, player5, player6, player7]
player0IsBeingAnnexed = False

font = pygame.font.Font(None, 32)
textWin = font.render('You have win!', True, Color('black'), Color('white'))
textLost = font.render('You have lost!', True, Color('black'), Color('white'))
textRect = textLost.get_rect()
textRect.center = (WINDOW_LENGHT // 2, WINDOW_HEIGHT // 2)

LEFT = 1

while not IS_GAMELOOP_STOPPED:

    if not turnStack or player0.isAnnexed():
        screen.fill(Color('white'))
        screen.blit(textLost, textRect) if player0.isAnnexed() else screen.blit(textWin, textRect)
        pygame.display.flip()
        #pygame.time.wait(2000)
        IS_GAMELOOP_STOPPED = True
    
    if player0IsBeingAnnexed:
        player0.cantDoAnything()

    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                IS_GAMELOOP_STOPPED = True
        elif event.type == pygame.QUIT:
            IS_GAMELOOP_STOPPED = True
        elif event.type == pygame.MOUSEMOTION:
            #print("yoru")
            if not turnStack:
                continue
            if player0IsBeingAnnexed:
                continue
            if pygame.mouse.get_pressed() == (1, 0, 0):
                #print("yora")
                posCase = pixelPosToGridPos(event.pos)
                if player0.howManyPerTurn() > 0 and isBorderingCase(posCase, player0.ownerIs()):
                    if player0.isInConflict():
                        #print("oh no")
                        #[print(x.ownerIs()) for x in player0.playersInConflict()]
                        for player in player0.playersInConflict():
                            if player.ownerIs() == gameMap[posCase]:
                                if player0.size() >= player0.sumOfConflict() or player.sumOfConflict() > player.size():
                                    gameMap[posCase] = player0.ownerIs()
                                    player0.ownCase(posCase)
                                    player.loseCase(posCase)
                                    #print(player.ownerIs())
                                    #print(posCase)
                                    for unitCase in adjacentCase(posCase):
                                        if unitCase != UnitCaseOwner.NOBODY and unitCase != UnitCaseOwner.OUTSIDE:
                                            player0.addPlayerToConflict(unitCaseOwnerToPlayer(unitCase))
                                    if player.isAnnexed():
                                        player0.playerAnnexed(player)
                                        turnStack.remove(player)
                                else:
                                    player0IsBeingAnnexed = True
                                break
                    elif isCaseOwnable(posCase):
                        gameMap[posCase] = player0.ownerIs()
                        player0.ownCase(posCase)
                        for unitCase in adjacentCase(posCase):
                            if unitCase != UnitCaseOwner.NOBODY and unitCase != UnitCaseOwner.OUTSIDE:
                                player0.addPlayerToConflict(unitCaseOwnerToPlayer(unitCase))


    if player0.howManyPerTurn() <= 0:
        for player in turnStack[:]:
            player.resetOwningPerTurn()
            if player.isInConflict():
                playersConflictOwner = [playerConflict.ownerIs() for playerConflict in player.playersInConflict()]
                basicAnnexingAi(player, playersConflictOwner)
            else :
                basicAnnexingAi(player, [UnitCaseOwner.NOBODY])
        player0.resetOwningPerTurn()

    screen.fill(MAP_BACKGROUND)
    drawMap()
    pygame.display.flip()
    fpsLimiter.tick(30)