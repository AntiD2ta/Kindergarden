from src.shared.string import OBSTACLE
from .robot import Robot
from .utils import count_free_babies, group_target, paths_to_target
from ..shared import count_dirt, get_length, BABY, OBSTACLE, DIRT
from ..logging import LoggerFactory as Logger


log = Logger('Kindergarden').getChild('Practical')


#Modes:
#cautious: Hay mucho indice de suciedad, recoger basura es la prioridad, si es factible
#recoger un bebe, hacerlo, seguir hasta volverse atrevido. Planear cual es la mejor forma
# de ejecutar las tareas
#
#dared: Hay poco indice de suciedad, concentrarse en recoger ninnos, siempre terminar la tarea.
#Chequear si se cambia de modo solamente en el cambio de ambiente

#beliefs

class Practical(Robot):
    '''
    Practical reasoning agent. Model-based and goal-based reflex agent
    '''
    def __init__(self, pos, t):
        self.time = 0
        self.goal = None
        self.dirt_count = 0
        self.babies = 0
        self.t = t
        super().__init__(pos)

    def action(self, house):
        beliefs   = self.get_beliefs(house)
        options   = self.get_options(beliefs)
        operation = self.filter_options(options)
        self.execute(operation)

    def get_beliefs(self, house):
        '''
        Get state of the environment detected by the agent given the latest perception
        '''
        beliefs = dict()
        self.dirt_count = count_dirt(house)
        self.babies = count_free_babies(house)
        n, m = get_length(house)
        beliefs['mess'] = self.dirt_count * 100 // (n * m)
        beliefs['dirt_groups'] = group_target(house, DIRT, self.t // 2)
        beliefs['baby_groups'] = group_target(house, BABY, 2)

        paths_to_babies = set()
        paths_to_dirt = set()
        paths_to_target(house, self.pos, BABY, {self.pos}, dict(), [OBSTACLE], paths_to_babies)
        paths_to_target(house, self.pos, DIRT, {self.pos}, dict(), [OBSTACLE, BABY], paths_to_dirt)

        dirt_in_path_to_babies = list()
        for p in paths_to_babies:
            dirt = 0
            for (i, j) in p:
                dirt += 1 if house[i][j].value == DIRT else 0
            dirt_in_path_to_babies.append(dirt)
        beliefs['dirt_in_path_to_babies'] = dirt_in_path_to_babies

        beliefs['path_to_babies'] = paths_to_babies
        beliefs['paths_to_dirt'] = paths_to_dirt
        beliefs['cur_cell_value'] = house[self.pos[0]][self.pos[1]].value
        return beliefs

    def get_options(self, beliefs):
        '''
        Get options(plans) available for the agent given its actual beliefs and its intentions
        '''
        options = beliefs

        #Get best path to garbage
        considering = list()
        for p in options['path_to_dirt']:
            for g in options['dirt_groups']:
                if p[-1] in g:
                    #(length of path, concentration of dirt, path)
                    considering.append((len(p), len(g), p))
                    break
        considering.sort()
        log.debug(f'Best paths to dirt: {considering}')
        options['best_path_dirt'] = None if considering == [] else considering[0]

        #Get best path to baby sorted by occurrence of dirt in the path
        considering.clear()
        for p, d in zip(options['path_to_babies'], options['dirt_in_path_to_babies']):
            #(length of path, number of dirt in path, path)
            considering.append((len(p), d, p))
        considering.sort()
        log.debug(f'Best dirty paths to babies: {considering}')
        options['best_dirty_path_babies'] = None if considering == [] else considering[0]

        #Get best path to baby
        considering.clear()
        for p in options['path_to_babies']:
            for g in options['baby_groups']:
                if p[-1] in g:
                    #(length of path, concentration of babies, path)
                    considering.append((len(p), len(g), p))
                    break
        considering.sort()
        log.debug(f'Best paths to babies: {considering}')
        options['best_path_babies'] = None if considering == [] else considering[0]


    def filter_options(self, options):
        '''
        Update intentions and get an action to execute
        '''
        pass

    def execute(self, operation):
        '''
        Execute a action given the planned operation
        '''
        pass

    def __str__(self):
        return 'Practical'
