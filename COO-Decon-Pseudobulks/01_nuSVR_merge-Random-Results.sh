#!/bin/bash

# Columns to remove (case-sensitive)
DROP_COLS=("nuValue" "CValue" "RMSE-PredictedCounts" "RMSE-Composition")

# Loop through each matching directory
for dir in CIBERSORTx-Matrix_*; do
    # Ensure it's a directory
    [[ -d "$dir" ]] || continue
    
    echo "Processing $dir..."

    # Remove prefix "CIBERSORTx-Matrix_" from dir name for output file
    base_name="${dir#CIBERSORTx-Matrix_}"
    out_file="nuSVR_Counts_${base_name}_v2C.txt"

    first_file=true
    tmp_combined="${dir}/tmp_combined.txt"

    > "$tmp_combined"  # Empty temp file

    for file in "$dir"/nuSVR_CountsRMSE_Random*.txt; do
        [[ -e "$file" ]] || continue  # Skip if no such file

        # Get header and filter out DROP_COLS
        header=$(head -n 1 "$file")
        IFS=$'\t' read -r -a header_cols <<< "$header"

        # Identify column indices to keep
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
            $skip || keep_indices+=($i)
        done

        # If first file, write filtered header
        if $first_file; then
            (for i in "${keep_indices[@]}"; do echo -ne "${header_cols[$i]}\t"; done; echo) | sed 's/\t$//' > "$out_file"
            first_file=false
        fi

        # Process data lines
        tail -n +2 "$file" | while IFS=$'\t' read -r -a line_cols; do
            line_out=""
            for i in "${keep_indices[@]}"; do
                line_out+="${line_cols[$i]}\t"
            done
            echo -e "${line_out::-1}" >> "$tmp_combined"
        done
    done

    # Remove duplicates by Sample column (assumed to be first column)
    awk -F'\t' '!seen[$1]++' "$tmp_combined" >> "$out_file"
    rm "$tmp_combined"
done

for file in nuSVR_Counts_*_v2C.txt; do
  echo "Processing $file ..."
  awk 'BEGIN {OFS="\t"} {sub(/\\$/, "", $NF); print}' "$file" > "$file.tmp" && mv "$file.tmp" "$file"
done
