#!/bin/bash

# Columns to remove (case-sensitive)
DROP_COLS=("nuValue" "CValue" "RMSE-PredictedCounts" "RMSE-Composition")

# Loop through each Decon-COO result dir
for dir in Decon-COO-Results_v3_Noise*_nuSVR/; do
    [[ -d "$dir" ]] || continue
    echo "Processing $dir..."

    # Extract numeric phi value (after "phi")
    raw_noise=$(echo "$dir" | sed -E 's/.*phi([0-9]+(\.[0-9]+)?).*/\1/')

    # Format to 2 decimal places
    noise=$(printf "%.2f" "$raw_noise")

    # Construct matching outer directory
    outer_dir="TSP-BDa_Outer_300_1500_10_Random_v2C-Noisy_phi${raw_noise}_All-Counts"
    [[ -d "$outer_dir" ]] || { echo "Warning: $outer_dir not found, skipping"; continue; }

    # Output file path inside corresponding TSP-BDa_Outer dir
    out_file="${outer_dir}/nuSVR_Counts_${outer_dir}.txt"

    first_file=true
    tmp_combined="${dir}/tmp_combined.txt"
    > "$tmp_combined"

    # Merge nuSVR files
    for file in "$dir"/nuSVR_CountsRMSE_*.txt; do
        [[ -e "$file" ]] || continue

        header=$(head -n 1 "$file")
        IFS=$'\t' read -r -a header_cols <<< "$header"

        keep_indices=()
        for i in "${!header_cols[@]}"; do
            col="${header_cols[$i]}"
            skip=false
            for drop in "${DROP_COLS[@]}"; do
                if [[ "$col" == "$drop" ]]; then
                    skip=true; break
                fi
            done
            $skip || keep_indices+=($i)
        done

        # If first file, write header
        if $first_file; then
            (for i in "${keep_indices[@]}"; do echo -ne "${header_cols[$i]}\t"; done; echo) \
            | sed 's/\t$//' > "$out_file"
            first_file=false
        fi

        # Write filtered rows
        tail -n +2 "$file" | while IFS=$'\t' read -r -a line_cols; do
            line_out=""
            for i in "${keep_indices[@]}"; do
                line_out+="${line_cols[$i]}\t"
            done
            echo -e "${line_out::-1}" >> "$tmp_combined"
        done
    done

    # Deduplicate by sample ID (col1) and append
    awk -F'\t' '!seen[$1]++' "$tmp_combined" >> "$out_file"
    rm "$tmp_combined"

    echo "  -> Output saved to $out_file"
done

# Final cleanup: strip stray trailing backslashes
for file in TSP-BDa_Outer_300_1500_10_Random_v2C-Noisy_phi*/nuSVR_Counts_*.txt; do
    [[ -e "$file" ]] || continue
    echo "Post-processing $file ..."
    awk 'BEGIN {OFS="\t"} {sub(/\\$/, "", $NF); print}' "$file" > "$file.tmp" && mv "$file.tmp" "$file"
done
