#!/bin/bash

# helper script: take url as positional arg and loop
# until it succeeds or max count is reached
i=0
while [ $i -lt 100 ]; do
    if curl --silent --fail ${1}; then
        break
    else
        echo 'try again';
    fi
    sleep 3
    i=$[$i+1]
done