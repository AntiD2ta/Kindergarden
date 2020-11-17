from .robot import Robot


log = None


#Practical reasoning agent. Model-based and goal-based reflex agent
class Practical(Robot):
    def __init__(self, pos, logP):
        global log
        log = logP.getChild('Practical')
        super().__init__(pos)

    def action(self, house):
        pass

    def __str__(self):
        return 'Practical'
        