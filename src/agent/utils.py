from ..shared import get_adjacents, BABY

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
    acum.append(cur)
    if p[cur] == first:
        acum.reverse()
        return acum
    return get_parent(p, first, p[cur], acum)


def count_free_babies(house):
    return len([0 for r in house for c in r if c.value == BABY])
