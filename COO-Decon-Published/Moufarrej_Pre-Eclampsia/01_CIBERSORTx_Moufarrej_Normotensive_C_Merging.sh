#!/bin/bash

# Base directory
base_dir="COO-Decon-Published/Moufarrej_Pre-Eclampsia"

# Go into base dir
cd "$base_dir" || exit 1

# Define merged output prefix (target directory)
merged_prefix="TSP-BDa_Outer_300_1500_10-Moufarrej_Normotensive"
mkdir -p "$merged_prefix"

# Output file
merged_file="$merged_prefix/CIBERSORTx_Results_Merged.txt"
> "$merged_file"

# Define the input directories to merge
dirs=(
  "TSP-BDa_Outer_300_1500_10-Moufarrej_Normotensive1"
  "TSP-BDa_Outer_300_1500_10-Moufarrej_Normotensive2"
  "TSP-BDa_Outer_300_1500_10-Moufarrej_Normotensive3"
)

# Loop through each directory and append its results
for dir in "${dirs[@]}"; do
    file="$dir/CIBERSORTx_Results.txt"
    if [[ -f "$file" ]]; then
        echo "Adding $file ..."
        if [[ ! -s "$merged_file" ]]; then
            # First file: keep header
            cat "$file" >> "$merged_file"
        else
            # Subsequent files: skip header
            tail -n +2 "$file" >> "$merged_file"
        fi
    else
        echo "Warning: $file not found."
    fi
done

echo "Merged results saved to: $merged_file"
