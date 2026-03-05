#!/bin/bash

#$ -l h_vmem=15G          # Uequest 4GB of UAM
#$ -cwd                   # Uun in the current working directory
#$ -l h_rt=48:00:00       # Set a runtime limit of 47 hours
#$ -N Jul26_MuSiC_R     
#$ -m ae
#$ -M s2556897@ed.ac.uk

# Load the Python environment 
source /etc/profile.d/modules.sh
module load anaconda
conda activate music-apr

# Define directories
BASE_DIR="TOO-Decon-Degradation"
REF_DIR="TOO-Matrix/TOO-Matrices_MuSiC"
RESULTS_DIR="${BASE_DIR}/MuSiC-Deconvolutions"
MIXTURE_DIR="${BASE_DIR}/Data"

mkdir -p "$RESULTS_DIR"

# List of reference files
REF_FILES=(
  "${REF_DIR}/20250405_GeneID_LessTissueV2_2Median-withGTFNames.tsv"
)

# List of mixture files
MIXTURE_FILES=(
  "${MIXTURE_DIR}/20250616_All-Tissues-NoDup_Random_Simulated_v2_Counts.txt"
  "${MIXTURE_DIR}/20250616_All-Tissues-NoDup_Random_Degradation_top_10_percent_removed.txt"
  "${MIXTURE_DIR}/20250616_All-Tissues-NoDup_Random_Degradation_top_20_percent_removed.txt"
  "${MIXTURE_DIR}/20250616_All-Tissues-NoDup_Random_Degradation_top_30_percent_removed.txt"
  "${MIXTURE_DIR}/20250616_All-Tissues-NoDup_Random_Degradation_top_40_percent_removed.txt"
)

# Loop through each combination of reference and mixture
for REF in "${REF_FILES[@]}"; do
  for MIX in "${MIXTURE_FILES[@]}"; do
    echo "Running MuSiC with:"
    echo "  Reference: $REF"
    echo "  Mixture:   $MIX"

    REF_NAME=$(basename "$REF" .tsv)
    MIX_NAME=$(basename "$MIX" .txt)

    OUTPUT_FILE="${RESULTS_DIR}/${REF_NAME}__${MIX_NAME}__MuSiC_proportions.txt"

    # Run the R script
    Rscript ${BASE_DIR}/01_MuSiC_A_Run.R "$REF" "$MIX" "$OUTPUT_FILE"
  done
done


