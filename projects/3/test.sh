#!/bin/bash
for i in "0.1" "0.2" "0.3" "0.4" "0.5" "0.6" "0.7" "0.8" "0.9" "1.0"; do
  for j in "0.1" "0.2" "0.3" "0.4" "0.5" "0.6" "0.7" "0.8" "0.9" "1.0"; do
    echo "e = $i, l = $j";
    python gridworld.py -a q -k 50 -n 0 -g BridgeGrid -q -w 100 -e $i -l $j;
    python gridworld.py -a q -k 50 -n 0 -g BridgeGrid -q -w 100 -e $i -l $j;
  done
done
