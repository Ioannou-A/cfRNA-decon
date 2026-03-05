#!/bin/bash

#$ -cwd                   # Run in the current working directory
#$ -l h_rt=47:00:00       # Runtime limit
#$ -N MuSiC_Moufarrej       # Job name
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
MIXTURE_PREECLAMPSIA="COO-Decon-Published/Moufarrej_Pre-Eclampsia/GSE192902_Pre-eclampsia_preQC_filtered_counts_UniquePatient_SpecificSample.txt"
MIXTURE_SEVERE="COO-Decon-Published/Moufarrej_Pre-Eclampsia/GSE192902_SeverePre-eclampsia_preQC_filtered_counts_UniquePatient_SpecificSample.txt"
MIXTURE_NORM="COO-Decon-Published/Moufarrej_Pre-Eclampsia/GSE192902_Normotensive_preQC_filtered_counts_UniquePatient_SpecificSample.txt"

# Output directories
OUTDIR_PREECLAMPSIA="COO-Decon-Published/Moufarrej_Pre-Eclampsia/TSP-BDa_Outer_300_1500_10-Moufarrej_Pre-eclampsia"
OUTDIR_SEVERE="COO-Decon-Published/Moufarrej_Pre-Eclampsia/TSP-BDa_Outer_300_1500_10-Moufarrej_SeverePre-eclampsia"
OUTDIR_NORM="COO-Decon-Published/Moufarrej_Pre-Eclampsia/TSP-BDa_Outer_300_1500_10-Moufarrej_Normotensive"

mkdir -p "$OUTDIR_PREECLAMPSIA"
mkdir -p "$OUTDIR_SEVERE"
mkdir -p "$OUTDIR_NORM"

# Run Pre-Eclampsia mixture
echo "Running MuSiC on Pre-Eclampsia mixture..."
OUTPUT_PREECLAMPSIA="${OUTDIR_PREECLAMPSIA}/TSP-HBA_Inner_100each_seed42_Moufarrej_Pre-eclampsia_MuSiC.txt"
Rscript COO-Decon-Published/Moufarrej_Pre-Eclampsia/01_run_MuSiC-2.R "$REF" "$META" "$MIXTURE_PREECLAMPSIA" "$OUTPUT_PREECLAMPSIA"

# Run Severe Pre-Eclampsia mixture
echo "Running MuSiC on Severe Pre-Eclampsia mixture..."
OUTPUT_SEVERE="${OUTDIR_SEVERE}/TSP-HBA_Inner_100each_seed42_Moufarrej_SeverePre-eclampsia_MuSiC.txt"
Rscript COO-Decon-Published/Moufarrej_Pre-Eclampsia/01_run_MuSiC-2.R "$REF" "$META" "$MIXTURE_SEVERE" "$OUTPUT_SEVERE"

# Run Normotensive mixture
echo "Running MuSiC on Severe Pre-Eclampsia mixture..."
OUTPUT_NORM="${OUTDIR_NORM}/TSP-HBA_Inner_100each_seed42_Moufarrej_Normotensive_MuSiC.txt"
Rscript COO-Decon-Published/Moufarrej_Pre-Eclampsia/01_run_MuSiC-2.R "$REF" "$META" "$MIXTURE_NORM" "$OUTPUT_NORM"

echo "All runs completed."
