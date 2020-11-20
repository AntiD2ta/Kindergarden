from .utils import *
from .cell import Cell
from ..agent import current_agent
from ..shared import ROBOT
from ..logging import LoggerFactory as Logger

log = None

class Env:
    def __init__(self, n, m, dirt, obstacules, babies, t, p, robot):
        global log
        log = Logger('Kindergarden').getChild('Env')

        if not validate_args(n, m, dirt, obstacules, babies):
            log.error('Invalid args, there is no empty cells or dirtiness is greater than 60 percent')

        while True:
            house = [[Cell() for _ in range(m)] for _ in range(n)]
            if build_corral(house, babies):
                break
        generate_babies(house, babies)
        generate_obstacules(house, obstacules)
        generate_dirt(house, dirt)
        self.house = house
        log.debug('House created')

        self.p = p
        self.t = t
        self.time = 0
        self.running = True
        self.succeded = False
        x, y = gen_coordenates_robot(self.house)
        if robot is 'Practical':
            self.robot = current_agent[robot]((x, y), self.t)
        else:
            self.robot = current_agent[robot]((x, y))
    
        self.house[x][y].update(ROBOT)
        log.info(f'Robot of type {str(self.robot)} created at ({x}, {y})')
        log.info('Env created') 

    def natural_change(self):
        n, m = get_length(self.house)
        babies = [(i, j) for i in range(n) for j in range(m) if self.house[i][j].value == BABY]

        move_babies(self.house, babies, log, self.p)
        free_babies = get_free_babies(self.house, babies)
        babies_in_order = len(free_babies) == 0
        mess_up(self.house, free_babies, log)

        total_mess = count_dirt(self.house)
        if total_mess == 0 and babies_in_order:
            log.info('The robot completed its job successfully!!!', 'change')
            self.running = False
            self.succeded = True
            return

        n, m = get_length(self.house)
        if total_mess * 100 // (n * m) >= 60:
            log.info('The robot is fired!!!')
            self.running = False

    def random_change(self):
        n, m = get_length(self.house)
        for i in range(n):
            for j in range(m):
                x, y = gen_coordenates(n, m)
                self.house[i][j], self.house[x][y] = self.house[x][y], self.house[i][j]

        corrals = [(i, j) for i in range(n) for j in range(m) if CORRAL in self.house[i][j].value]
        new_corrals = [corrals.pop(0)]
        while len(corrals) > 0:
            adj = []
            while len(adj) == 0:
                if len(new_corrals) == 0:
                    self.random_change()
                    return
                i, j = new_corrals.pop()
                adj = list(filter(lambda x: CORRAL not in self.house[x[0]][x[1]].value, get_adjacents(self.house, (i, j), True)))

            i, j = adj[0]
            x, y = corrals.pop(0)
            self.house[i][j], self.house[x][y] = self.house[x][y], self.house[i][j]
            new_corrals.append((i, j))

        robot = [(i, j) for i in range(n) for j in range(m) if ROBOT in self.house[i][j].value][0]
        self.robot.pos = robot


    def simulate(self, interactive):
        while self.running and self.time < self.t * 100:
            self.time += 1
            user_control(interactive)
            self.robot.action(self.house)
            self.natural_change()
            if interactive:
                log.info(f'House at time {self.time}:')
                print(self)
            if self.time % self.t == 0:
                log.debug('Environment random change!!!', 'simulate')
                self.random_change()
                if interactive:
                    print()
                    print(self)

        log.info(f'House at the final turn, time {self.time}:')
        print(self)
        log.info(f'The robot collected {self.robot.garbage_collected} units of dirt', 'simulate')
        mess = count_dirt(self.house)
        return (self.succeded, mess)

    def copy_house(self):
        new_house = list()
        for r in self.house:
            new_row = list()
            for c in r:
                new_row.append(c.copy())
            new_house.append(new_row)
        return new_house

    def __str__(self):
        col_num = ['    ']
        col_num += [f'{idx}     ' for idx, _ in enumerate(self.house[0])]
        h = [''.join(col_num)]
        for idx, r in enumerate(self.house):
            h.append(str(idx) + ''.join([' ' for _ in range(2 - len(str(idx)))]) + '  ' + ' '.join([str(c) for c in r]))
        return '\n'.join(h)
