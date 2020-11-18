from ..shared import *
from random import randint, shuffle, random


def build_house(n, m, dirt, obstacules, babies):
    house = [[EMPTY for _ in range(m)] for _ in range(n)]


def build_corral(house, c):
    n, m = get_length(house)
    i, j = gen_coordenates(n, m)
    corrals = [(i, j)]
    while c:
        house[i][j].update(CORRAL)
        house[i][j].isFixed = True
        #This may fail, so I keep a list with the rest of corrals to continue generation for there if adj is empty
        adj = []
        while len(adj) == 0:
            if len(corrals) == 0:
                return False
            i, j = corrals.pop()
            adj = list(filter(lambda x: house[x[0]][x[1]].value != CORRAL, get_adjacents(house, (i, j), True)))

        i, j = adj[0]
        corrals.append((i, j))
        c -= 1
    return True


def generate_babies(house, b):
    n, m = get_length(house)
    babies = set()
    while b:
        i, j = gen_coordenates(n, m)
        if not house[i][j].isFixed and house[i][j].update(BABY, [BABY]):
            b -= 1
            babies.add((i,j))    
    return babies 


def generate_obstacules(house, obstacules):
    n, m = get_length(house)
    remaining = n * m * obstacules // 100
    while remaining:
        i, j = gen_coordenates(n, m)
        if not house[i][j].isFixed and house[i][j].update(OBSTACLE, [BABY, OBSTACLE]):
            remaining -= 1   


def generate_dirt(house, dirtiness):
    n, m = get_length(house)
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
    n, m = get_length(house)
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


def gen_coordenates_robot(house):
    n, m = get_length(house)
    empty_cells = [(i, j) for i in range(n) for j in range(m) if house[i][j].value == EMPTY]
    idx = randint(0, len(empty_cells) - 1)
    return empty_cells[idx]
    

def get_cells(house, typex):
    return [cell for r in house for cell in r if cell.value is typex]


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


def move_babies(house, babies, log):
    for (x, y) in babies:
        if bernoulli():
            empty_adj = list(filter(lambda x: house[x[0]][x[1]].value in [EMPTY, OBSTACLE], get_adjacents(house, (x, y), True)))
            if len(empty_adj) > 0:
                i, j = empty_adj[0]
                if house[i][j].value == OBSTACLE:
                    d = (abs(x - i), abs(y - j))
                    if move_obstacules(house, (i, j), d):
                        house[i][j].update(BABY, old=house[x][y])
                        log.debug(f'Baby at ({x}, {y}) moved to ({i}, {j})')
                else:
                    house[i][j].update(BABY, old=house[x][y])
                    log.debug(f'Baby at ({x}, {y}) moved to ({i}, {j})')


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


def mess_up(house, s, log):
    for group in s:
        mess = get_mess(group)
        while mess:
            for (x, y) in group:
                i, j = get_adjacents(house, (x, y), True)[0]
                if house[i][j].update(DIRT, [CORRAL, DIRT, BABY, OBSTACLE, ROBOT]):
                    log.debug(f'Dirt created at ({i}, {j})')
                    house[i][j].dirty = True
                mess -= 1
                if mess == 0:
                    break


def bernoulli(p = 0.5):
    return random() < p


def user_control(on):
    if on:
        s = '$'
        while s != '':
            print('Press ENTER to continue:')
            s = input()