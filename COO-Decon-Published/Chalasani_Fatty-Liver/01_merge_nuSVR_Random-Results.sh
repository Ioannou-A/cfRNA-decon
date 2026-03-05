#!/bin/bash
set -euo pipefail

# Columns to remove (case-sensitive)
DROP_COLS=("nuValue" "CValue" "RMSE-PredictedCounts" "RMSE-Composition")

echo "Starting merge for Chalasani cohorts..."
echo

# Loop through only the three nuSVR directories
for dir in Decon-COO-Results_Chalasani_*_nuSVR; do
    [[ -d "$dir" ]] || continue

    # Extract cohort name (Healthy, NAFLD, NASH)
    cohort=$(echo "$dir" | sed -E 's/.*Chalasani_([A-Za-z0-9]+)_nuSVR/\1/')
    target_dir="TSP-BDa_Outer_300_1500_10-Chalasani_${cohort}"

    mkdir -p "$target_dir"

    out_file="${target_dir}/nuSVR_Counts_${target_dir##*/}.txt"
    tmp_combined="${dir}/tmp_combined.txt"
    first_file=true

    echo "Processing cohort: $cohort"
    echo "   ➜ Input:  $dir"
    echo "   ➜ Output: $out_file"
    > "$tmp_combined"

    # Loop through files
    for file in "$dir"/nuSVR_CountsRMSE_Random*.txt; do
        [[ -e "$file" ]] || continue

        header=$(head -n 1 "$file")
        IFS=$'\t' read -r -a header_cols <<< "$header"

        # Find columns to keep
        keep_indices=()
        for i in "${!header_cols[@]}"; do
            col="${header_cols[$i]}"
            skip=false
            for drop in "${DROP_COLS[@]}"; do
                if [[ "$col" == "$drop" ]]; then
                    skip=true
                    break
                fi
            done
            $skip || keep_indices+=("$i")
        done

        # Write header once
        if $first_file; then
            (for i in "${keep_indices[@]}"; do echo -ne "${header_cols[$i]}\t"; done; echo) \
                | sed 's/\t$//' > "$out_file"
            first_file=false
        fi

        # Append filtered data
        tail -n +2 "$file" | while IFS=$'\t' read -r -a line_cols; do
            line_out=""
            for i in "${keep_indices[@]}"; do
                line_out+="${line_cols[$i]}\t"
            done
            echo -e "${line_out::-1}" >> "$tmp_combined"
        done
    done

    # Deduplicate by sample name (first column)
    awk -F'\t' '!seen[$1]++' "$tmp_combined" >> "$out_file"
    rm -f "$tmp_combined"

    echo "Finished $cohort"
    echo
done

# Final cleanup
echo "🧹 Cleaning stray backslashes..."
for file in TSP-BDa_Outer_300_1500_10-Chalasani_*/nuSVR_Counts_*.txt; do
  [[ -f "$file" ]] || continue
  awk 'BEGIN {OFS="\t"} {sub(/\\$/, "", $NF); print}' "$file" > "$file.tmp" && mv "$file.tmp" "$file"
  echo "Cleaned $file"
done

echo
echo "All cohorts processed successfully!"
