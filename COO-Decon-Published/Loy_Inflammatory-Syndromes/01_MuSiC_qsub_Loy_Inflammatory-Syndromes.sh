#!/bin/bash

#$ -l h_vmem=30G          # Request 30GB of RAM
#$ -cwd                   # Run in the current working directory
#$ -l h_rt=47:00:00       # Runtime limit
#$ -N MuSiC_Loy     # Job name
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
MIXTURE="COO-Decon-Published/Loy_Inflammatory-Syndromes/GSE255555_pedInflam_filtered_counts_CPM_GeneNames.txt"

# Output directories
OUTDIR="COO-Decon-Published/Loy_Inflammatory-Syndromes/Decon-COO-Results_Loy_Inflammatory-Syndromes"

mkdir -p "$OUTDIR"

# Run mixture
echo "Running MuSiC on Loy mixture..."
OUTPUT="${OUTDIR}/TSP-HBA_Inner_100each_seed42_Loy_Inflammatory-Syndromes_MuSiC.txt"
Rscript COO-Decon-Published/Loy_Inflammatory-Syndromes/01_run_MuSiC-2.R "$REF" "$META" "$MIXTURE" "$OUTPUT"

echo "All runs completed."
