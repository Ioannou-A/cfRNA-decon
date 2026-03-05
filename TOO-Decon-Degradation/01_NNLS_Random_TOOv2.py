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
base_output_dir = os.getcwd()

# Define input data paths
data_paths = [
    "TOO-Decon-Degradation/Data/20250616_All-Tissues-NoDup_Random_Degradation_top_10_percent_removed.txt",
    "TOO-Decon-Degradation/Data/20250616_All-Tissues-NoDup_Random_Degradation_top_20_percent_removed.txt",
    "TOO-Decon-Degradation/Data/20250616_All-Tissues-NoDup_Random_Degradation_top_30_percent_removed.txt",
    "TOO-Decon-Degradation/Data/20250616_All-Tissues-NoDup_Random_Degradation_top_40_percent_removed.txt",
]

# List of basis matrices
basis_paths = [
    "TOO-Matrix/TOO-Matrices_Renamed/CIBERSORTx-TOO-Matrix_2Median_300_500/CIBERSORTx_20250405_PhenotypeClass_LessTissueV2_2Median.CIBERSORTx_20250405_GeneID_LessTissueV2_2Median.withGTFNames.txt",
]

# Loop over data files and basis matrices
for data_path in data_paths:
    data_basename = os.path.splitext(os.path.basename(data_path))[0]

    for basis_path in basis_paths:
        # Get full path for basis
        basis_path_full = os.path.join(base_output_dir, basis_path)

        # Create output directory using degradation info + basis matrix identifier
        relative_output = os.path.dirname(basis_path).replace("TOO-Matrix/TOO-Matrices_Renamed/CIBERSORTx-TOO-Matrix_", "")
        output_dir_name = f"Decon-Results_{data_basename}_{relative_output}/"
        output_dir = os.path.join(base_output_dir, output_dir_name)
        os.makedirs(output_dir, exist_ok=True)

        print(f"Running QP: Data={data_path} | Basis={basis_path} -> Output={output_dir}")
        nnls_deconvolution(data_path=data_path, basis_path=basis_path_full, output_dir=output_dir)

print("All QP deconvolution tasks completed.")