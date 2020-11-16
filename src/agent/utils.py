from src.env.string import OBSTACLE
from ..env import distance, get_adjacents, directions, get_length, BABY

#BFS
def closest_target(house, pos, target, check:list):
    q = [pos]
    visited = {pos}
    p = dict()

    while len(q) > 0:
        v = q.pop(0)
        for u in get_adjacents(house, v):
            if house[u[0]][u[1]].value == target:
                return get_parent(p, pos, u)
            if u not in visited and u not in check:
                q.append(u)
                visited.add(u)
                p[u] = v
    return []


def get_parent(p, first, cur, acum=[]):
    acum.append(cur)
    if p[cur] == first:
        acum.reverse()
        return acum
    return get_parent(p[cur])


def count_free_babies(house):
    return len([0 for r in house for c in r if c.value == BABY])
