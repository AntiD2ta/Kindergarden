#!/bin/bash
if [ ! -d ./results ]; then
    mkdir results
    if [ ! -f ./results/results.txt ]; then
        touch ./results/results.txt
    fi
fi

declare -a simulation
#default (easy)
simulation[1]='-s'
#easy, more dirtiness
simulation[2]='-d 45'
#easy, more obstacules
simulation[3]='-o 30'
#easy, more babies and less dirtiness
simulation[4]='-b 8 -d 15'
#normal, time 2
simulation[5]='-t 2 -s'
#normal, time 2 and moving babies with 0.75
simulation[6]='-t 2 -P 0.75'
#normal, time 2, moving babies with 0.75 and dirtiness at 45%
simulation[7]='-t 2 -P 0.75 -d 45'
#hard, time 1
simulation[8]='-t 1 -s'
#hard, time 1 and moving babies with 0.75
simulation[9]='-t 1 -P 0.75'
#hard, time 1, moving babies with 0.75 and dirtiness at 45%
simulation[10]='-t 1 -P 0.75 -d 45'
#hard, time 1
simulation[11]='-t 1 -s'
#hard, time 1 and moving babies with 1
simulation[12]='-t 1 -P 1'
#hard, time 1, moving babies with 1, dirtiness at 10%, obtacules at 10%
simulation[13]='-t 1 -P 1 -d 10 -o 10'
#ultimate hard, time 1, moving babies with 0.5, dirtiness at 40%, obtacules at 20% and 6 babies
simulation[14]='-t 1 -d 40 -b 6'
#ultimate hard, time 1, moving babies with 1, dirtiness at 40%, obtacules at 20% and 6 babies
simulation[15]='-t 1 -P 1 -d 40 -b 6'

for i in {1..12}; do
    printf "Set %d: \n\n" $i >>./results/results.txt
    for j in {1..30}; do
        printf "Simulation %d: \n\n" $j >>./results/results.txt
        echo | python main.py ${simulation[i]} -s >>./results/results.txt
    done
done

python count.py
