#!/bin/bash

# Insert here your credentials of CIBERSORTx generated from https://cibersortx.stanford.edu/
CIBERSORTX_USERNAME="your_email@domain"
CIBERSORTX_TOKEN="your_token_here"

# List of basis paths
input_dir="TOO-Matrix/TOO-Matrices_Renamed/CIBERSORTx-TOO-Matrix_2Median_300_500"
output_dir="TOO-Decon-Published/Moufarrej_Pre-Eclampsia/Decon-Results_Moufarrej_Normotensive_SpecificSample"
sig_name="CIBERSORTx_20250405_PhenotypeClass_LessTissueV2_2Median.CIBERSORTx_20250405_GeneID_LessTissueV2_2Median.withGTFNames.txt"

# Define base path
module load singularity/4.1.3

cp TOO-Decon-Published/Moufarrej_Pre-Eclampsia/GSE192902_Normotensive_preQC_filtered_counts_UniquePatient_SpecificSample.txt ${input_dir}

# Run the Docker command for deconvolution
singularity exec -B ${input_dir}:/src/data -B ${output_dir}:/src/outdir fractions_latest.sif /src/CIBERSORTxFractions \
    --username "$CIBERSORTX_USERNAME" --token "$CIBERSORTX_TOKEN" --mixture /src/data/GSE192902_Normotensive_preQC_filtered_counts_UniquePatient_SpecificSample.txt --sigmatrix /src/data/${sig_name} --verbose TRUE
