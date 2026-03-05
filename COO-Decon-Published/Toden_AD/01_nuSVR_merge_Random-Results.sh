#!/bin/bash

# Columns to remove (case-sensitive)
DROP_COLS=("nuValue" "CValue" "RMSE-PredictedCounts" "RMSE-Composition")

# Loop through only *_nuSVR directories
for dir in *_nuSVR; do
    [[ -d "$dir" ]] || continue

    echo "Processing $dir..."

    # Map source directory to target directory
    case "$dir" in
        "Decon-COO-Results_Toden_AD_nuSVR")
            target_dir="TSP-BDa_Outer_300_1500_10-Toden-AD"
            ;;
        "Decon-COO-Results_Toden_NCI_nuSVR")
            target_dir="TSP-BDa_Outer_300_1500_10-Toden-NCI"
            ;;
        *)
            target_dir="${dir%_nuSVR}"  # fallback: strip _nuSVR
            ;;
    esac

    # Ensure the target directory exists
    mkdir -p "$target_dir"

    # Base name for output file (strip everything before last '/')
    base_name=$(basename "$target_dir")
    out_file="${target_dir}/nuSVR_Counts_${base_name}.txt"

    first_file=true
    tmp_combined="${dir}/tmp_combined.txt"

    > "$tmp_combined"  # Empty temp file

    # Loop through input files in nuSVR directory
    for file in "$dir"/nuSVR_CountsRMSE_Random*.txt; do
        [[ -e "$file" ]] || continue  # Skip if no files

        # Get header and filter out DROP_COLS
        header=$(head -n 1 "$file")
        IFS=$'\t' read -r -a header_cols <<< "$header"

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
            (for i in "${keep_indices[@]}"; do echo -ne "${header_cols[$i]}\t"; done; echo) \
                | sed 's/\t$//' > "$out_file"
            first_file=false
        fi

        # Append data rows
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
    rm "$tmp_combined"
done

# Final cleanup: remove stray backslashes at end of last column
for file in */nuSVR_Counts_*.txt; do
  echo "Cleaning $file ..."
  awk 'BEGIN {OFS="\t"} {sub(/\\$/, "", $NF); print}' "$file" > "$file.tmp" && mv "$file.tmp" "$file"
done
