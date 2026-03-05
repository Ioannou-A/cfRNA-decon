#!/bin/bash

#$ -l h_vmem=30G          # Request 30GB of RAM
#$ -cwd                   # Run in the current working directory
#$ -l h_rt=47:00:00       # Runtime limit
#$ -N MuSiC_Toden       # Job name
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
MIXTURE_NCI="COO-Decon-Published/Toden_AD/All-NCI_Counts_v46_Clean_UniquePatients_CPM.txt"
MIXTURE_AD="COO-Decon-Published/Toden_AD/All-AD_Counts_v46_Clean_UniquePatients_CPM.txt"

# Output directories
OUTDIR_NCI="COO-Decon-Published/Toden_AD/TSP-BDa_Outer_300_1500_10-Toden-NCI/"
OUTDIR_AD="COO-Decon-Published/Toden_AD/TSP-BDa_Outer_300_1500_10-Toden-AD/"

mkdir -p "$OUTDIR_NCI"
mkdir -p "$OUTDIR_AD"

# Run AD mixture
echo "Running MuSiC on AD mixture..."
OUTPUT_NCI="${OUTDIR_NCI}/TSP-HBA_Inner_100each_seed42_Toden_AD_MuSiC.txt"
Rscript COO-Decon-Published/Toden_AD/01_run_MuSiC-2.R "$REF" "$META" "$MIXTURE_NCI" "$OUTPUT_NCI"

# Run NCI mixture
echo "Running MuSiC on NCI mixture..."
OUTPUT_AD="${OUTDIR_AD}/TSP-HBA_Inner_100each_seed42_Toden_NCI_MuSiC.txt"
Rscript COO-Decon-Published/Toden_AD/01_run_MuSiC-2.R "$REF" "$META" "$MIXTURE_AD" "$OUTPUT_AD"

echo "All runs completed."
