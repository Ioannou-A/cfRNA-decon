#!/bin/bash

# Base directory
base_dir="COO-Decon-Noise"

# Go into base dir
cd "$base_dir" || exit 1

# Detect all unique prefixes (strip _part* dirs)
for prefix in $(ls -d TSP-BDa_*Noisy_phi*_All-Counts_part* 2>/dev/null | sed -E 's/_part[0-9]+\/?$//' | sort -u); do

    # Extract the scientific phi part (e.g. 5.0e+00)
    phi_sci=$(echo "$prefix" | sed -E 's/.*_phi([0-9.eE+-]+)_All-Counts.*/\1/')

    # Convert scientific phi to normal form (e.g. 5.0e+00 → 5, 1.0e+01 → 10)
    phi_norm=$(awk -v val="$phi_sci" 'BEGIN{printf "%g", val}')

    # Build the output directory name (replace sci notation with normal)
    out_prefix=$(echo "$prefix" | sed -E "s/_phi[0-9.eE+-]+_/_phi${phi_norm}_/")

    echo "Merging parts for φ=$phi_sci → $phi_norm ..."
    mkdir -p "$out_prefix"

    merged_file="$out_prefix/CIBERSORTx_Results_Merged.txt"
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