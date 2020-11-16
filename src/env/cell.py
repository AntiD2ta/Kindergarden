from ..shared import BABY, DIRT, EMPTY, CORRAL, ROBOT

class Cell:
    def __init__(self, value=EMPTY):
        self.value   = value
        self.dirty   = False
        self.isFixed = False
    
    def update(self, value, check=[], old=None):
        if self.value in check:
            return False

        if self.value == CORRAL:
            self.value = f'{CORRAL}-{value}'
        elif self.value == DIRT and value == f'{ROBOT}-{BABY}':
            self.value = f'{DIRT}-{value}'
        else:
            self.value = value
        
        if old:
            if old.isFixed:
                if BABY in old.value:
                    old.update(f'{CORRAL}-{BABY}')
                old.update(CORRAL)
            elif old.dirty:
                old.update(DIRT)
            else:
                old.update(EMPTY)
        return True

    def __str__(self):
        return self.value + ''.join([' ' for _ in range(4 - len(self.value))])