from .robot import Robot
from ..shared import ROBOT, DIRT, BABY, CORRAL, OBSTACLE, get_adjacents, count_dirt
from .utils import closest_target, count_free_babies
from ..logging import LoggerFactory as Logger


log = Logger('Kindergarden').getChild('Reagent')


class Reagent(Robot):
    '''
    Reagent agent. Simple reflex agent
    '''
    def action(self, house):
        x, y = self.pos

        if self.will_clean:
            self.garbage_collected += 1
            self.will_clean = False
            house[x][y].update(ROBOT)
            house[x][y].dirty = False
            log.debug(f'Dirt cleaned in ({x}, {y})', 'action')
        elif DIRT in house[x][y].value and not self.carrying_baby:
            self.will_clean = True
            log.debug(f'I\'ll clean dirt on ({x}, {y}) in the next turn', 'action')
        elif not self.carrying_baby and BABY in house[x][y].value and not house[x][y].isFixed:
            self.carrying_baby = True
            house[x][y].update(f'{ROBOT}-{BABY}')
            log.debug(f'Loaded baby on ({x}, {y})')
        elif self.carrying_baby and CORRAL in house[x][y].value and not f'{CORRAL}-{BABY}' in house[x][y].value:
            self.carrying_baby = False
            house[x][y].update(f'{BABY}-{ROBOT}')
            log.debug(f'Dropped baby in corral at ({x}, {y})', 'action')
        else:
            adj = get_adjacents(house, self.pos)
            if len(adj) == 0:
                log.debug('No valid adyacents cells to robot', 'action')
                log.debug(f'I can\'t move!!! Waiting for an environment change', 'action')
                return
            if self.carrying_baby:
                self.try_move(house, CORRAL, [OBSTACLE, BABY])
            elif count_free_babies(house) > 0:
                self.try_move(house, BABY)
            elif count_dirt(house) > 0:
                self.try_move(house, DIRT)
            else:
                log.debug('There is no dirt to clean or babies to carry!!! Waiting for an environment change', 'action')
    
    def move(self, house, pos, steps=1):
        if steps == 0 or pos == []:
            return
        cur_cell = house[self.pos[0]][self.pos[1]]
        x, y = pos.pop(0)
        if self.carrying_baby:
            value = f'{ROBOT}-{BABY}'
        else:
            value = ROBOT
        house[x][y].update(value, old=cur_cell)
        self.pos = (x, y)
        log.debug(f'Moved to ({x}, {y})', 'move')
        self.move(house, pos, steps - 1)

    def try_move(self, house, target, check=[OBSTACLE]):
        p = closest_target(house, self.pos, target, check)
        #log.debug(f'p: {p}', 'try_move')
        if p == []:
            log.debug(f'No path to closest target: {target}', 'try_move')
            log.debug(f'I can\'t move!!! Waiting for an environment change', 'try_move')
            return
        if target == CORRAL:
            self.move(house, p, steps=2)
        else:
            self.move(house, p)

    def __str__(self):
        return 'Reagent'