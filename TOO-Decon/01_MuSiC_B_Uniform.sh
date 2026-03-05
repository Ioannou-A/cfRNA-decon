#!/bin/bash

#$ -l h_vmem=16G          # Uequest 4GB of UAM
#$ -cwd                   # Uun in the current working directory
#$ -l h_rt=47:00:00       # Set a runtime limit of 47 hours
#$ -N July23_MuSiC_U     # Name the job nuSVU-Decon
#$ -m ae
#$ -M s2556897@ed.ac.uk

# Load the Python environment (adjust if using a virtual environment or module system)
source /etc/profile.d/modules.sh
module load anaconda
conda activate music-apr

# Define directories
BASE_DIR="TOO-Decon"
REF_DIR="TOO-Matrix/TOO-Matrices_MuSiC"
RESULTS_DIR="${BASE_DIR}/MuSiC-Deconvolutions"
MIXTURE="${BASE_DIR}/20250616_All-Tissues-NoDup_Uniform_Simulated_v2_Counts.txt"

mkdir -p "$RESULTS_DIR"

# Loop through each reference file
for ref in "${REF_DIR}"/*LessTissueV2*-withGTFNames.tsv; do
    echo "Running MuSiC with:"
    echo "  Reference: $ref"
    echo "  Mixture:   $MIXTURE"

    # Create output filename based on reference basename
    REF_NAME=$(basename "$ref" .tsv)  # Remove .tsv
    OUTPUT_FILE="${RESULTS_DIR}/${REF_NAME}_Uniform_Simulated_v2_MuSiC_proportions.txt"

    # Run the R script
    Rscript TOO-Decon/01_MuSiC_A_Run.R "$ref" "$MIXTURE" "$OUTPUT_FILE"
done

