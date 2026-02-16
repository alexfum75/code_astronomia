#!/bin/bash

#set -x

#counter=-123.7

for counter in $(seq -131.7 2 -123.7)
do
    new_counter=`echo ${counter/,/.}`
    echo "angle: "$new_counter
    echo  "python ./sim-free-return.py $new_counter 3150 10"
    python ./sim-free-return.py $new_counter 3150 10
done

