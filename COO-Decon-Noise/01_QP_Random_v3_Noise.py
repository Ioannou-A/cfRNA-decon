import os
import numpy as np
import pandas as pd
from sklearn import preprocessing
from cvxopt import matrix, solvers
import time

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

data_paths = [
    "COO-Decon-Noise/Random_v2C-Noisy_Final3/Random_v2C-Noisy_phi1.0e+00_All-Counts.txt",
    "COO-Decon-Noise/Random_v2C-Noisy_Final3/Random_v2C-Noisy_phi1.0e+01_All-Counts.txt",
    "COO-Decon-Noise/Random_v2C-Noisy_Final3/Random_v2C-Noisy_phi1.0e+02_All-Counts.txt",
    "COO-Decon-Noise/Random_v2C-Noisy_Final3/Random_v2C-Noisy_phi2.0e+00_All-Counts.txt",
    "COO-Decon-Noise/Random_v2C-Noisy_Final3/Random_v2C-Noisy_phi2.0e+01_All-Counts.txt",
    "COO-Decon-Noise/Random_v2C-Noisy_Final3/Random_v2C-Noisy_phi3.0e+00_All-Counts.txt",
    "COO-Decon-Noise/Random_v2C-Noisy_Final3/Random_v2C-Noisy_phi3.0e+01_All-Counts.txt",
    "COO-Decon-Noise/Random_v2C-Noisy_Final3/Random_v2C-Noisy_phi5.0e+00_All-Counts.txt",
    "COO-Decon-Noise/Random_v2C-Noisy_Final3/Random_v2C-Noisy_phi5.0e+01_All-Counts.txt"
]

# List of basis matrices
basis_paths = [
    "CIBERSORTx-Matrix_TSP-BDa_Inner_300_1500_10/CIBERSORTx_TSP-BDa_Inner_25each_inferred_phenoclasses.CIBERSORTx_TSP-BDa_Inner_25each_inferred_refsample.bm.K999.txt"
]

# Loop through basis matrices and data paths
for basis_path in basis_paths:
    basis_path_full = "COO-Decon-KnownTissue/" + basis_path
    output_dir_name = os.path.dirname(basis_path).replace("CIBERSORTx-Matrix_", "") + "-Random_v3_Noisy-E5_Final"
    output_dir = os.path.join(base_output_dir, output_dir_name)
    os.makedirs(output_dir, exist_ok=True)
    
    print(f"Running QP for {basis_path} -> Output: {output_dir}")
    
    for data_path in data_paths:
        start_time = time.time()  # Start timer

        qp_deconvolution(
            data_path=data_path,
            basis_path=basis_path_full,
            output_dir=output_dir
        )
        
        elapsed = time.time() - start_time  # Stop timer
        minutes, seconds = divmod(int(elapsed), 60)
        print(f"  → Runtime: {minutes} min {seconds} sec")

print("All QP deconvolution tasks completed.")