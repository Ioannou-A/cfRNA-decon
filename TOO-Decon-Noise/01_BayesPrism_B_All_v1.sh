#!/bin/bash

# Define the input file paths
bulk_files=(
  "TOO-Decon-Noise/20250616_All-Tissues-NoDup_Noise0.1_Counts.txt"
  "TOO-Decon-Noise/20250616_All-Tissues-NoDup_Noise0.2_Counts.txt"
  "TOO-Decon-Noise/20250616_All-Tissues-NoDup_Noise0.3_Counts.txt"
  "TOO-Decon-Noise/20250616_All-Tissues-NoDup_Noise0.4_Counts.txt"
  "TOO-Decon-Noise/20250616_All-Tissues-NoDup_Noise0.5_Counts.txt"
  "TOO-Decon-Noise/20250616_All-Tissues-NoDup_Noise0.6_Counts.txt"
  "TOO-Decon-Noise/20250616_All-Tissues-NoDup_Noise0.7_Counts.txt"
  "TOO-Decon-Noise/20250616_All-Tissues-NoDup_Noise0.8_Counts.txt"
  "TOO-Decon-Noise/20250616_All-Tissues-NoDup_Noise0.9_Counts.txt"
  "TOO-Decon-Noise/20250616_All-Tissues-NoDup_Noise1.0_Counts.txt"
)


sc_refs=(
  "TOO-Matrix/TOO-Matrices_Renamed/20250405_GeneID_LessTissueV2_2Median-withGTFNames.tsv"
)

# Define the output directory and create it if it doesn't exist
module load anaconda
conda activate bayes
output_dir="TOO-Decon-Noise/BayesPrism-Deconvolutions"
mkdir -p "$output_dir"

# Loop through all combinations
for bulk in "${bulk_files[@]}"; do
  for sc in "${sc_refs[@]}"; do

    # Extract file base names to construct output filename
    bulk_base=$(basename "$bulk" .txt)
    sc_base=$(basename "$sc" .tsv)
    output_file="$output_dir/${sc_base}_${bulk_base}_BayesPrism.txt"

    echo "Running BayesPrism on:"
    echo "  Bulk: $bulk"
    echo "  SC:   $sc"
    echo "  Out:  $output_file"

    Rscript TOO-Decon-Noise/01_BayesPrism_A_Run.R "$bulk" "$sc" "$output_file"
  done
done
