#!/bin/bash

# Define the input file paths
bulk_files=(
  "COO-Decon-Published/Loy_COVID-MIS-C/GSE225221_cfrna_counts_CPM_GeneNames.txt"
)

# These sc_refs are the same as those for MuSiC but lack the pancreatic pp cell type as it was filtered by the rest of the methods (because it only has 2 cells)
sc_refs=(
  "COO-Matrix/TSP-BDa_Inner_100each_seed42_filtered.txt"
)


# Define the output directory and create it if it doesn't exist
module load anaconda
conda activate bayes

output_dir="COO-Decon-Published/Loy_COVID-MIS-C/Decon-COO-Results_Loy_COVID-MIS-C/"
mkdir -p "$output_dir"

# Loop through all combinations
for bulk in "${bulk_files[@]}"; do
  for sc in "${sc_refs[@]}"; do

    # Extract file base names to construct output filename
    bulk_base=$(basename "$bulk" .txt)
    sc_base=$(basename "$sc" .txt)
    output_file="$output_dir/${sc_base}_${bulk_base}_BayesPrism.txt"

    echo "Running BayesPrism on:"
    echo "  Bulk: $bulk"
    echo "  SC:   $sc"
    echo "  Out:  $output_file"

    Rscript COO-Decon-Published/Loy_COVID-MIS-C/01_BayesPrism_A_Run.R "$bulk" "$sc" "$output_file"

  done
done
