#!/bin/bash

#$ -l h_vmem=15G          # Uequest 4GB of UAM
#$ -cwd                   # Uun in the current working directory
#$ -l h_rt=48:00:00       # Set a runtime limit of 47 hours
#$ -N Nov2_MuSiC_Moufarrej # Name the job nuSVU-Decon
#$ -m ae
#$ -M s2556897@ed.ac.uk

# Load the Python environment (adjust if using a virtual environment or module system)
source /etc/profile.d/modules.sh
module load anaconda
conda activate music-apr

# Define directories
BASE_DIR="TOO-Decon-Published"
ref="TOO-Matrix/TOO-Matrices_MuSiC/20250405_GeneID_LessTissueV2_2Median-withGTFNames.tsv"
RESULTS_DIR1="${BASE_DIR}/Moufarrej_Pre-Eclampsia/Decon-Results_Moufarrej_Pre-Eclampsia_SpecificSample"
RESULTS_DIR2="${BASE_DIR}/Moufarrej_Pre-Eclampsia/Decon-Results_Moufarrej_SeverePre-Eclampsia_SpecificSample"
RESULTS_DIR3="${BASE_DIR}/Moufarrej_Pre-Eclampsia/Decon-Results_Moufarrej_Normotensive_SpecificSample/"
MIXTURE1="${BASE_DIR}/Moufarrej_Pre-Eclampsia/GSE192902_Pre-eclampsia_preQC_filtered_counts_UniquePatient_SpecificSample.txt"
MIXTURE2="${BASE_DIR}/Moufarrej_Pre-Eclampsia/GSE192902_SeverePre-eclampsia_preQC_filtered_counts_UniquePatient_SpecificSample.txt"
MIXTURE3="${BASE_DIR}/Moufarrej_Pre-Eclampsia/GSE192902_Normotensive_preQC_filtered_counts_UniquePatient_SpecificSample.txt"

echo "Running MuSiC with:"
echo "  Reference: $ref"

# Create output filename based on reference basename
REF_NAME=$(basename "$ref" .tsv)  # Remove .tsv
OUTPUT_FILE1="${RESULTS_DIR1}/${REF_NAME}_MuSiC_proportions.txt"
OUTPUT_FILE2="${RESULTS_DIR2}/${REF_NAME}_MuSiC_proportions.txt"
OUTPUT_FILE3="${RESULTS_DIR3}/${REF_NAME}_MuSiC_proportions.txt"

# Run the R scripts
Rscript TOO-Decon-Published/Moufarrej_Pre-Eclampsia/01_MuSiC_A_Run.R "$ref" "$MIXTURE1" "$OUTPUT_FILE1"
Rscript TOO-Decon-Published/Moufarrej_Pre-Eclampsia/01_MuSiC_A_Run.R "$ref" "$MIXTURE2" "$OUTPUT_FILE2"
Rscript TOO-Decon-Published/Moufarrej_Pre-Eclampsia/01_MuSiC_A_Run.R "$ref" "$MIXTURE3" "$OUTPUT_FILE3"

