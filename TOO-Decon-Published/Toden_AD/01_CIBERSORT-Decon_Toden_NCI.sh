#!/bin/bash
#$ -l h_vmem=16G              # memory per slot
#$ -l h_rt=47:00:00           # max runtime
#$ -pe sharedmem 2          # request 2 CPU cores
#$ -cwd                       # run in current working dir
#$ -N CIBER_NCI            # job name
#$ -m ae                      # email on abort/end
#$ -M s2556897@ed.ac.uk       # email address

# Insert here your credentials of CIBERSORTx generated from https://cibersortx.stanford.edu/
CIBERSORTX_USERNAME="your_email@domain"
CIBERSORTX_TOKEN="your_token_here"

# List of basis paths
input_dir="TOO-Matrix/TOO-Matrices_Renamed/CIBERSORTx-TOO-Matrix_2Median_300_500"
output_dir="TOO-Decon-Published/Toden_AD/Decon-Results_Toden_NCI"
sig_name="CIBERSORTx_20250405_PhenotypeClass_LessTissueV2_2Median.CIBERSORTx_20250405_GeneID_LessTissueV2_2Median.withGTFNames.txt"

# Define modules
source /etc/profile.d/modules.sh
module load singularity/4.1.3

cp TOO-Decon-Published/Toden_AD/All-NCI_Counts_v46_Clean_UniquePatients_CPM.txt ${input_dir}

# Run the Docker command for deconvolution
singularity exec -B ${input_dir}:/src/data -B ${output_dir}:/src/outdir fractions_latest.sif /src/CIBERSORTxFractions \
    --username "$CIBERSORTX_USERNAME" --token "$CIBERSORTX_TOKEN" --mixture /src/data/All-NCI_Counts_v46_Clean_UniquePatients_CPM.txt --sigmatrix /src/data/${sig_name} --verbose TRUE
