#!/bin/bash

#$ -l h_vmem=30G          # Uequest 4GB of UAM
#$ -cwd                   # Uun in the current working directory
#$ -l h_rt=47:00:00       # Set a runtime limit of 72 hours
#$ -N Oct5_MuSiC     # Name the job nuSVU-Decon
#$ -m ae
#$ -M s2556897@ed.ac.uk

# Load the Python environment (adjust if using a virtual environment or module system)
source /etc/profile.d/modules.sh
module load anaconda
conda activate music-apr

# Base directory
BASE_DIR="COO-Decon-Degradation"

# Directories
REF_FILE="COO-Matrix/TSP-HBA_Inner_100each_seed42_filtered.txt"
META_FILE="COO-Matrix/TSP-HBA_Inner_100each_seed42_metadata.txt"
MIXTURE_DIR="${BASE_DIR}/Data"
RESULTS_DIR="${BASE_DIR}/MuSiC-Deconvolution-Degradation_v4"

mkdir -p "$RESULTS_DIR"

# Loop through all mixture files
for MIXTURE in "${MIXTURE_DIR}"/Random_v2C_top_*_percent_removed.txt; do
    echo "Running MuSiC with:"
    echo "  Reference: $REF_FILE"
    echo "  Metadata:  $META_FILE"
    echo "  Mixture:   $MIXTURE"

    # Output file name: Reference base + mixture base
    REF_BASE=$(basename "$REF_FILE" .txt)
    MIX_BASE=$(basename "$MIXTURE" .txt)
    OUTPUT_FILE="${RESULTS_DIR}/${REF_BASE}_${MIX_BASE}_prop_weights_MuSiC.txt"

    # Run the R script
    Rscript COO-Decon-Degradation/01_run_MuSiC-2.R "$REF_FILE" "$META_FILE" "$MIXTURE" "$OUTPUT_FILE"
done

