#!/bin/bash
#$ -l h_vmem=16G
#$ -l h_rt=47:30:00
#$ -pe sharedmem 2
#$ -cwd
#$ -N CIBER_BDa-Outer-Noisy
#$ -m a
#$ -M s2556897@ed.ac.uk
#$ -t 1-110               

source /etc/profile.d/modules.sh
module load singularity/4.1.3

# Start timer
SECONDS=0

# Job-specific variables
TASKID=$SGE_TASK_ID
basis_path="CIBERSORTx_TSP-BDa_Outer_25each_inferred_phenoclasses.CIBERSORTx_TSP-BDa_Outer_25each_inferred_refsample.bm.K999.txt"

# Insert here your credentials of CIBERSORTx generated from https://cibersortx.stanford.edu/
CIBERSORTX_USERNAME="your_email@domain"
CIBERSORTX_TOKEN="your_token_here"

# Desired output prefix
output_dir_name="TSP-BDa_Outer_300_1500_10"

# Directory containing all noisy mixtures
mixture_dir="COO-Decon-Noise/Random_v2C-Noisy_Final3"

# Generate list of all mixture files and pick one by TASKID
mixture_file=$(ls ${mixture_dir}/Random_v2C-Noisy_phi*_All-Counts_part*.txt | sort | sed -n "${TASKID}p")

echo "Processing mixture file: $mixture_file"

# Prepare output directory (unique per mixture file)
mixture_base=$(basename "$mixture_file" .txt)
outdir="COO-Decon-Noise/${output_dir_name}_${mixture_base}"
mkdir -p "$outdir"

# Run CIBERSORTx
singularity exec \
    -B "$mixture_dir:/src/data" \
    -B "$outdir:/src/outdir" \
    fractions_latest.sif /src/CIBERSORTxFractions \
    --username "$CIBERSORTX_USERNAME" --token "$CIBERSORTX_TOKEN" \
    --mixture /src/data/$(basename "$mixture_file") \
    --sigmatrix /src/data/${basis_path} --verbose TRUE

# Compute runtime
duration=$SECONDS
echo "[$(date)] Finished task ${TASKID}"
echo "Runtime: $((duration / 60)) min $((duration % 60)) sec"