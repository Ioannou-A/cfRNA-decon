#!/bin/bash

# Number of chunks
chunks=11

# Loop over all matching files
for file in Data/Random_v2C_top*_percent_removed.txt; do
    echo "Processing $file"

    # Count columns
    ncol=$(head -n1 "$file" | awk -F"\t" '{print NF}')

    # ceil division, excluding "index" column
    per_chunk=$(( (ncol-1 + chunks - 1) / chunks ))

    for i in $(seq 1 $chunks); do
        start=$(( (i-1)*per_chunk + 2 ))
        end=$(( i*per_chunk + 1 ))
        if [ $end -gt $ncol ]; then end=$ncol; fi

        # keep output in same directory
        out="${file%.txt}_part${i}.txt"
        echo "  Making chunk $i → $out (columns 1 and $start–$end)..."
        cut -f1,$start-$end "$file" > "$out"
    done
done
