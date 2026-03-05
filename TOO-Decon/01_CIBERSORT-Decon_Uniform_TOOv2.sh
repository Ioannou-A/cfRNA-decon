#!/bin/bash

# List of basis paths
basis_paths=("TOO-Matrix/TOO-Matrices_Renamed/CIBERSORTx-TOO-Matrix_2Median_1000_1500/CIBERSORTx_20250405_PhenotypeClass_LessTissueV2_2Median.CIBERSORTx_20250405_GeneID_LessTissueV2_2Median.withGTFNames.txt"
    "TOO-Matrix/TOO-Matrices_Renamed/CIBERSORTx-TOO-Matrix_2Median_300_500/CIBERSORTx_20250405_PhenotypeClass_LessTissueV2_2Median.CIBERSORTx_20250405_GeneID_LessTissueV2_2Median.withGTFNames.txt"
    "TOO-Matrix/TOO-Matrices_Renamed/CIBERSORTx-TOO-Matrix_2Median_500_1000/CIBERSORTx_20250405_PhenotypeClass_LessTissueV2_2Median.CIBERSORTx_20250405_GeneID_LessTissueV2_2Median.withGTFNames.txt"
    "TOO-Matrix/TOO-Matrices_Renamed/CIBERSORTx-TOO-Matrix_Sampling10_1000_1500/CIBERSORTx_20250405_PhenotypeClass_LessTissueV2_Sampling10.CIBERSORTx_20250405_GeneID_LessTissueV2_Sampling10.withGTFNames.txt"
    "TOO-Matrix/TOO-Matrices_Renamed/CIBERSORTx-TOO-Matrix_Sampling10_300_500/CIBERSORTx_20250405_PhenotypeClass_LessTissueV2_Sampling10.CIBERSORTx_20250405_GeneID_LessTissueV2_Sampling10.withGTFNames.txt"
    "TOO-Matrix/TOO-Matrices_Renamed/CIBERSORTx-TOO-Matrix_Sampling10_500_1000/CIBERSORTx_20250405_PhenotypeClass_LessTissueV2_Sampling10.CIBERSORTx_20250405_GeneID_LessTissueV2_Sampling10.withGTFNames.txt"
    "TOO-Matrix/TOO-Matrices_Renamed/CIBERSORTx-TOO-Matrix_Sampling5_1000_1500/CIBERSORTx_20250405_PhenotypeClass_LessTissueV2_Sampling5.CIBERSORTx_20250405_GeneID_LessTissueV2_Sampling5.withGTFNames.txt"
    "TOO-Matrix/TOO-Matrices_Renamed/CIBERSORTx-TOO-Matrix_Sampling5_300_500/CIBERSORTx_20250405_PhenotypeClass_LessTissueV2_Sampling5.CIBERSORTx_20250405_GeneID_LessTissueV2_Sampling5.withGTFNames.txt"
    "TOO-Matrix/TOO-Matrices_Renamed/CIBERSORTx-TOO-Matrix_Sampling5_500_1000/CIBERSORTx_20250405_PhenotypeClass_LessTissueV2_Sampling5.CIBERSORTx_20250405_GeneID_LessTissueV2_Sampling5.withGTFNames.txt"
)

# Insert here your credentials of CIBERSORTx generated from https://cibersortx.stanford.edu/
CIBERSORTX_USERNAME="your_email@domain"
CIBERSORTX_TOKEN="your_token_here"

# Define base path
base_path="TOO-Decon/"
module load singularity/4.1.3

for basis_path in "${basis_paths[@]}"; do
        # Extract directory name (second-to-last directory)
        directory_name=$(dirname "$basis_path")
        echo "Extracted directory name: $directory_name"

        # Extract the base directory name (last directory name in path) and append -Uniform_TOOv2
        output_dir_name=$(basename "$directory_name" | sed 's/^CIBERSORTx-TOO-Matrix/Decon-Results/')-Uniform_TOOv2_250
        echo "Output directory name: $output_dir_name"

        # Extract the final .txt file name
        file_name=$(basename "$basis_path")
        echo "Extracted file name: $file_name"
        cp TOO-Decon/20250616_All-Tissues-NoDup_Uniform_Simulated_v2_Counts.txt ${directory_name}

        # Run the Docker command for deconvolution
        echo "Running Docker command with mixture file Random_v1_All-Counts.txt and signature matrix $file_name"
        singularity exec -B ${directory_name}:/src/data -B ${output_dir_name}:/src/outdir fractions_latest.sif /src/CIBERSORTxFractions \
            --username "$CIBERSORTX_USERNAME" --token "$CIBERSORTX_TOKEN" --mixture /src/data/20250616_All-Tissues-NoDup_Uniform_Simulated_v2_Counts.txt --sigmatrix /src/data/${file_name}  --verbose TRUE

        # Confirm completion of current iteration
        echo "Completed processing for: $basis_path"
done

echo "All processes completed."
