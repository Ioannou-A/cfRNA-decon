#!/bin/bash

# Define the input file paths
bulk_file1="TOO-Decon-Published/Moufarrej_Pre-Eclampsia/GSE192902_Pre-eclampsia_preQC_filtered_counts_UniquePatient_SpecificSample.txt"
bulk_file2="TOO-Decon-Published/Moufarrej_Pre-Eclampsia/GSE192902_SeverePre-eclampsia_preQC_filtered_counts_UniquePatient_SpecificSample.txt"
bulk_file3="TOO-Decon-Published/Moufarrej_Pre-Eclampsia/GSE192902_Normotensive_preQC_filtered_counts_UniquePatient_SpecificSample.txt"

sc_ref=(
  "TOO-Matrix/TOO-Matrices_Renamed/20250405_GeneID_LessTissueV2_2Median-withGTFNames.tsv"
)

# Define the output directory and create it if it doesn't exist
module load anaconda
conda activate bayes
output_dir1="TOO-Decon-Published/Moufarrej_Pre-Eclampsia/Decon-Results_Moufarrej_Pre-Eclampsia_SpecificSample"
output_dir2="TOO-Decon-Published/Moufarrej_Pre-Eclampsia/Decon-Results_Moufarrej_SeverePre-Eclampsia_SpecificSample"
output_dir3="TOO-Decon-Published/Moufarrej_Pre-Eclampsia/Decon-Results_Moufarrej_Normotensive_SpecificSample"
mkdir -p "$output_dir1"
mkdir -p "$output_dir2"
mkdir -p "$output_dir3"

# Extract file base names to construct output filename
bulk_base1=$(basename "$bulk_file1" .txt)
bulk_base2=$(basename "$bulk_file2" .txt)
bulk_base3=$(basename "$bulk_file3" .txt)

sc_base=$(basename "$sc_ref" .tsv)
output_file1="$output_dir1/${sc_base}_${bulk_base1}_BayesPrism.txt"
output_file2="$output_dir2/${sc_base}_${bulk_base2}_BayesPrism.txt"
output_file3="$output_dir3/${sc_base}_${bulk_base3}_BayesPrism.txt"

echo "Running BayesPrism on:"
echo "  Bulk: $bulk_file1"
echo "  SC:   $sc_ref"
echo "  Out:  $output_file1"

Rscript TOO-Decon-Published/Moufarrej_Pre-Eclampsia/01_BayesPrism_A_Run.R "$bulk_file1" "$sc_ref" "$output_file1"

echo "Running BayesPrism on:"
echo "  Bulk: $bulk_file2"
echo "  SC:   $sc_ref"
echo "  Out:  $output_file2"

Rscript TOO-Decon-Published/Moufarrej_Pre-Eclampsia/01_BayesPrism_A_Run.R "$bulk_file2" "$sc_ref" "$output_file2"

echo "Running BayesPrism on:"
echo "  Bulk: $bulk_file3"
echo "  SC:   $sc_ref"
echo "  Out:  $output_file3"

Rscript TOO-Decon-Published/Moufarrej_Pre-Eclampsia/01_BayesPrism_A_Run.R "$bulk_file3" "$sc_ref" "$output_file3"