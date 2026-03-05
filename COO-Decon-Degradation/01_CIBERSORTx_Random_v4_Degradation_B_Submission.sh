#!/bin/bash
#$ -l h_vmem=16G
#$ -l h_rt=72:00:00
#$ -pe sharedmem 2
#$ -cwd
#$ -N CIBER_BDa-Outer-Deg
#$ -m ae
#$ -M s2556897@ed.ac.uk
#$ -t 1-44               

source /etc/profile.d/modules.sh
module load singularity/4.1.3

# Insert here your credentials of CIBERSORTx generated from https://cibersortx.stanford.edu/
CIBERSORTX_USERNAME="your_email@domain"
CIBERSORTX_TOKEN="your_token_here"

# Job-specific variables
TASKID=$SGE_TASK_ID
basis_path="CIBERSORTx_TSP-BDa_Outer_25each_inferred_phenoclasses.CIBERSORTx_TSP-BDa_Outer_25each_inferred_refsample.bm.K999.txt"

# Desired output prefix
output_dir_name="TSP-BDa_Outer_300_1500_10"

# Directory containing all mixtures without faster degrading genes
mixture_dir="COO-Decon-Degradation/Data"

# Generate list of all mixture files and pick one by TASKID
mixture_file=$(ls ${mixture_dir}/Random_v2C_top_*_percent_removed_part*.txt | sort | sed -n "${TASKID}p")

echo "Processing mixture file: $mixture_file"

# Prepare output directory (unique per mixture file)
mixture_base=$(basename "$mixture_file" .txt)
outdir="COO-Decon-Degradation/${output_dir_name}_${mixture_base}"
mkdir -p "$outdir"

# Run CIBERSORTx
singularity exec \
    -B "$mixture_dir:/src/data" \
    -B "$outdir:/src/outdir" \
    fractions_latest.sif /src/CIBERSORTxFractions \
    --username "$CIBERSORTX_USERNAME" --token "$CIBERSORTX_TOKEN" \
    --mixture /src/data/$(basename "$mixture_file") \
    --sigmatrix /src/data/${basis_path} --verbose TRUE