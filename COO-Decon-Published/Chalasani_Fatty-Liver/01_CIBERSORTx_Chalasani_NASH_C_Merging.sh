#!/bin/bash

# Base directory
base_dir="COO-Decon-Published/Chalasani_Fatty-Liver"

# Go into base dir
cd "$base_dir" || exit 1

# Define merged output prefix (target directory)
merged_prefix="TSP-BDa_Outer_300_1500_10-Chalasani_NASH"
mkdir -p "$merged_prefix"

# Output file
merged_file="$merged_prefix/CIBERSORTx_Results_Merged.txt"
> "$merged_file"

# Define the input directories to merge
dirs=(
  "TSP-BDa_Outer_300_1500_10-Chalasani_NASH-01"
  "TSP-BDa_Outer_300_1500_10-Chalasani_NASH-02"
  "TSP-BDa_Outer_300_1500_10-Chalasani_NASH-03"
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
