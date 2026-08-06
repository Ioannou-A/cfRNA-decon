#!/bin/bash
#$ -l h_vmem=36G
#$ -l h_rt=180:00:00
#$ -cwd
#$ -N CIBER_TOO_RANDOM
#$ -m ae
#$ -M s2556897@ed.ac.uk
#$ -t 1-5

source /etc/profile.d/modules.sh
module load singularity/4.1.3

# Insert here your credentials of CIBERSORTx generated from https://cibersortx.stanford.edu/
CIBERSORTX_USERNAME="your_email@domain"
CIBERSORTX_TOKEN="your_token_here"

common_root="TOO-Decon-Undetected"

basis_paths=(
  "20250723_TOO-Matrices_Renamed/CIBERSORTx-TOO-Matrix_2Median_300_500/CIBERSORTx_20250405_PhenotypeClass_LessTissueV2_2Median.CIBERSORTx_20250405_GeneID_LessTissueV2_2Median.withGTFNames.txt"
)

mixture_paths=(
  "Data/20250616_All-Tissues-NoDup_Random_20_percent_removed_CPM.txt"
  "Data/20250616_All-Tissues-NoDup_Random_40_percent_removed_CPM.txt"
  "Data/20250616_All-Tissues-NoDup_Random_60_percent_removed_CPM.txt"
  "Data/20250616_All-Tissues-NoDup_Random_80_percent_removed_CPM.txt"
  "Data/20250616_All-Tissues-NoDup_Random_100_percent_removed_CPM.txt"
)

basis_path="${basis_paths[0]}"
mixture_path="${mixture_paths[$((SGE_TASK_ID-1))]}"

basis_dir=$(dirname "$basis_path")
basis_filename=$(basename "$basis_path")

mixture_filename=$(basename "$mixture_path")
mixture_basename="${mixture_filename%.*}"

basis_label=$(echo "$basis_dir" | sed 's|.*CIBERSORTx-TOO-Matrix_||')

output_dir_name="Decon-Results_${mixture_basename}_${basis_label}"

abs_basis_dir="${common_root}/${basis_dir}"
abs_mixture_file="${common_root}/${mixture_path}"

echo "Task ID: $SGE_TASK_ID"
echo "Basis path: $basis_path"
echo "Mixture path: $mixture_path"
echo "Basis directory: $abs_basis_dir"
echo "Basis file: $basis_filename"
echo "Mixture file: $mixture_filename"
echo "Output dir: $output_dir_name"

mkdir -p "$output_dir_name"

echo "Copying mixture file into basis directory..."
cp "$abs_mixture_file" "$abs_basis_dir/$mixture_filename"

singularity exec \
    -B "$abs_basis_dir":/src/data \
    -B "$(pwd)/$output_dir_name":/src/outdir \
    /fractions_latest.sif \
    /src/CIBERSORTxFractions \
    --username ${CIBERSORTX_USERNAME} \
    --token ${CIBERSORTX_TOKEN} \
    --mixture "/src/data/${mixture_filename}" \
    --sigmatrix "/src/data/${basis_filename}"

echo "Completed: $mixture_basename with $basis_label"