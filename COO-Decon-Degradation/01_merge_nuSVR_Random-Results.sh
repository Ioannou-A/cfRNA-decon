#!/bin/bash
set -euo pipefail

# Columns to remove (case-sensitive)
DROP_COLS=("nuValue" "CValue" "RMSE-PredictedCounts" "RMSE-Composition")

echo "Starting merge for degradation datasets..."
echo

# Loop through all nuSVR degradation directories
for src_dir in Decon-COO-Results_Degradation_v4_top_*_percent_removed_nuSVR; do
    [[ -d "$src_dir" ]] || continue

    # Extract the percent part (10, 20, 30, 40)
    percent=$(echo "$src_dir" | sed -E 's/.*top_([0-9]+)_percent_removed.*/\1/')
    target_dir="TSP-BDa_Outer_300_1500_10_Random_v2C_top_${percent}_percent_removed"

    mkdir -p "$target_dir"

    base_name=$(basename "$target_dir")
    out_file="${target_dir}/nuSVR_Counts_${base_name}.txt"
    tmp_combined="${src_dir}/tmp_combined.txt"
    first_file=true

    echo "Processing: $src_dir"
    echo "   ➜ Output: $out_file"
    > "$tmp_combined"

    # Merge all matching files
    for file in "$src_dir"/nuSVR_CountsRMSE_Random*.txt; do
        [[ -e "$file" ]] || continue

        header=$(head -n 1 "$file")
        IFS=$'\t' read -r -a header_cols <<< "$header"

        # Find which columns to keep
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

        # Append filtered rows
        tail -n +2 "$file" | while IFS=$'\t' read -r -a line_cols; do
            line_out=""
            for i in "${keep_indices[@]}"; do
                line_out+="${line_cols[$i]}\t"
            done
            echo -e "${line_out::-1}" >> "$tmp_combined"
        done
    done

    # Deduplicate by first column (Sample)
    awk -F'\t' '!seen[$1]++' "$tmp_combined" >> "$out_file"
    rm -f "$tmp_combined"

    echo "Finished: $target_dir"
    echo
done

# Final cleanup of trailing backslashes
echo "🧹 Cleaning stray backslashes..."
for file in TSP-BDa_Outer_300_1500_10_Random_v2C_top_*_percent_removed/nuSVR_Counts_*.txt; do
  [[ -f "$file" ]] || continue
  awk 'BEGIN {OFS="\t"} {sub(/\\$/, "", $NF); print}' "$file" > "$file.tmp" && mv "$file.tmp" "$file"
  echo "Cleaned $file"
done

echo
echo "All degradation sets processed successfully!"
