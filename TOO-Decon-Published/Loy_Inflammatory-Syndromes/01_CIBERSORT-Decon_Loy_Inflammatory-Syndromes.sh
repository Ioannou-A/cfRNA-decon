#!/bin/bash

# Insert here your credentials of CIBERSORTx generated from https://cibersortx.stanford.edu/
CIBERSORTX_USERNAME="your_email@domain"
CIBERSORTX_TOKEN="your_token_here"

# List of basis paths
input_dir="TOO-Matrix/TOO-Matrices_Renamed/CIBERSORTx-TOO-Matrix_2Median_300_500"
output_dir="TOO-Decon-Published/Loy_Inflammatory-Syndromes/Decon-Results_Loy_Inflammatory-Syndromes"
sig_name="CIBERSORTx_20250405_PhenotypeClass_LessTissueV2_2Median.CIBERSORTx_20250405_GeneID_LessTissueV2_2Median.withGTFNames.txt"

# Define base path
module load singularity/4.1.3

cp TOO-Decon-Published/Loy_Inflammatory-Syndromes/GSE255555_pedInflam_filtered_counts_CPM_GeneNames.txt ${input_dir}

# Run the Docker command for deconvolution
singularity exec -B ${input_dir}:/src/data -B ${output_dir}:/src/outdir fractions_latest.sif /src/CIBERSORTxFractions \
    --username "$CIBERSORTX_USERNAME" --token "$CIBERSORTX_TOKEN" --mixture /src/data/GSE255555_pedInflam_filtered_counts_CPM_GeneNames.txt --sigmatrix /src/data/${sig_name} --verbose TRUE
