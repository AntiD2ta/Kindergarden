#!/bin/bash
if [ ! -d ./results ]; then
    mkdir results
    if [ ! -f ./results/results.txt ]; then
        touch ./results/results.txt
    else
        rm ./results/results.txt
        touch ./results/results.txt
    fi
fi

declare -a simulation
#default (easy)
simulation[1]=''
#easy, t = 6, more dirtiness
simulation[2]='-t 6 -d 45'
#easy, t = 6, more obstacules
simulation[3]='-t 6 -o 30'
#easy, t = 6,more babies and less dirtiness
simulation[4]='-t 6 -b 8 -d 15'
#normal, t = 4
simulation[5]='-t 4'
#normal, t = 4 and moving babies with 0.75
simulation[6]='-t 4 -P 0.75'
#normal, t = 4, moving babies with 0.75 and dirtiness at 45%
simulation[7]='-t 4 -P 0.75 -d 45'
#hard, t = 3
simulation[8]='-t 3'
#hard, t = 2
simulation[9]='-t 2'
#hard, t = 2 and moving babies with 0.75
simulation[10]='-t 2 -P 0.75'
#hard, t = 2, moving babies with 0.75 and dirtiness at 45%
simulation[11]='-t 2 -P 0.75 -d 45'
#hard, t = 2 and moving babies with 1
simulation[12]='-t 2 -P 1'
#hard, t = 2, moving babies with 1, dirtiness at 10%, obtacules at 10%
simulation[13]='-t 2 -P 1 -d 10 -o 10'
#hard, t = 2, moving babies with 0.5, dirtiness at 40%, obtacules at 20% and 6 babies
simulation[14]='-t 2 -d 40 -b 6'
#very hard, t = 2, moving babies with 0.5, dirtiness at 40%, obtacules at 20% and 8 babies
simulation[15]='-t 2 -d 10 -b 8'
#insane, t = 1, moving babies with 1, dirtiness at 40%, obtacules at 20% and 6 babies
simulation[15]='-t 1 -P 1 -d 40 -b 6'

for i in {1..15}; do
    printf "Set %d \n\n" $i
    printf "Set %d: \n\n" $i >>./results/results.txt
    for j in {1..30}; do
        printf "Simulation %d \n" $j
        printf "Simulation %d: \n\n" $j >>./results/results.txt
        echo | python main.py ${simulation[i]} -s -f >>./results/results.txt
    done
done

python count.py
