#!/bin/bash

#$ -l h_vmem=15G          # Uequest 4GB of UAM
#$ -cwd                   # Uun in the current working directory
#$ -l h_rt=48:00:00       # Set a runtime limit of 47 hours
#$ -N Sep1_MuSiC_Chalasani  # Name the job nuSVU-Decon
#$ -m ae
#$ -M s2556897@ed.ac.uk

# Load the Python environment (adjust if using a virtual environment or module system)
source /etc/profile.d/modules.sh
module load anaconda
conda activate music-apr

# Define directories
BASE_DIR="TOO-Decon-Published"
ref="TOO-Matrix/TOO-Matrices_MuSiC/20250405_GeneID_LessTissueV2_2Median-withGTFNames.tsv"
RESULTS_DIR="${BASE_DIR}/Chalasani_Fatty-Liver/Decon-Results_Chalasani_NAFLD"
MIXTURE="${BASE_DIR}/Chalasani_Fatty-Liver/All-NAFLD_Counts_v46_Clean_UniquePatients_CPM.txt"

echo "Running MuSiC with:"
echo "  Reference: $ref"
echo "  Mixture:   $MIXTURE"

# Create output filename based on reference basename
REF_NAME=$(basename "$ref" .tsv)  # Remove .tsv
OUTPUT_FILE="${RESULTS_DIR}/${REF_NAME}_MuSiC_proportions.txt"

# Run the R script
Rscript TOO-Decon-Published/Chalasani_Fatty-Liver/01_MuSiC_A_Run.R "$ref" "$MIXTURE" "$OUTPUT_FILE"

# Define directories
RESULTS_DIR="${BASE_DIR}/Chalasani_Fatty-Liver/Decon-Results_Chalasani_Healthy"
MIXTURE="${BASE_DIR}/Chalasani_Fatty-Liver/All-Healthy_Counts_v46_Clean_UniquePatients_CPM.txt"

echo "Running MuSiC with:"
echo "  Reference: $ref"
echo "  Mixture:   $MIXTURE"

# Create output filename based on reference basename
REF_NAME=$(basename "$ref" .tsv)  # Remove .tsv
OUTPUT_FILE="${RESULTS_DIR}/${REF_NAME}_MuSiC_proportions.txt"

# Run the R script
Rscript TOO-Decon-Published/Chalasani_Fatty-Liver/01_MuSiC_A_Run.R "$ref" "$MIXTURE" "$OUTPUT_FILE"

# Run the R script
Rscript TOO-Decon-Published/Chalasani_Fatty-Liver/01_MuSiC_A_Run.R "$ref" "$MIXTURE" "$OUTPUT_FILE"

# Define directories
RESULTS_DIR="${BASE_DIR}/Chalasani_Fatty-Liver/Decon-Results_Chalasani_NASH"
MIXTURE="${BASE_DIR}/Chalasani_Fatty-Liver/All-NASH_Counts_v46_Clean_UniquePatients_CPM.txt"

echo "Running MuSiC with:"
echo "  Reference: $ref"
echo "  Mixture:   $MIXTURE"

# Create output filename based on reference basename
REF_NAME=$(basename "$ref" .tsv)  # Remove .tsv
OUTPUT_FILE="${RESULTS_DIR}/${REF_NAME}_MuSiC_proportions.txt"

# Run the R script
Rscript TOO-Decon-Published/Chalasani_Fatty-Liver/01_MuSiC_A_Run.R "$ref" "$MIXTURE" "$OUTPUT_FILE"