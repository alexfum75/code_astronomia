#!/bin/bash

#set -x

#counter=-123.7

for counter in $(seq 3145 1 3155)
do
    #new_counter=`echo ${counter/,/.}`
    echo "dv: "$counter
    echo  "python ./sim-free-return.py -110 counter 10"
    python ./sim-free-return.py -123.7 $counter 10
done

