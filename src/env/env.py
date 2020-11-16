from .utils import *
from .cell import Cell
from ..logging import LoggerFactory as Logger
from ..agent import current_agent

log = Logger(name="Env")


class Env:
    def __init__(self, n, m, dirt, obstacules, babies, t):
        if not validate_args(n, m, dirt, obstacules, babies):
            log.error('Invalid args, there is no empty cells or dirtiness is greater than 60 percent')

        house = [[Cell() for _ in range(m)] for _ in range(n)]
        build_corral(house, babies)
        babies_list = generate_babies(house, babies)
        generate_obstacules(house, obstacules)
        generate_dirt(house, dirt)
        self.house = house
        self.babies = babies_list
        log.debug('House created')

        self.t = t
        self.time = 1
        self.running = True
        self.succeded = False
        self.robot = current_agent(gen_coordenates_robot(self.house))
        log.info(f'Robot of type {str(self.robot)} created at ({self.robot.pos[0]}, {self.robot.pos[1]})')
        log.info('Env created') 

    def change(self):
        move_babies(self.house, self.babies, log)
        free_babies = get_free_babies(self.house, self.babies)
        babies_in_order = len(free_babies) == 0

        total_mess = count_dirt(self.house)
        if total_mess == 0 and babies_in_order:
            log.info('The robot completed its job successfully!!!')
            self.running = False
            self.succeded = True
            return

        mess_up(self.house, free_babies)
        n, m = get_length(self.house)
        if total_mess * 100 // (n * m) >= 60:
            log.info('The robot is fired!!!')
            self.running = False

    def simulate(self, interactive):
        while self.running or self.time < 100:
            user_control(interactive)
            self.robot.action(self.house)
            if self.time % self.t == 0:
                self.change()
            self.time += 1
            if interactive:
                log.info(f'House at time {self.time}:')
                print(self)

        mess = count_dirt(self.house)
        return (self.succeded, mess)


    def __str__(self):
        col_num = [' ']
        col_num += [f'  {idx}  ' for idx, _ in enumerate(self.house[0])]
        h = [''.join(col_num)]
        for idx, r in enumerate(self.house):
            h.append(str(idx) + '  ' + ' '.join([str(c) for c in r]))
        return '\n'.join(h)
