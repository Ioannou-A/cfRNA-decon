#!/bin/bash

# Base directory
base_dir="COO-Decon-Degradation"

cd "$base_dir" || exit 1

# Find all dirs that end with _partN
for prefix in $(ls -d TSP-BDa_Outer_300_1500_10_Random_v2C_top_*_percent_removed_part* 2>/dev/null \
    | sed -E 's/_part[0-9]+\/?$//' | sort -u); do

    echo "Processing $prefix ..."

    # Make sure the target dir exists (it won’t by default)
    mkdir -p "$prefix"

    merged_file="$prefix/CIBERSORTx_Results_Merged.txt"
    > "$merged_file"

    # Go through all part directories for this prefix, sorted naturally
    for partdir in $(ls -d ${prefix}_part* | sort -V); do
        file="$partdir/CIBERSORTx_Results.txt"
        if [[ -f "$file" ]]; then
            if [[ ! -s "$merged_file" ]]; then
                # First file: keep header
                cat "$file" >> "$merged_file"
            else
                # Later files: skip header
                tail -n +2 "$file" >> "$merged_file"
            fi
        fi
    done
done