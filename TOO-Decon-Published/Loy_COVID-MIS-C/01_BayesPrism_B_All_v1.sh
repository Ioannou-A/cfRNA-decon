#!/bin/bash

# Define the input file paths
bulk_file=(
  "TOO-Decon-Published/Loy_COVID-MIS-C/GSE225221_cfrna_counts_CPM_GeneNames.txt"
)

sc_ref=(
  "TOO-Matrix/TOO-Matrices_Renamed/20250405_GeneID_LessTissueV2_2Median-withGTFNames.tsv"
)

# Define the output directory and create it if it doesn't exist
module load anaconda
conda activate bayes
output_dir="TOO-Decon-Published/Loy_COVID-MIS-C/Decon-Results_Loy_COVID-MIS-C"
mkdir -p "$output_dir"

# Extract file base names to construct output filename
bulk_base=$(basename "$bulk_file" .txt)
sc_base=$(basename "$sc_ref" .tsv)
output_file="$output_dir/${sc_base}_${bulk_base}_BayesPrism.txt"

echo "Running BayesPrism on:"
echo "  Bulk: $bulk_file"
echo "  SC:   $sc_ref"
echo "  Out:  $output_file"

Rscript TOO-Decon-Published/Loy_COVID-MIS-C/01_BayesPrism_A_Run.R "$bulk_file" "$sc_ref" "$output_file"
