import json
import os

with open('./results/results.json', 'w+') as f_json:
    with open('./results/results.txt', 'r') as f:
        contents = f.read()
        sets = contents.split('Set')
        sets.pop(0)
        for i, s in enumerate(sets):
            sim_set = dict()
            sim_set['name'] = f'Set {i+1}'
            practical = {
                'fired': 0,
                'done': 0,
                'mess': 0
            }
            reagent = {
                'fired': 0,
                'done': 0,
                'mess': 0
            }
            simulations = s.split('Simulation')
            simulations.pop(0)
            for sim in simulations:
                txt = sim.partition('Final Results: Results')[2].splitlines()

                if 'Practical' in txt[3]:
                    b = eval(txt[3].partition('Task completed by Practical agent: ')[2])
                    if b:
                        practical['done'] += 1
                else:
                    b = eval(txt[3].partition('Task completed by Reagent agent: ')[2])
                    if b:
                        reagent['done'] += 1

                if 'Practical' in txt[4]:
                    b = eval(txt[4].partition('Task completed by Practical agent: ')[2])
                    if b:
                        practical['done'] += 1
                else:
                    b = eval(txt[4].partition('Task completed by Reagent agent: ')[2])
                    if b:
                        reagent['done'] += 1

                if 'Practical' in txt[7]:
                    b = eval(txt[7].partition('Practical agent fired: ')[2])
                    if b:
                        practical['fired'] += 1
                else:
                    b = eval(txt[7].partition('Reagent agent fired: ')[2])
                    if b:
                        reagent['fired'] += 1

                if 'Practical' in txt[8]:
                    b = eval(txt[8].partition('Practical agent fired: ')[2])
                    if b:
                        practical['fired'] += 1
                else:
                    b = eval(txt[8].partition('Reagent agent fired: ')[2])
                    if b:
                        reagent['fired'] += 1

                if 'Practical' in txt[11]:
                    m = eval(txt[11].partition('Percentage of dirt at the end of this simulation of the Practical agent: ')[2])
                    practical['mess'] += m
                else:
                    m = eval(txt[11].partition('Percentage of dirt at the end of this simulation of the Reagent agent: ')[2])
                    reagent['mess'] += m

                if 'Practical' in txt[12]:
                    m = eval(txt[12].partition('Percentage of dirt at the end of this simulation of the Practical agent: ')[2])
                    practical['mess'] += m
                else:
                    m = eval(txt[12].partition('Percentage of dirt at the end of this simulation of the Reagent agent: ')[2])
                    reagent['mess'] += m

            practical['mess'] /= 30
            reagent['mess'] /= 30
            
            sim_set['Practical'] = practical
            sim_set['Reagent'] = reagent

            d = json.dumps(sim_set)
            d += '\n\n'
            f_json.write(d)