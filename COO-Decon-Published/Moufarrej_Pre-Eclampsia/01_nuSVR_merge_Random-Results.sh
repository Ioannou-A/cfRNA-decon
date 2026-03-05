#!/bin/bash

# Columns to remove (case-sensitive)
DROP_COLS=("nuValue" "CValue" "RMSE-PredictedCounts" "RMSE-Composition")

# Define input → target mappings
declare -A DIR_MAP=(
    ["Decon-COO-Results_Moufarrej_Pre-Eclampsia_nuSVR"]="TSP-BDa_Outer_300_1500_10-Moufarrej_Pre-eclampsia"
    ["Decon-COO-Results_Moufarrej_SeverePre-eclampsia_nuSVR"]="TSP-BDa_Outer_300_1500_10-Moufarrej_SeverePre-eclampsia"
    ["Decon-COO-Results_Moufarrej_Normotensive_nuSVR"]="TSP-BDa_Outer_300_1500_10-Moufarrej_Normotensive"
)

for SRC_DIR in "${!DIR_MAP[@]}"; do
    TARGET_DIR="${DIR_MAP[$SRC_DIR]}"

    [[ -d "$SRC_DIR" ]] || { echo "Skipping missing dir: $SRC_DIR"; continue; }

    echo "Processing $SRC_DIR → $TARGET_DIR ..."
    mkdir -p "$TARGET_DIR"

    base_name=$(basename "$TARGET_DIR")
    out_file="${TARGET_DIR}/nuSVR_Counts_${base_name}.txt"
    tmp_combined="${SRC_DIR}/tmp_combined.txt"

    > "$tmp_combined"
    first_file=true

    for file in "$SRC_DIR"/nuSVR_CountsRMSE_Random*.txt; do
        [[ -e "$file" ]] || continue

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

        if $first_file; then
            (for i in "${keep_indices[@]}"; do echo -ne "${header_cols[$i]}\t"; done; echo) \
                | sed 's/\t$//' > "$out_file"
            first_file=false
        fi

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

    # Clean up stray backslashes
    echo "Cleaning $out_file ..."
    awk 'BEGIN {OFS="\t"} {sub(/\\$/, "", $NF); print}' "$out_file" > "$out_file.tmp" && mv "$out_file.tmp" "$out_file"

    echo "Done: $out_file"
done
