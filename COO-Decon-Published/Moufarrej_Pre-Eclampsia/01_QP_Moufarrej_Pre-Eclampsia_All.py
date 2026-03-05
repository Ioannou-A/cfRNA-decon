import os
import numpy as np
import pandas as pd
from sklearn import preprocessing
from cvxopt import matrix, solvers

def qp_deconvolution(data_path, basis_path, output_dir):
    # Load the dataset, ignoring commented lines
    data = pd.read_csv(data_path, delimiter="\t", low_memory=False, comment='#')
    data.set_index(data.columns[0], inplace=True)
    
    # Load the basis matrix
    basis = pd.read_csv(basis_path, delimiter="\t", low_memory=False, header=0, index_col=0)
    
    # Filter both DataFrames to keep only common genes
    common_indexes = data.index.intersection(basis.index)
    filtered_data = data.loc[common_indexes]
    filtered_basis = basis.loc[common_indexes]
    
    # Scale the data
    scaledMat = pd.DataFrame(preprocessing.scale(filtered_basis.values), index=filtered_basis.index, columns=filtered_basis.columns)
    scaledMix = pd.DataFrame(preprocessing.scale(filtered_data.values), index=filtered_data.index, columns=filtered_data.columns)
    
    # Initialize result DataFrame
    QP_df = pd.DataFrame(index=scaledMat.columns, columns=scaledMix.columns)
    
    # Perform QP deconvolution
    for i in range(scaledMix.shape[1]):
        mixture = scaledMix.iloc[:, i]
        P = matrix(scaledMat.values.T.dot(scaledMat.values))
        q = matrix(-1 * scaledMat.values.T.dot(mixture.values))
        numCells = scaledMat.shape[1]
        A = matrix(np.ones(numCells).reshape((1, numCells)))
        b = matrix(np.ones(1).reshape((1, 1)))
        G = matrix(-1.0 * np.identity(numCells))
        h = matrix(0.0, (numCells, 1))
        soln = solvers.qp(P, q, G, h, A, b)
        QP_df.iloc[:, i] = np.asarray(soln['x']).flatten()
    
    # Final formatting and export
    QP_df = QP_df.astype(float).T
    QP_df[QP_df < 0] = 0
    QP_df *= 100
    QP_df = QP_df.round(5)
    
    # Generate a safe output filename
    input_basename = os.path.splitext(os.path.basename(data_path))[0]  # Remove path and extension
    output_filename = os.path.join(output_dir, f"QP_{input_basename}_composition.txt")
    QP_df.to_csv(output_filename, sep="\t", index=True, header=True)
    print(f"Results saved to {output_filename}")

# Define paths
base_output_dir = os.getcwd()

data_path_norm="COO-Decon-Published/Moufarrej_Pre-Eclampsia/GSE192902_Normotensive_preQC_filtered_counts_UniquePatient_SpecificSample.txt"
data_path_severe="COO-Decon-Published/Moufarrej_Pre-Eclampsia/GSE192902_SeverePre-eclampsia_preQC_filtered_counts_UniquePatient_SpecificSample.txt"
data_path_preeclampsia="COO-Decon-Published/Moufarrej_Pre-Eclampsia/GSE192902_Pre-eclampsia_preQC_filtered_counts_UniquePatient_SpecificSample.txt"
output_dir_preeclampsia="COO-Decon-Published/Moufarrej_Pre-Eclampsia/TSP-BDa_Outer_300_1500_10-Moufarrej_Pre-eclampsia"
output_dir_severe="COO-Decon-Published/Moufarrej_Pre-Eclampsia/TSP-BDa_Outer_300_1500_10-Moufarrej_SeverePre-eclampsia"
output_dir_norm="COO-Decon-Published/Moufarrej_Pre-Eclampsia/TSP-BDa_Outer_300_1500_10-Moufarrej_Normotensive"

# List of basis matrices
basis_path="COO-Decon-Published/CIBERSORTx-Matrix_TSP-BDa_Inner_300_1500_10/CIBERSORTx_TSP-BDa_Inner_25each_inferred_phenoclasses.CIBERSORTx_TSP-BDa_Inner_25each_inferred_refsample.bm.K999.txt"

# Loop through basis matrices and data paths
print(f"Running QP for {data_path_severe} -> Output: {output_dir_severe}")
    
qp_deconvolution(
            data_path=data_path_severe,
            basis_path=basis_path,
            output_dir=output_dir_severe
        )

print(f"Running QP for {data_path_preeclampsia} -> Output: {output_dir_preeclampsia}")
    
qp_deconvolution(
            data_path=data_path_preeclampsia,
            basis_path=basis_path,
            output_dir=output_dir_preeclampsia
        )

print(f"Running QP for {data_path_norm} -> Output: {output_dir_norm}")
    
qp_deconvolution(
            data_path=data_path_norm,
            basis_path=basis_path,
            output_dir=output_dir_norm
        )

print("All QP deconvolution tasks completed.")
