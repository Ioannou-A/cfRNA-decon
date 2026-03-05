#!/bin/bash

# Define the input file paths
bulk_files=(
  "COO-Decon-Noise/Random_v2C-Noisy_Final3/Random_v2C-Noisy_phi1.0e+00_All-Counts.txt"
  "COO-Decon-Noise/Random_v2C-Noisy_Final3/Random_v2C-Noisy_phi1.0e+01_All-Counts.txt"
  "COO-Decon-Noise/Random_v2C-Noisy_Final3/Random_v2C-Noisy_phi1.0e+02_All-Counts.txt"
  "COO-Decon-Noise/Random_v2C-Noisy_Final3/Random_v2C-Noisy_phi2.0e+00_All-Counts.txt"
  "COO-Decon-Noise/Random_v2C-Noisy_Final3/Random_v2C-Noisy_phi2.0e+01_All-Counts.txt"
  "COO-Decon-Noise/Random_v2C-Noisy_Final3/Random_v2C-Noisy_phi3.0e+00_All-Counts.txt"
  "COO-Decon-Noise/Random_v2C-Noisy_Final3/Random_v2C-Noisy_phi3.0e+01_All-Counts.txt"
  "COO-Decon-Noise/Random_v2C-Noisy_Final3/Random_v2C-Noisy_phi5.0e+00_All-Counts.txt"
  "COO-Decon-Noise/Random_v2C-Noisy_Final3/Random_v2C-Noisy_phi5.0e+01_All-Counts.txt"
)

# These sc_refs are the same as those for MuSiC but lack the pancreatic pp cell type as it was filtered by the rest of the methods (because it only has 2 cells)
sc_refs=(
  "COO-Matrix/TSP-BDa_Inner_100each_seed42_filtered.txt"
)

# Define the output directory and create it if it doesn't exist
module load anaconda
conda activate bayes

output_dir="COO-Decon-Noise/BayesPrism-Deconvolutions"
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
    SECONDS=0
    Rscript COO-Decon-Noise/01_BayesPrism_A_Run.R "$bulk" "$sc" "$output_file"

    duration=$SECONDS
    echo "  → Runtime: $((duration / 60)) min $((duration % 60)) sec"
    echo
  done
done
