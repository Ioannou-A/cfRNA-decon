#!/bin/bash
module load singularity/4.1.3

# Insert here your credentials of CIBERSORTx generated from https://cibersortx.stanford.edu/
CIBERSORTX_USERNAME="your_email@domain"
CIBERSORTX_TOKEN="your_token_here"

# List of basis paths
basis_paths=(
    "CIBERSORTx-Matrix_TSP-BDa_Inner_300_1500_10/CIBERSORTx_TSP-BDa_Inner_25each_inferred_phenoclasses.CIBERSORTx_TSP-BDa_Inner_25each_inferred_refsample.bm.K999.txt"
#    "CIBERSORTx-Matrix_TSP-BDa_Outer_300_1500_10/CIBERSORTx_TSP-BDa_Outer_25each_inferred_phenoclasses.CIBERSORTx_TSP-BDa_Outer_25each_inferred_refsample.bm.K999.txt"
#    "CIBERSORTx-Matrix_TSP-HBA_Inner_300_1500_10/CIBERSORTx_TSP-HBA_Inner_25each_inferred_phenoclasses.CIBERSORTx_TSP-HBA_Inner_25each_inferred_refsample.bm.K999.txt"
)

# Define base path
base_path="COO-Matrix/"

for basis_path in "${basis_paths[@]}"; do
    (
        # Extract directory name (second-to-last directory)
        directory_name=$(dirname "$basis_path")
        echo "Extracted directory name: $directory_name"
    
        # Extract the base directory name (last directory name in path) and append -GTEx-Brain
        output_dir_name=$(basename "$directory_name" | sed 's/^CIBERSORTx-Matrix_//')-GTEx-Brain
        echo "Output directory name: $output_dir_name"
    
        # Extract the final .txt file name
        file_name=$(basename "$basis_path")
        echo "Extracted file name: $file_name"
    
        # Copy the 20250830_GeneId_Brain_50PerRegion-Unique.OnlyInBrainRemapped.txt file to the appropriate directory
        echo "Copying 20250830_GeneId_Brain_50PerRegion-Unique.OnlyInBrainRemapped.txt to COO-Matrix/${directory_name}"
        cp COO-Decon-KnownTissue/20250830_GeneId_Brain_50PerRegion-Unique.OnlyInBrainRemapped.txt COO-Matrix/${directory_name}
    
        # Run the Docker command for deconvolution
        echo "Running Docker command with mixture file 20250830_GeneId_Brain_50PerRegion-Unique.OnlyInBrainRemapped.txt and signature matrix $file_name"
        singularity exec \
            -B COO-Matrix/${directory_name}:/src/data \
            -B COO-Decon-KnownTissue/${output_dir_name}:/src/outdir \
            fractions_latest.sif /src/CIBERSORTxFractions \
            --username "$CIBERSORTX_USERNAME" --token "$CIBERSORTX_TOKEN" \
            --mixture /src/data/20250830_GeneId_Brain_50PerRegion-Unique.OnlyInBrainRemapped.txt --sigmatrix /src/data/${file_name} --verbose TRUE

        # Confirm completion of current iteration
        echo "Completed processing for: $basis_path"
#    ) &
    )
done

# Wait for all background jobs to complete
#wait
echo "All processes completed."