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

data_path_nci="COO-Decon-Published/Toden_AD/All-NCI_Counts_v46_Clean_UniquePatients_CPM.txt"
data_path_ad="COO-Decon-Published/Toden_AD/All-AD_Counts_v46_Clean_UniquePatients_CPM.txt"
output_dir_ad="COO-Decon-Published/Toden_AD/TSP-BDa_Outer_300_1500_10-Toden-AD"
output_dir_nci="COO-Decon-Published/Toden_AD/TSP-BDa_Outer_300_1500_10-Toden-NCI"

# List of basis matrices
basis_path="COO-Decon-Published/CIBERSORTx-Matrix_TSP-BDa_Inner_300_1500_10/CIBERSORTx_TSP-BDa_Inner_25each_inferred_phenoclasses.CIBERSORTx_TSP-BDa_Inner_25each_inferred_refsample.bm.K999.txt"

# Loop through basis matrices and data paths
print(f"Running QP for {data_path_nci} -> Output: {output_dir_nci}")
    
qp_deconvolution(
            data_path=data_path_nci,
            basis_path=basis_path,
            output_dir=output_dir_nci
        )

print(f"Running QP for {data_path_ad} -> Output: {output_dir_ad}")
    
qp_deconvolution(
            data_path=data_path_ad,
            basis_path=basis_path,
            output_dir=output_dir_ad
        )

print("All QP deconvolution tasks completed.")
