from .string import EMPTY
from .utils import *
from .cell import Cell
from ..logging import LoggerFactory as Logger


log = Logger(name="Env")


class Env:
    def __init__(self, n, m, dirt, obstacules, babies, t):
        if not validate_args(n, m, dirt, obstacules, babies):
            log.error("Invalid args, there is no empty cells or dirtiness is greater than 60 percent")

        house = [[Cell() for _ in range(m)] for _ in range(n)]
        build_corral(house, babies)
        babies_list = generate_babies(house, babies)
        generate_obstacules(house, obstacules)
        generate_dirt(house, dirt)
        self.house = house
        self.babies = babies_list
        log.debug("House created")

        self.t = t
        self.time = 1
        self.running = True
        self.succeded = False
        #//TODO:build robot
        log.info("Env created") 

    def variate_env(self):
        move_babies(self.house, self.babies)
        free_babies = get_free_babies(self.house, self.babies)
        babies_in_order = len(free_babies) == 0

        total_mess = 0
        for r in self.house:
            total_mess += len(list(filter(lambda x: DIRT in self.house[x[0]][x[1]].value, r)))

        if total_mess == 0 and babies_in_order:
            #//TODO: Finish simulation
            self.running = False
            self.succeded = True

        mess_up(self.house, free_babies)
        n, m = get_length(self.house)
        if total_mess * 100 // (n * m) >= 60:
            #//TODO: Fire up robot
            self.running = False

    def change(self):
        while self.running or self.time < 100:
            #//TODO: Move robot
            if self.time % self.t == 0:
                self.variate_env()
            self.time += 1

        #//TODO: Clarify this mean
        mess_mean = 0
        return (self.succeded, mess_mean)


    def __str__(self):
        h = list()
        for r in self.house:
            h.append(' '.join([str(c) for c in r]))
        return '\n'.join(h)
