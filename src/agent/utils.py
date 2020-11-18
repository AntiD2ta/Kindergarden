from ..shared import get_adjacents, get_length, BABY, DIRT

#BFS
def closest_target(house, pos, target, check:list):
    q = [pos]
    visited = {pos}
    p = dict()

    while len(q) > 0:
        v = q.pop(0)
        for u in get_adjacents(house, v):
            value = house[u[0]][u[1]].value
            if u not in visited and value not in check:
                q.append(u)
                visited.add(u)
                p[u] = v
                if value == target:
                    return get_parent(p, pos, u, [])
    return []


def get_parent(p, first, cur, acum):
    '''
    Build parent list path
    '''
    acum.append(cur)
    if p[cur] == first:
        acum.reverse()
        return acum
    return get_parent(p, first, p[cur], acum)


def count_free_babies(house):
    return len([0 for r in house for c in r if c.value == BABY])


def group_target(house, target, threshold):
    n, m = get_length(house)
    matches = {(i, j) for i in range(n) for j in range(m) if house[i][j].value == target}
    groups = set()
    for m in matches:
        g = [m]
        for other in matches - {m}:
            if distance(m, other) <= threshold:
                g.append(other)
        groups.add(frozenset(g))
    return groups

#DFS
def paths_to_target(house, first, pos, target, visited, p, check:list, acum:list, max_path):
    for u in get_adjacents(house, pos):
        value = house[u[0]][u[1]].value
        if u not in visited and value not in check:
            visited.add(u)
            p[u] = pos
            path = get_parent(p, first, u, [])
            if len(path) <= max_path: 
                if value == target:
                    acum.append(path)
                    visited.remove(u)
                    continue
                paths_to_target(house, first, u, target, visited.copy(), p.copy(), check, acum, max_path)


def distance(x, y): 
    '''
    Manhattan distance
    '''
    return abs(x[0] - y[0]) + abs(x[1] - y[1])