from src import Env, LoggerFactory as Logger

LEYEND = '''

Leyend:

R : Robot
B : Baby
C : Corral
# : Obstacule
* : Dirt
- : Empty cell
'''

def main(args, log):
    robot = 'Reagent'
    if args.practical:
        robot = 'Practical'
        #//HACKME:Monkey patch current_agent
        #src.agent.current_agent.func = current_agent


    while True:
        e = Env(args.rows, args.columns, args.dirtiness, args.obstacules, args.babies, args.time, robot)
        log.info('The generated environment is:')
        print(e)
        print(LEYEND)
        print('If this environment ok to you? Insert REPEAT to re-generate, insert anything else to continue')
        s = input()
        if s != 'REPEAT':
            break

    succeded, mess = e.simulate(args.interactive)

    if not succeded and e.running:
        log.info('The time is over, task failed for robot')

    log.info(f'The amount of dirt at the end of this simulation is: {mess}')
    

if __name__ == '__main__':
    import argparse
    import os

    parser = argparse.ArgumentParser(description='Kindergarden simulator')
    parser.add_argument('-r', '--rows', type=int, default=10, help='number of rows of the house')
    parser.add_argument('-c', '--columns', type=int, default=10, help='number of columns of the house')
    parser.add_argument('-d', '--dirtiness', type=int, default=30, help='percentage of dirty cells at the start of the simulation')
    parser.add_argument('-o', '--obstacules', type=int, default=20, help='percentage of obstacules at the start of the simulation')
    parser.add_argument('-b', '--babies', type=int, default=5, help='number of babies in the house')
    parser.add_argument('-t', '--time', type=int, default=5, help='number of turns between changes of the environment')
    parser.add_argument('-p', '--practical', type=bool, const=True, nargs='?', help='set if you want to simulate Practical agent. Reagent agent is default')
    parser.add_argument('-P', '--bernoulli', type=float, default=0.5, help='probability of a baby moving in an environment change (0 to 1)')
    parser.add_argument('-f', '--file', type=bool, const=True, nargs='?', help='set if you want log to a file')
    parser.add_argument('-i', '--interactive', type=bool, const=True, nargs='?', help='set if you want to see what happens in every turn')

    args = parser.parse_args()
    if not os.path.exists('./logs'):
        os.mkdir('./logs/')
    log = Logger(name='Kindergarden', log=args.file)

    log.setLevel(args.level)
    main(args, log)