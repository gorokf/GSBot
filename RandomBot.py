from hlt import *
from networking import *

'''
STILL = 0
NORTH = 1
EAST = 2
SOUTH = 3
WEST = 4
'''

myID, gameMap = getInit()
sendInit("FiodorBot")


def surrouned_by_allies(location):
    for d in CARDINALS:
        neighbour_site = gameMap.getSite(location, d)
        if neighbour_site.owner != myID:
            return 0
    return 1


def highest_production_direction(location):
    highest_production = gameMap.getSite(location).production
    highest_production_direction = STILL
    for d in CARDINALS:
        neighbour_production = gameMap.getSite(location, d).production
        if neighbour_production > highest_production:
            highest_production = neighbour_production
            highest_production_direction = d
    return highest_production_direction


def lowest_strength_direction(location):
    lowest_strength = 999
    lowest_strength_direction = STILL
    for d in CARDINALS:
        neighbour = gameMap.getSite(location, d)
        neighbour_strength = neighbour.strength
        if neighbour.owner != myID and neighbour_strength < lowest_strength:
            lowest_strength = neighbour_strength
            lowest_strength_direction = d
    return lowest_strength_direction


def move(location):
    site = gameMap.getSite(location)

    if surrouned_by_allies(location):
        if site.strength > 150:
            return Move(location, WEST)
        elif site.strength > 100:
            return Move(location, NORTH)
        elif site.strength < site.production * 5:
            return Move(location, STILL)
        else:
            return Move(location, highest_production_direction(location))
    else:
        if site.strength < site.production * 5:
            return Move(location, STILL)
        else:
            attack_direction = lowest_strength_direction(location)
            if gameMap.getSite(location, attack_direction).strength > site.strength:
                return Move(location, STILL)
            else:
                return Move(location, attack_direction)


while True:
    moves = []
    gameMap = getFrame()
    for y in range(gameMap.height):
        for x in range(gameMap.width):
            location = Location(x, y)
            if gameMap.getSite(location).owner == myID:
                moves.append(move(location))
    sendFrame(moves)

