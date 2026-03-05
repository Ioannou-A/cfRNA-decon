#!/bin/bash
#$ -l h_vmem=16G              # memory per slot
#$ -l h_rt=47:00:00           # max runtime
#$ -pe sharedmem 2          # request 2 CPU cores
#$ -cwd                       # run in current working dir
#$ -N CIBER_Healthy         # job name
#$ -m ae                      # email on abort/end
#$ -M s2556897@ed.ac.uk       # email address

# Define modules
source /etc/profile.d/modules.sh
module load singularity/4.1.3

# Insert here your credentials of CIBERSORTx generated from https://cibersortx.stanford.edu/
CIBERSORTX_USERNAME="your_email@domain"
CIBERSORTX_TOKEN="your_token_here"

# List of basis paths
basis_paths=(
    "CIBERSORTx-Matrix_TSP-BDa_Outer_300_1500_10/CIBERSORTx_TSP-BDa_Outer_25each_inferred_phenoclasses.CIBERSORTx_TSP-BDa_Outer_25each_inferred_refsample.bm.K999.txt"
)

for basis_path in "${basis_paths[@]}"; do
    (
        # Extract directory name (second-to-last directory)
        directory_name=$(dirname "$basis_path")
        echo "Extracted directory name: $directory_name"
    
        # Extract the base directory name (last directory name in path) and append -Chalasani_Healthy
        output_dir_name=$(basename "$directory_name" | sed 's/^CIBERSORTx-Matrix_//')-Chalasani_Healthy
        echo "Output directory name: $output_dir_name"
        mkdir -p COO-Decon-Published/Chalasani_Fatty-Liver/${output_dir_name}

        # Extract the final .txt file name
        file_name=$(basename "$basis_path")
        echo "Extracted file name: $file_name"

        # Copy the All-Healthy_Counts_v46_Clean_UniquePatients_CPM.txt file to the appropriate directory
        echo "Copying All-Healthy_Counts_v46_Clean_UniquePatients_CPM.txt to COO-Decon-Published/${directory_name}"
        cp COO-Decon-Published/Chalasani_Fatty-Liver/All-Healthy_Counts_v46_Clean_UniquePatients_CPM.txt COO-Decon-Published/${directory_name}
    
        # Run the Docker command for deconvolution
        echo "Running Docker command with mixture file All-Healthy_Counts_v46_Clean_UniquePatients_CPM.txt and signature matrix $file_name"
        singularity exec \
            -B COO-Decon-Published/${directory_name}:/src/data \
            -B COO-Decon-Published/Chalasani_Fatty-Liver/${output_dir_name}:/src/outdir \
            fractions_latest.sif /src/CIBERSORTxFractions \
            --username "$CIBERSORTX_USERNAME" --token "$CIBERSORTX_TOKEN" \
            --mixture /src/data/All-Healthy_Counts_v46_Clean_UniquePatients_CPM.txt --sigmatrix /src/data/${file_name} --verbose TRUE

        # Confirm completion of current iteration
        echo "Completed processing for: $basis_path"
#    ) &
    )
done

# Wait for all background jobs to complete
#wait
echo "All processes completed."