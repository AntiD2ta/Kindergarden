from random import shuffle
from .string import DIRT
from math import sqrt


directions = [(-1, 0), (0, 1), (1, 0), (0, -1)]

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


def get_length(house):
    return (len(house), len(house[0]))


def count_dirt(house):
    return len([0 for r in house for c in r if DIRT in c.value])


def distance(x, y): 
    '''
    Euclidian distance
    '''
    return int(sqrt(abs(x[0] - y[0]) ** 2 + abs(x[1] - y[1]) ** 2))
