from .string import *
from random import randint, shuffle, random
from math import sqrt

directions = [(-1, 0), (0, 1), (1, 0), (0, -1)]

def build_house(n, m, dirt, obstacules, babies):
    house = [[EMPTY for _ in range(m)] for _ in range(n)]


def build_corral(house, c):
    n, m = get_length(house)
    i, j = gen_coordenates(n, m)
    while c:
        house[i][j].update(CORRAL)
        house[i][j].isFixed = True
        i, j = list(filter(lambda x: house[x[0]][x[1]].value != CORRAL, get_adjacents(house, (i, j), True)))[0]
        c -= 1


def generate_babies(house, b):
    n, m = (len(house), len(house[0]))
    babies = set()
    while b:
        i, j = gen_coordenates(n, m)
        if not house[i][j].isFixed and house[i][j].update(BABY, [BABY]):
            b -= 1
            babies.add((i,j))    
    return babies 


def generate_obstacules(house, obstacules):
    n, m = (len(house), len(house[0]))
    remaining = n * m * obstacules // 100
    while remaining:
        i, j = gen_coordenates(n, m)
        if not house[i][j].isFixed and house[i][j].update(OBSTACLE, [BABY, OBSTACLE]):
            remaining -= 1   


def generate_dirt(house, dirtiness):
    n, m = (len(house), len(house[0]))
    remaining = n * m * dirtiness // 100
    while remaining:
        i, j = gen_coordenates(n, m)
        if not house[i][j].isFixed and house[i][j].update(DIRT, [BABY, OBSTACLE, DIRT]):
            remaining -= 1  
            house[i][j].dirty = True


def validate_args(n, m, dirt, obstacules, babies):
    cells = n * m - babies * 2
    cells -= n * m * dirt // 100
    cells -= n * m * obstacules // 100
    return cells > 0 and dirt < 60


def get_adjacents(house, cur, shuffled=False):
    adj = list()
    n, m = (len(house), len(house[0]))
    for d in directions:
        x = cur[0] + d[0]
        y = cur[1] + d[1]
        if x < n and x >= 0 and y >= 0 and y < m:
            adj.append((x, y))
    if shuffled:
        shuffle(adj)
    return adj


def gen_coordenates(n, m):
    return (randint(0, n-1), randint(0, m-1))


def get_length(house):
    return (len(house), len(house[0]))


def get_cells(house, typex):
    return [cell for r in house for cell in r if cell.value is typex]


def distance(x, y): 
    return int(sqrt(abs(x[0] - y[0]) ** 2 + abs(x[1] - y[1]) ** 2))


def get_free_babies(house, babies):
    free_babies = {b for b in babies if not house[b[0]][b[1]].isFixed}
    groups = set()
    for baby in free_babies:
        g = [baby]
        for other in free_babies - {baby}:
            if distance(baby, other) <= 2:
                g.append(other)
        groups.add(frozenset(g))
    return groups


def move_babies(house, babies):
    for (x, y) in babies:
        if bernoulli():
            empty_adj = list(filter(lambda x: house[x[0]][x[1]].value in [EMPTY, OBSTACLE], get_adjacents(house, (x, y), True)))
            if len(empty_adj) > 0:
                i, j = empty_adj[0]
                if house[i][j].value == OBSTACLE:
                    d = (abs(x - i), abs(y - j))
                    if move_obstacules(house, (i, j), d):
                        house[i][j].update(BABY, house[x][y])
                else:
                    house[i][j].update(BABY, house[x][y])


def move_obstacules(house, pos, d):
    n, m = get_length(house)
    x, y = (pos[0] + d[0], pos[1] + d[1])
    
    if x < n and x >= 0 and y >= 0 and y < m:
        if house[x][y].value == EMPTY:
            house[x][y].update(OBSTACLE)
            return True
        elif house[x][y].value == OBSTACLE:
            return move_obstacules(house, (x, y), d)
        return False
    return False
        

def get_mess(s):
    mess = 1
    l = len(s)
    if l >= 3:
        mess = 6
    elif l == 2:
        mess = 3
    return mess


def mess_up(house, s):
    mess = get_mess(s)
    while mess:
        for (x, y) in s:
            i, j = get_adjacents(house, (x, y), True)[0]
            house[i][j].update(DIRT, [CORRAL, DIRT, BABY, OBSTACLE, ROBOT]):
            mess -= 1
            if mess == 0:
                break


def bernoulli(p = 0.5):
    return random() < p