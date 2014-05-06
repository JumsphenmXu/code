#! /bin/bash

while [ -n "$*" ]
    do
        echo $1 $2 $3 $4 $5 $6
        shift
    done


(echo "my name is xuxh"; cd ~)

{ echo "my name is xuxh";}

CRT_DIR=`pwd`
echo ${CRT_DIR}
