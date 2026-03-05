import os
import numpy as np
import pandas as pd
from sklearn import preprocessing
from scipy.optimize import nnls

def nnls_deconvolution(data_path, basis_path, output_dir):
    # Load the dataset, ignoring commented lines
    data = pd.read_csv(data_path, delimiter="\t", low_memory=False, comment='#')
    data.set_index(data.columns[0], inplace=True)
    
    # Load basis matrix
    basis = pd.read_csv(basis_path, delimiter="\t", low_memory=False, header=0, index_col=0)
    
    # Get common indexes and filter data
    common_indexes = data.index.intersection(basis.index)

    # Sort the common indexes (optional but good)
    common_indexes = common_indexes.sort_values()

    # Reindex both data and basis to the same ordered index
    filtered_data = data.loc[common_indexes]
    filtered_basis = basis.loc[common_indexes]
    
    # Scale matrices
    scaled_basis = preprocessing.scale(filtered_basis.values)
    scaled_basis_df = pd.DataFrame(scaled_basis, index=filtered_basis.index, columns=filtered_basis.columns)
    
    scaled_data = preprocessing.scale(filtered_data.values)
    scaled_data_df = pd.DataFrame(scaled_data, index=filtered_data.index, columns=filtered_data.columns)
    
    # Perform NNLS deconvolution
    nnls_result = pd.DataFrame(index=scaled_basis_df.columns, columns=scaled_data_df.columns)
    
    for i in range(scaled_data_df.shape[1]):
        mixture = scaled_data_df.iloc[:, i].values
        coefs, _ = nnls(scaled_basis_df.values, mixture, maxiter=10**5)
        if coefs.sum() != 0:
            coefs = coefs / coefs.sum()
        nnls_result.iloc[:, i] = coefs
    
    nnls_result = nnls_result.astype(float).T
    nnls_result *= 100  # Convert to percentages
    nnls_result = nnls_result.round(5)
    
    # Construct output filename
    input_filename = os.path.basename(data_path)
    output_filename = f"NNLS_{input_filename}"
    output_path = os.path.join(output_dir, output_filename)
    
    # Save output
    nnls_result.to_csv(output_path, sep="\t", index=True, header=True)
    
    print(f"Deconvolution results saved to: {output_path}")

# Define paths
data_path = "TOO-Decon-Published/Moufarrej_Pre-Eclampsia/GSE192902_Normotensive_preQC_filtered_counts_UniquePatient_SpecificSample.txt"
base_output_dir = os.getcwd()

# List of basis matrices
basis_path = "TOO-Matrix/TOO-Matrices_Renamed/CIBERSORTx-TOO-Matrix_2Median_300_500/CIBERSORTx_20250405_PhenotypeClass_LessTissueV2_2Median.CIBERSORTx_20250405_GeneID_LessTissueV2_2Median.withGTFNames.txt"

# Create the directory
output_dir_name = "Decon-Results_Moufarrej_Normotensive_SpecificSample"
output_dir = os.path.join(base_output_dir, output_dir_name)
os.makedirs(output_dir, exist_ok=True)
    
    
# Run the deconvolution function
nnls_deconvolution(
        data_path=data_path,
        basis_path=basis_path,
        output_dir=output_dir
    )