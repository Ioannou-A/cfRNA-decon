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
base_output_dir = os.getcwd()

data_path_healthy="COO-Decon-Published/Chalasani_Fatty-Liver/All-Healthy_Counts_v46_Clean_UniquePatients_CPM.txt"
data_path_nafld="COO-Decon-Published/Chalasani_Fatty-Liver/All-NAFLD_Counts_v46_Clean_UniquePatients_CPM.txt"
output_dir_nafld="COO-Decon-Published/Chalasani_Fatty-Liver/TSP-BDa_Outer_300_1500_10-Chalasani_NAFLD"
output_dir_healthy="COO-Decon-Published/Chalasani_Fatty-Liver/TSP-BDa_Outer_300_1500_10-Chalasani_Healthy"
data_path_nash="COO-Decon-Published/Chalasani_Fatty-Liver/All-NASH_Counts_v46_Clean_UniquePatients_CPM.txt"
output_dir_nash="COO-Decon-Published/Chalasani_Fatty-Liver/TSP-BDa_Outer_300_1500_10-Chalasani_NASH"

# List of basis matrices
basis_path="COO-Decon-Published/CIBERSORTx-Matrix_TSP-BDa_Inner_300_1500_10/CIBERSORTx_TSP-BDa_Inner_25each_inferred_phenoclasses.CIBERSORTx_TSP-BDa_Inner_25each_inferred_refsample.bm.K999.txt"

# Loop through basis matrices and data paths
print(f"Running NNLS for {data_path_healthy} -> Output: {output_dir_healthy}")
    
nnls_deconvolution(
            data_path=data_path_healthy,
            basis_path=basis_path,
            output_dir=output_dir_healthy
        )

print(f"Running NNLS for {data_path_nafld} -> Output: {output_dir_nafld}")
    
nnls_deconvolution(
            data_path=data_path_nafld,
            basis_path=basis_path,
            output_dir=output_dir_nafld
        )

print(f"Running NNLS for {data_path_nash} -> Output: {output_dir_nash}")
    
nnls_deconvolution(
            data_path=data_path_nash,
            basis_path=basis_path,
            output_dir=output_dir_nash
        )

print("All NNLS deconvolution tasks completed.")
