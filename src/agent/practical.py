from src.shared.string import EMPTY
from .reagent import Reagent
from .utils import closest_target, count_free_babies, group_target, paths_to_target
from ..shared import count_dirt, get_length, ROBOT, DIRT, BABY, CORRAL, OBSTACLE
from ..logging import LoggerFactory as Logger


log = None


CAUTIOUS = 'CAUTIOUS'
DARED    = 'DARED'

class Practical(Reagent):
    '''
    Practical reasoning agent. Model-based and goal-based reflex agent
    '''
    def __init__(self, pos, t):
        global log
        log = Logger('Kindergarden').getChild('Practical')
        self.t = 0
        self.time = 0
        self.babies = 0
        self.mode = ''
        self.drop = False
        self.old_pos = pos
        super().__init__(pos)

    def action(self, house):
        beliefs   = self.get_beliefs(house)
        options   = self.get_options(beliefs)
        operation = self.filter_options(options)
        self.execute(operation, house)

    def get_beliefs(self, house):
        '''
        Get state of the environment detected by the agent given the latest perception
        '''
        beliefs = dict()
        self.time += 1

        #Learn t
        if self.old_pos != self.pos:
            self.t = self.time - self.t
            self.time = 0
        #Top priority intentions
        if self.will_clean or self.carrying_baby:
            return beliefs

        log.info('Updating state of the environment...', 'get_beliefs')
        self.babies = count_free_babies(house)
        n, m = get_length(house)
        beliefs['mess'] = count_dirt(house) * 100 // (n * m)
        beliefs['dirt_groups'] = group_target(house, DIRT, self.t // 2 if self.t > 0 else 10)
        beliefs['baby_groups'] = group_target(house, BABY, 2)

        paths_to_babies = list()
        paths_to_dirt = list()

        max_path = len(closest_target(house, self.pos, DIRT, [OBSTACLE]))
        max_path *= 2
        paths_to_target(house, self.pos, self.pos, DIRT, {self.pos}, dict(), [OBSTACLE, BABY], paths_to_dirt, max_path)

        max_path = len(closest_target(house, self.pos, BABY, [OBSTACLE]))
        max_path += self.t // 2 if self.t > 0 else 5
        paths_to_target(house, self.pos, self.pos, BABY, {self.pos}, dict(), [OBSTACLE], paths_to_babies, max_path)
        # log.debug(f'paths_to_babies: {paths_to_babies}')
        # log.debug(f'paths_to_dirt: {paths_to_dirt}')

        dirt_in_path_to_babies = list()
        for p in paths_to_babies:
            dirt = 0
            for (i, j) in p:
                dirt += 1 if house[i][j].value == DIRT else 0
            dirt_in_path_to_babies.append(dirt)
        beliefs['dirt_in_path_to_babies'] = dirt_in_path_to_babies
        #log.debug(f'dirt_in_path_to_babies: {dirt_in_path_to_babies}')

        beliefs['paths_to_babies'] = paths_to_babies
        beliefs['paths_to_dirt'] = paths_to_dirt
        beliefs['cur_cell_value'] = house[self.pos[0]][self.pos[1]].value
        return beliefs

    def get_options(self, beliefs):
        '''
        Get options(plans) available for the agent given its actual beliefs and its intentions
        '''
        #Top priority intentions
        if self.will_clean or self.carrying_baby:
            return self.options

        options = beliefs

        #Get best path to garbage
        considering = list()
        for p in options['paths_to_dirt']:
            for g in options['dirt_groups']:
                last = list(p)[-1]
                if last in g:
                    #(length of path, concentration of dirt, path)
                    considering.append((len(p), -len(g), p))
                    break
        considering.sort()
        #log.debug(f'Best paths to dirt: {considering}')
        options['best_path_dirt'] = None if considering == [] else list(considering[0][2])

        #Get best path to baby sorted by occurrence of dirt in the path
        considering.clear()
        for p, d in zip(options['paths_to_babies'], options['dirt_in_path_to_babies']):
            #(length of path, number of dirt in path, path)
            considering.append((len(p), -d, p))
        considering.sort()
        #log.debug(f'Best dirty paths to babies: {considering}')
        options['best_dirty_path_babies'] = None if considering == [] else list(considering[0][2])

        #Get best path to baby
        considering.clear()
        for p in options['paths_to_babies']:
            for g in options['baby_groups']:
                last = list(p)[-1]
                if last in g:
                    #(length of path, concentration of babies, path)
                    considering.append((len(p), -len(g), p))
                    break
        considering.sort()
        #log.debug(f'Best paths to babies: {considering}')
        options['best_path_babies'] = None if considering == [] else list(considering[0][2])
        self.options = options
        return options

    def filter_options(self, options):
        '''
        Update intentions and get an action to execute
        '''
        #Top priority intentions
        if self.carrying_baby:
            if self.drop:
                self.mode = CAUTIOUS
                return ('DROP', [])
            return ('GOTO_CORRAL', [])
        if self.will_clean:
            self.garbage_collected += 1
            self.will_clean = False
            return ('CLEAN', [])
        
        #Goal selection
        if options['mess'] >= 40 or self.babies == 0:
            #CAUTIOUS mode
            self.mode = CAUTIOUS
            log.debug(f'Current mode: CAUTIOUS')
            actions = list()
            if options['best_path_dirt']:
                actions.append(options['best_path_dirt'].copy())
                self.options['best_path_dirt'].pop(0)
            if options['best_dirty_path_babies']:
                actions.append(options['best_dirty_path_babies'].copy())
                self.options['best_dirty_path_babies'].pop(0)
            if actions == []:
                return ('BLOCK', [])
            else:
                actions.sort()
                return ('MOVE', actions[0])
        else:
            #DARED mode
            self.mode = DARED
            log.debug(f'Current mode: DARED')
            if options['best_path_babies']:
                opt = options['best_path_babies'].copy()
                self.options['best_path_babies'].pop(0)
                return ('MOVE', opt)
            return ('BLOCK', [])

    def execute(self, operation, house):
        '''
        Execute a action given the planned operation
        '''
        x, y = self.pos
        task, args = operation
        
        if task is 'CLEAN':
            house[x][y].update(ROBOT)
            house[x][y].dirty = False
            log.debug(f'Dirt cleaned in ({x}, {y})', 'CMD: CLEAN')
        elif task is 'GOTO_CORRAL':
            log.debug('Executing task GOTO_CORRAL', 'execute')
            if CORRAL in house[x][y].value and not f'{CORRAL}-{BABY}' in house[x][y].value:
                self.carrying_baby = False
                house[x][y].update(f'{BABY}-{ROBOT}')
                log.debug(f'Dropped baby in corral at ({x}, {y})', 'CMD: GOTO_CORRAL')
            else:
                if not self.try_move(house, CORRAL, [OBSTACLE, BABY]):
                    self.drop = True
        elif task is 'DROP':
            if DIRT in house[x][y].value:
                self.try_move(house, EMPTY, [OBSTACLE, BABY, DIRT])
            self.drop = False
            self.carrying_baby = False
            house[x][y].update(f'{BABY}-{ROBOT}')
            log.debug(f'Dropped baby at ({x}, {y})', 'CMD: DROP')
        else:
            if self.mode is CAUTIOUS:
                self.execute_move(operation, house)
                x, y = self.pos
                if DIRT in house[x][y].value:
                    self.will_clean = True
                    log.debug(f'I\'ll clean dirt on ({x}, {y}) in the next turn', 'execute')
            elif self.mode is DARED:
                self.execute_move(operation, house)
                x, y = self.pos

            if BABY in house[x][y].value and not house[x][y].isFixed:
                self.carrying_baby = True
                house[x][y].update(f'{ROBOT}-{BABY}')
                log.debug(f'Loaded baby on ({x}, {y})', 'execute')
        
        self.old_pos = self.pos

    def execute_move(self, operation, house):
        task, args = operation
        if task is 'MOVE':
            log.debug('Executing task MOVE', 'execute_move')
            self.move(house, args)
        else:
            log.debug(f'I can\'t move!!! Analyzing options... Meanwhile waiting for an environment change', 'execute_move')
     
    def __str__(self):
        return 'Practical'
