from .robot import Robot
from ..env import ROBOT, DIRT, BABY, CORRAL, OBSTACLE, get_adjacents
from .utils import closest_target, count_free_babies, count_dirt
from ..logging import LoggerFactory as Logger


log = Logger(name="Reagent")


class Reagent(Robot):
    def action(self, house):
        x, y = self.pos

        if self.will_clean:
            self.garbage_collected += 1
            self.will_clean = False
            house[x][y].update(ROBOT)
            house[x][y].dirty = False
            log.info(f'Dirt cleaned in ({x}, {y})')
        elif DIRT in house[x][y].value and not self.carrying_baby:
            self.will_clean = True
            log.info(f'I\'ll clean dirt on ({x}, {y}) in the next turn')
        elif house[x][y].value == BABY:
            self.carrying_baby = True
            house[x][y].update('f{ROBOT}-{BABY}')
            log.info(f'Loaded baby on ({x}, {y})')
        elif house[x][y].value == CORRAL and self.carrying_baby:
            self.carrying_baby = False
            house[x][y].update('f{BABY}-{ROBOT}')
            log.info(f'Dropped baby in corral at({x}, {y})')
        else:
            adj = get_adjacents(house, self.pos)
            if len(adj) == 0:
                log.debug('No valid adyacents cells to robot')
                log.info(f'I can\'t move!!! Waiting for an environment change')
                return
            if self.carrying_baby:
                self.try_move(house, CORRAL, [OBSTACLE, BABY])
            elif count_free_babies(house) > 0:
                self.try_move(house, BABY)
            elif count_dirt(house) > 0:
                self.try_move(house, DIRT)
            else:
                log.info('There is no dirt to clean or babies to carry!!! Waiting for an environment change')

    
    def move(self, house, pos, steps=1):
        if steps == 0:
            return
        cur_cell = house[self.pos[0]][self.pos[1]]
        x, y = pos.pop(0)
        house[x][y].update(cur_cell.value, cur_cell)
        log.info(f'Moved to ({x}, {y})')
        self.move(house, pos, steps - 1)

    def try_move(self, house, target, check=[OBSTACLE]):
        p = closest_target(house, self.pos, target, check)
        if p == []:
            log.debug(f'No path to closest target: {target}')
            log.info(f'I can\'t move!!! Waiting for an environment change')
            return
        if target == BABY:
            self.move(house, self.pos, steps=2)
        else:
            self.move(house, self.pos)

    def __str__(self):
        return 'Reagent'