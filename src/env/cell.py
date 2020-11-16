from .string import EMPTY, CORRAL

class Cell:
    def __init__(self, value=EMPTY):
        self.value   = value
        self.dirty   = False
        self.isFixed = False
    
    def update(self, value, check=[], old=None):
        if self.value in check:
            return False
        if self.value == CORRAL:
            self.value = CORRAL + '-' + value
        else:
            self.value = value
        
        if old:
            if old.isFixed:
                old.update(CORRAL)
            else:
                old.update(EMPTY)
        return True

    def __str__(self):
        return self.value + ''.join([' ' for _ in range(4 - len(self.value))])