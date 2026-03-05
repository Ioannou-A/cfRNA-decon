#!/bin/bash

#$ -l h_vmem=30G          # Uequest 4GB of UAM
#$ -cwd                   # Uun in the current working directory
#$ -l h_rt=47:00:00       # Set a runtime limit of 72 hours
#$ -N Aug29_MuSiC_R     # Name the job nuSVU-Decon
#$ -m ae
#$ -M s2556897@ed.ac.uk

# Load the Python environment (adjust if using a virtual environment or module system)
source /etc/profile.d/modules.sh
module load anaconda
conda activate music-apr

# Define directories
MIXTURE_DIR="COO-Decon-Pseudobulks/"
RESULTS_DIR="${MIXTURE_DIR}/Results-Random_v2C"

mkdir -p "$RESULTS_DIR"

# Define mixture file
MIXTURE="${MIXTURE_DIR}/Random_v2C_All-Counts.txt"

# Loop through reference files and their corresponding metadata
for ref in COO-Matrix/TSP*100each_seed42_filtered.txt; do
    # Skip metadata files
    if [[ "$ref" == *metadata* ]]; then
        continue
    fi

    # Construct metadata filename
    meta="${ref/_filtered.txt/_metadata.txt}"

    # Check if metadata exists
    if [[ -f "$meta" ]]; then
        echo "Running MuSiC with:"
        echo "  Reference: $ref"
        echo "  Metadata:  $meta"
        echo "  Mixture:   $MIXTURE"

        # Run the R script
        OUTPUT_FILE="${RESULTS_DIR}/$(basename "$ref" .txt)_Random_v1_prop_weights_MuSiC.txt"
        Rscript COO-Decon-Pseudobulks/01_run_MuSiC-2.R "$ref" "$meta" "$MIXTURE" "$OUTPUT_FILE"
    else
        echo "Metadata not found for $ref"
    fi
done

