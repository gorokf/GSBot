from hlt import *
from networking import *
import math
import numpy as np

'''
STILL = 0
NORTH = 1
EAST = 2
SOUTH = 3
WEST = 4
'''

EASTORNORTH = [a for a in range(1, 2)]

myID, gameMap = getInit()
sendInit("FiodorReal")


def closest_to_edge_direction(location, height, width):
    x = location.x
    y = location.y

    distance_north = 0
    while y - distance_north >= 0:
        cell = Location(x, y - distance_north)
        if gameMap.getSite(cell).owner != myID:
            break
        distance_north += 1

    distance_south = 0
    while y + distance_south <= height-1:
        cell = Location(x, y + distance_south)
        if gameMap.getSite(cell).owner != myID:
            break
        distance_south += 1

    distance_east = 0
    while x + distance_east <= width-1:
        cell = Location(x + distance_east, y)
        if gameMap.getSite(cell).owner != myID:
            break
        distance_east += 1

    distance_west = 0
    while x - distance_west >= 0:
        cell = Location(x - distance_west, y)
        if gameMap.getSite(cell).owner != myID:
            break
        distance_west += 1

    distances = np.array([distance_north, distance_east, distance_south, distance_west])
    return CARDINALS[np.argmin(distances)]


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


def highest_efficiency_direction(location):
    highest_efficiency = -999
    highest_efficiency_direction = STILL
    for d in CARDINALS:
        neighbour = gameMap.getSite(location, d)
        if neighbour.owner != myID:
            current = gameMap.getSite(location)
            neighbour_efficiency = neighbour.production / max(math.ceil(neighbour.strength - current.strength / max(current.production, 1)), 1)
            if neighbour_efficiency > highest_efficiency:
                highest_efficiency = neighbour_efficiency
                highest_efficiency_direction = d
    return highest_efficiency_direction


def target_location_strong_cell(location, height, width):
    return closest_to_edge_direction(location, height, width)


def move(location, turn, height, width):
    site = gameMap.getSite(location)

    if site.strength < site.production * 4:
        return Move(location, STILL)
    elif surrouned_by_allies(location):
        if site.strength > 50:
            return Move(location, target_location_strong_cell(location, height, width))
        else:
            return Move(location, highest_production_direction(location))
    else:
        attack_direction = highest_efficiency_direction(location)
        if gameMap.getSite(location, attack_direction).strength >= site.strength:
            return Move(location, STILL)
        else:
            return Move(location, attack_direction)

turn = 0
while True:
    moves = []
    gameMap = getFrame()

    for y in range(gameMap.height):
        for x in range(gameMap.width):
            location = Location(x, y)
            if gameMap.getSite(location).owner == myID:
                moves.append(move(location, turn, gameMap.height, gameMap.width))
    sendFrame(moves)
    turn += 1

