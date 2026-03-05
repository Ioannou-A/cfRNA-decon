#!/bin/bash

# Base directory (adjust if needed)
base_dir="COO-Decon-Pseudobulks"

# Go into base dir
cd "$base_dir" || exit 1

# Loop over unique prefixes (strip _part* dirs)
for prefix in TSP-BDa_Inner_300_1500_10-Random_v2 \
              TSP-BDa_Inner_1000_3000_10-Random_v2 \
              TSP-BDa_Inner_3000_5000_10-Random_v2 \
              TSP-HBA_Inner_300_1500_10-Random_v2 \
              TSP-HBA_Inner_1000_3000_10-Random_v2 \
              TSP-HBA_Inner_3000_5000_10-Random_v2 \
              TSP-BDa_Outer_300_1500_10-Random_v2 \
              TSP-BDa_Outer_1000_3000_10-Random_v2 \
              TSP-BDa_Outer_3000_5000_10-Random_v2; do

    echo "Processing $prefix ..."

    merged_file="$prefix/CIBERSORTx_Results_Merged.txt"

    # Start fresh
    > "$merged_file"

    # Find part dirs sorted by number
    for partdir in ${prefix}_part*; do
        file="$partdir/CIBERSORTx_Results.txt"
        if [[ -f "$file" ]]; then
            if [[ ! -s "$merged_file" ]]; then
                # First file: keep header
                cat "$file" >> "$merged_file"
            else
                # Other files: skip header
                tail -n +2 "$file" >> "$merged_file"
            fi
        fi
    done
done

