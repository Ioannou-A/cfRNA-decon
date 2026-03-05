#!/bin/bash

# Count columns
ncol=$(head -n1 COO-Decon-Published/Chalasani_Fatty-Liver/All-NASH_Counts_v46_Clean_UniquePatients_CPM.txt | awk -F"\t" '{print NF}')

# Decide how many chunks (3)
chunks=3
per_chunk=$(( (ncol-1 + chunks - 1) / chunks ))   # ceil division, excluding "index"

for i in $(seq 1 $chunks); do
    start=$(( (i-1)*per_chunk + 2 ))
    end=$(( i*per_chunk + 1 ))
    if [ $end -gt $ncol ]; then end=$ncol; fi
    echo "Making chunk $i (columns 1 and $start–$end)..."
    cut -f1,$start-$end COO-Decon-Published/Chalasani_Fatty-Liver/All-NASH_Counts_v46_Clean_UniquePatients_CPM.txt > COO-Decon-Published/Chalasani_Fatty-Liver/All-NASH_Counts_v46_Clean_UniquePatients_CPM_part${i}.txt
done
