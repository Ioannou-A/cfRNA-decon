#!/bin/bash

# Count columns
ncol=$(head -n1 COO-Decon-Published/Moufarrej_Pre-Eclampsia/GSE192902_Normotensive_preQC_filtered_counts_UniquePatient_SpecificSample.txt | awk -F"\t" '{print NF}')

# Decide how many chunks (3)
chunks=3
per_chunk=$(( (ncol-1 + chunks - 1) / chunks ))   # ceil division, excluding "index"

for i in $(seq 1 $chunks); do
    start=$(( (i-1)*per_chunk + 2 ))
    end=$(( i*per_chunk + 1 ))
    if [ $end -gt $ncol ]; then end=$ncol; fi
    echo "Making chunk $i (columns 1 and $start–$end)..."
    cut -f1,$start-$end COO-Decon-Published/Moufarrej_Pre-Eclampsia/GSE192902_Normotensive_preQC_filtered_counts_UniquePatient_SpecificSample.txt > COO-Decon-Published/Moufarrej_Pre-Eclampsia/GSE192902_Normotensive_preQC_filtered_counts_UniquePatient_SpecificSample_part${i}.txt
done
