#!/bin/bash

#$ -l h_vmem=30G          # Request 30GB of RAM
#$ -cwd                   # Run in the current working directory
#$ -l h_rt=80:00:00       # Runtime limit
#$ -N MuSiC_Chalasani       # Job name
#$ -m ae
#$ -M s2556897@ed.ac.uk

# Load environment
source /etc/profile.d/modules.sh
module load anaconda
conda activate music-apr

# Fixed reference and metadata
REF="COO-Matrix/TSP-HBA_Inner_100each_seed42_filtered.txt"
META="COO-Matrix/TSP-HBA_Inner_100each_seed42_metadata.txt"

# Mixture files
MIXTURE_NAFLD="COO-Decon-Published/Chalasani_Fatty-Liver/All-NAFLD_Counts_v46_Clean_UniquePatients_CPM.txt"
MIXTURE_NASH="COO-Decon-Published/Chalasani_Fatty-Liver/All-NASH_Counts_v46_Clean_UniquePatients_CPM.txt"
MIXTURE_HEALTHY="COO-Decon-Published/Chalasani_Fatty-Liver/All-Healthy_Counts_v46_Clean_UniquePatients_CPM.txt"

# Output directories
OUTDIR_NAFLD="COO-Decon-Published/Chalasani_Fatty-Liver/TSP-BDa_Outer_300_1500_10-Chalasani_NAFLD"
OUTDIR_NASH="COO-Decon-Published/Chalasani_Fatty-Liver/TSP-BDa_Outer_300_1500_10-Chalasani_NASH"
OUTDIR_HEALTHY="COO-Decon-Published/Chalasani_Fatty-Liver/TSP-BDa_Outer_300_1500_10-Chalasani_Healthy"

mkdir -p "$OUTDIR_NAFLD"
mkdir -p "$OUTDIR_NASH"
mkdir -p "$OUTDIR_HEALTHY"

# Run NAFLD mixture
echo "Running MuSiC on NAFLD mixture..."
OUTPUT_NAFLD="${OUTDIR_NAFLD}/TSP-HBA_Inner_100each_seed42_Chalasani_NAFLD_MuSiC.txt"
Rscript COO-Decon-Published/Chalasani_Fatty-Liver/01_run_MuSiC-2.R "$REF" "$META" "$MIXTURE_NAFLD" "$OUTPUT_NAFLD"

# Run Healthy mixture
echo "Running MuSiC on Healthy mixture..."
OUTPUT_HEALTHY="${OUTDIR_HEALTHY}/TSP-HBA_Inner_100each_seed42_Chalasani_Healthy_MuSiC.txt"
Rscript COO-Decon-Published/Chalasani_Fatty-Liver/01_run_MuSiC-2.R "$REF" "$META" "$MIXTURE_HEALTHY" "$OUTPUT_HEALTHY"

# Run NASH mixture
echo "Running MuSiC on NASH mixture..."
OUTPUT_NASH="${OUTDIR_NASH}/TSP-HBA_Inner_100each_seed42_Chalasani_NASH_MuSiC.txt"
Rscript COO-Decon-Published/Chalasani_Fatty-Liver/01_run_MuSiC-2.R "$REF" "$META" "$MIXTURE_NASH" "$OUTPUT_NASH"

echo "All runs completed."