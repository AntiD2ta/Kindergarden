from .robot import Robot
from ..env import ROBOT, DIRT, BABY, CORRAL, OBSTACLE, get_adjacents
from .utils import closest_target, count_free_babies

class Reagent(Robot):
    def action(self, house):
        x, y = self.pos

        if self.will_clean:
            self.garbage_collected += 1
            self.will_clean = False
            house[x][y].update(ROBOT)
        elif DIRT in house[x][y].value and not self.carrying_baby:
            self.will_clean = True
        elif house[x][y].value == BABY:
            self.carrying_baby = True
            house[x][y].update('f{ROBOT}-{BABY}')
        elif house[x][y].value == CORRAL and self.carrying_baby:
            self.carrying_baby = False
            house[x][y].update('f{BABY}-{ROBOT}')
        else:
            adj = get_adjacents(house, self.pos)
            if len(adj) == 0:
                #Can't move!!!
                return
            if self.carrying_baby:
                self.try_move(house, CORRAL, [OBSTACLE, BABY])
            elif count_free_babies(house) > 0:
                self.try_move(house, BABY)
            else:
                self.try_move(house, DIRT)

    
    def move(self, house, pos, steps=1):
        if steps == 0:
            return
        cur_cell = house[self.pos[0]][self.pos[1]]
        x, y = pos.pop(0)
        house[x][y].update(cur_cell.value, cur_cell)
        self.move(house, pos, steps - 1)

    def try_move(self, house, target, check=[OBSTACLE]):
        p = closest_target(house, self.pos, target, check)
        if p == []:
            #wait, trapped!!
            return
        if target == BABY:
            self.move(house, self.pos, steps=2)
        else:
            self.move(house, self.pos)
