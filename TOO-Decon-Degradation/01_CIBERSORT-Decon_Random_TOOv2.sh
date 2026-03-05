#!/bin/bash

# Insert here your credentials of CIBERSORTx generated from https://cibersortx.stanford.edu/
CIBERSORTX_USERNAME="your_email@domain"
CIBERSORTX_TOKEN="your_token_here"

common_root="TOO-Decon-Degradation"

basis_paths=(
    "TOO-Matrix/TOO-Matrices_Renamed/CIBERSORTx-TOO-Matrix_2Median_300_500/CIBERSORTx_20250405_PhenotypeClass_LessTissueV2_2Median.CIBERSORTx_20250405_GeneID_LessTissueV2_2Median.withGTFNames.txt"
)

mixture_paths=(
    "Data/20250616_All-Tissues-NoDup_Random_Degradation_top_10_percent_removed.txt"
    "Data/20250616_All-Tissues-NoDup_Random_Degradation_top_20_percent_removed.txt"
    "Data/20250616_All-Tissues-NoDup_Random_Degradation_top_30_percent_removed.txt"
    "Data/20250616_All-Tissues-NoDup_Random_Degradation_top_40_percent_removed.txt"
)

module load singularity/4.1.3

for mixture_path in "${mixture_paths[@]}"; do
    mixture_filename=$(basename "$mixture_path")
    mixture_basename="${mixture_filename%.*}"

    for basis_path in "${basis_paths[@]}"; do
        basis_dir=$(dirname "$basis_path")
        basis_filename=$(basename "$basis_path")
        basis_label=$(echo "$basis_dir" | sed 's|.*CIBERSORTx-TOO-Matrix_||')

        output_dir_name="Decon-Results_${mixture_basename}_${basis_label}"
        mkdir -p "$output_dir_name"

        # Absolute paths
        abs_basis_dir="${basis_dir}"
        abs_mixture_file="${common_root}/${mixture_path}"

        echo "Copying mixture file into basis directory..."
        cp "$abs_mixture_file" "$abs_basis_dir/$mixture_filename"

        echo "Running deconvolution for:"
        echo "  Mixture (copied): $abs_basis_dir/$mixture_filename"
        echo "  Basis: $abs_basis_dir/$basis_filename"
        echo "  Output dir: $output_dir_name"

        singularity exec \
            -B "$abs_basis_dir":/src/data \
            -B "$(pwd)/$output_dir_name":/src/outdir \
            fractions_latest.sif \
            /src/CIBERSORTxFractions \
            --username "$CIBERSORTX_USERNAME" --token "$CIBERSORTX_TOKEN" \
            --mixture "/src/data/${mixture_filename}" \
            --sigmatrix "/src/data/${basis_filename}"

        echo "Completed: $mixture_basename with $basis_label"
    done
done

echo "All deconvolution processes completed."
