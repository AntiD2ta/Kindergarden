from ..shared import BABY, DIRT, EMPTY, CORRAL, ROBOT

class Cell:
    def __init__(self, value=EMPTY):
        self.value   = value
        self.dirty   = False
        self.isFixed = False
    
    def update(self, value, check=[], old=None):
        for v in check:
            if v in self.value:
                return False

        if self.isFixed and value != CORRAL:
            if f'{CORRAL}-{BABY}' in self.value and value != BABY:
                self.value += f'-{ROBOT}'
            else:
                self.value = f'{CORRAL}-{value}'
        elif self.value == DIRT:
            self.value = f'{DIRT}-{value}'
        elif self.value == BABY and value == ROBOT:
            self.value = f'{BABY}-{value}'
        else:
            self.value = value
        
        if old:
            if old.isFixed:
                if BABY in old.value:
                    old.update(BABY)
                else:
                    old.update(CORRAL)
            elif old.dirty:
                old.update(DIRT)
            else:
                old.update(EMPTY)
        return True

    def copy(self):
        new_cell = Cell(self.value)
        new_cell.dirty = self.dirty
        new_cell.isFixed = self.isFixed
        return new_cell

    def __str__(self):
        return self.value + ''.join([' ' for _ in range(5 - len(self.value))])