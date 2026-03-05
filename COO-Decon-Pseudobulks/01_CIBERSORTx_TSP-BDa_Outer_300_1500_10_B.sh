#!/bin/bash
#$ -l h_vmem=16G
#$ -l h_rt=72:00:00
#$ -pe sharedmem 2
#$ -cwd
#$ -N CIBER_BDa-Outer
#$ -m ae
#$ -M s2556897@ed.ac.uk
#$ -t 1-11                

source /etc/profile.d/modules.sh
module load singularity/4.1.3

# Job-specific variables
TASKID=$SGE_TASK_ID
basis_path="CIBERSORTx-Matrix_TSP-BDa_Outer_300_1500_10/CIBERSORTx_TSP-BDa_Outer_25each_inferred_phenoclasses.CIBERSORTx_TSP-BDa_Outer_25each_inferred_refsample.bm.K999.txt"

# Insert here your credentials of CIBERSORTx generated from https://cibersortx.stanford.edu/
CIBERSORTX_USERNAME="your_email@domain"
CIBERSORTX_TOKEN="your_token_here"

directory_name=$(dirname "$basis_path")
file_name=$(basename "$basis_path")
output_dir_name=$(basename "$directory_name" | sed 's/^CIBERSORTx-Matrix_//')-Random_v2

mixture_file="Random_v2C_All-Counts_part${TASKID}.txt"

# Copy mixture file into working dir
cp COO-Decon-Pseudobulks/${mixture_file} \
   COO-Decon-Pseudobulks/${directory_name}

# Prepare output directory
mkdir -p COO-Decon-Pseudobulks/${output_dir_name}_part${TASKID}

# Run CIBERSORTx
singularity exec \
    -B COO-Decon-Pseudobulks/${directory_name}:/src/data \
    -B COO-Decon-Pseudobulks/${output_dir_name}_part${TASKID}:/src/outdir \
    fractions_latest.sif /src/CIBERSORTxFractions \
    --username "$CIBERSORTX_USERNAME" --token "$CIBERSORTX_TOKEN" \
    --mixture /src/data/${mixture_file} \
    --sigmatrix /src/data/${file_name} --verbose TRUE