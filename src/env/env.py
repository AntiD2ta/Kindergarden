from .utils import *
from .cell import Cell
from ..agent import current_agent
from ..shared import ROBOT
from ..logging import LoggerFactory as Logger

log = Logger('Kindergarden').getChild('Env')

class Env:
    def __init__(self, n, m, dirt, obstacules, babies, t, p, robot):
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

    def change(self):
        n, m = get_length(self.house)
        babies = [(i, j) for i in range(n) for j in range(m) if self.house[i][j].value == BABY]

        move_babies(self.house, babies, log, self.p)
        free_babies = get_free_babies(self.house, babies)
        babies_in_order = len(free_babies) == 0

        total_mess = count_dirt(self.house)
        if total_mess == 0 and babies_in_order:
            log.info('The robot completed its job successfully!!!', 'change')
            self.running = False
            self.succeded = True
            return

        mess_up(self.house, free_babies, log)
        n, m = get_length(self.house)
        if total_mess * 100 // (n * m) >= 60:
            log.info('The robot is fired!!!')
            self.running = False

    def simulate(self, interactive):
        while self.running and self.time < 100:
            self.time += 1
            user_control(interactive)
            self.robot.action(self.house)
            if self.time % self.t == 0:
                log.debug('Environment change!!!', 'simulate')
                self.change()
            if interactive:
                log.info(f'House at time {self.time}:')
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
        col_num = ['   ']
        col_num += [f'{idx}     ' for idx, _ in enumerate(self.house[0])]
        h = [''.join(col_num)]
        for idx, r in enumerate(self.house):
            h.append(str(idx) + '  ' + ' '.join([str(c) for c in r]))
        return '\n'.join(h)
