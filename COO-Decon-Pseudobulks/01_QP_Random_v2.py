import os
import numpy as np
import pandas as pd
from sklearn import preprocessing
from sklearn.metrics import mean_squared_error
from scipy import stats
from cvxopt import matrix, solvers

def qp_deconvolution(data_path, basis_path, groundtruth_path, output_dir):
    # Load the dataset, ignoring commented lines
    data = pd.read_csv(data_path, delimiter="\t", low_memory=False, comment='#')
    data.set_index(data.columns[0], inplace=True)
    
    # Load the basis matrix
    basis = pd.read_csv(basis_path, delimiter="\t", low_memory=False, header=0, index_col=0)
    
    # Load the ground truth matrix and rearrange
    groundtruth2 = pd.read_csv(groundtruth_path, delimiter="\t", low_memory=False, header=0, index_col=0).drop(columns=['TotalCells']).T
    groundtruth = pd.DataFrame(0.0, index=basis.columns, columns=groundtruth2.columns)
    
    for row in groundtruth.index:
        cell_types = row.split('/')
        for cell_type in cell_types:
            if cell_type in groundtruth2.index:
                groundtruth.loc[row] += groundtruth2.loc[cell_type]
    groundtruth = groundtruth.T
    
    # Filter both DataFrames to keep only common genes
    common_indexes = data.index.intersection(basis.index)
    filtered_data = data.loc[common_indexes]
    filtered_basis = basis.loc[common_indexes]
    
    # Scale the data
    scaledMat = pd.DataFrame(preprocessing.scale(filtered_basis.values), index=filtered_basis.index, columns=filtered_basis.columns)
    scaledMix = pd.DataFrame(preprocessing.scale(filtered_data.values), index=filtered_data.index, columns=filtered_data.columns)
    
    # Initialize result DataFrames
    QP_df = pd.DataFrame(index=scaledMat.columns, columns=scaledMix.columns)
    rmse_results = pd.DataFrame()
    
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
    
    # Convert and transpose results
    QP_df = QP_df.astype(float).T
    preds_norm = np.dot(scaledMat, QP_df.T)
    rmse_list = []
    
    # Compute RMSE and Pearson correlation
    for i in range(scaledMix.shape[1]):
        gt_sample = scaledMix.values[:, i]
        pred_sample = preds_norm[:, i]
        rmse_value2 = np.sqrt(mean_squared_error(gt_sample, pred_sample))
        pearsonR_QP, pearsonP_QP = stats.pearsonr(gt_sample, pred_sample)
        rmse_list.append({'Sample': scaledMix.columns[i], 'RMSE-PredictedCounts': rmse_value2, 'r-PredictedCounts': pearsonR_QP, 'p-value-PredictedCounts': pearsonP_QP})
    
    rmse_results = pd.DataFrame(rmse_list).set_index('Sample')
    QP_df[QP_df < 0] = 0
    QP_df *= 100
    
    # Compute RMSE for composition
    rmse_values, r_values, p_values = [], [], []
    for index, row in QP_df.iterrows():
        true_values = groundtruth.loc[index].values
        rmse_values.append(np.sqrt(mean_squared_error(true_values, row.values)))
        r, p = stats.pearsonr(true_values, row.values)
        r_values.append(r)
        p_values.append(p)
    
    QP_df['RMSE-Composition'] = rmse_values
    QP_df['r-Composition'] = r_values
    QP_df['RMSE-PredictedCounts'] = rmse_results['RMSE-PredictedCounts']
    QP_df['r-PredictedCounts'] = rmse_results['r-PredictedCounts']
    QP_df = QP_df.round(3)
    
    # Save output
    output_filename = os.path.join(output_dir, "QP_" + os.path.basename(data_path))
    QP_df.to_csv(output_filename, sep="\t", index=True, header=True)
    print(f"Results saved to {output_filename}")


# Define paths
data_path = "COO-Decon-Pseudobulks/Random_v2C_All-Counts.txt"
groundtruth_path = "COO-Decon-Pseudobulks/Random_v2C_All-Proportions.txt"
base_output_dir = os.getcwd()

# List of basis matrices
basis_paths = [
    "CIBERSORTx-Matrix_TSP-BDa_Inner_1000_3000_10/CIBERSORTx_TSP-BDa_Inner_25each_inferred_phenoclasses.CIBERSORTx_TSP-BDa_Inner_25each_inferred_refsample.bm.K999.txt",
    "CIBERSORTx-Matrix_TSP-BDa_Inner_3000_5000_10/CIBERSORTx_TSP-BDa_Inner_25each_inferred_phenoclasses.CIBERSORTx_TSP-BDa_Inner_25each_inferred_refsample.bm.K999.txt",
    "CIBERSORTx-Matrix_TSP-BDa_Inner_300_1500_10/CIBERSORTx_TSP-BDa_Inner_25each_inferred_phenoclasses.CIBERSORTx_TSP-BDa_Inner_25each_inferred_refsample.bm.K999.txt",
    "CIBERSORTx-Matrix_TSP-BDa_Outer_1000_3000_10/CIBERSORTx_TSP-BDa_Outer_25each_inferred_phenoclasses.CIBERSORTx_TSP-BDa_Outer_25each_inferred_refsample.bm.K999.txt",
    "CIBERSORTx-Matrix_TSP-BDa_Outer_3000_5000_10/CIBERSORTx_TSP-BDa_Outer_25each_inferred_phenoclasses.CIBERSORTx_TSP-BDa_Outer_25each_inferred_refsample.bm.K999.txt",
    "CIBERSORTx-Matrix_TSP-BDa_Outer_300_1500_10/CIBERSORTx_TSP-BDa_Outer_25each_inferred_phenoclasses.CIBERSORTx_TSP-BDa_Outer_25each_inferred_refsample.bm.K999.txt",
    "CIBERSORTx-Matrix_TSP-HBA_Inner_1000_3000_10/CIBERSORTx_TSP-HBA_Inner_25each_inferred_phenoclasses.CIBERSORTx_TSP-HBA_Inner_25each_inferred_refsample.bm.K999.txt",
    "CIBERSORTx-Matrix_TSP-HBA_Inner_3000_5000_10/CIBERSORTx_TSP-HBA_Inner_25each_inferred_phenoclasses.CIBERSORTx_TSP-HBA_Inner_25each_inferred_refsample.bm.K999.txt",
    "CIBERSORTx-Matrix_TSP-HBA_Inner_300_1500_10/CIBERSORTx_TSP-HBA_Inner_25each_inferred_phenoclasses.CIBERSORTx_TSP-HBA_Inner_25each_inferred_refsample.bm.K999.txt",
]

# Loop through basis matrices and run NuSVR deconvolution
for basis_path in basis_paths:
    # Extract directory name to create output folder
    basis_path_full = "COO-Matrix/" + basis_path
    output_dir_name = os.path.dirname(basis_path).replace("CIBERSORTx-Matrix_", "") + "-Random_v2"
    output_dir = os.path.join(base_output_dir, output_dir_name)
    
    # Create the directory
    os.makedirs(output_dir, exist_ok=True)
    
    print(f"Running QP for {basis_path} -> Output: {output_dir}")
    
    # Run the deconvolution function
    qp_deconvolution(
        data_path=data_path,
        basis_path=basis_path_full,
        groundtruth_path=groundtruth_path,
        output_dir=output_dir
    )

print("All QP deconvolution tasks completed.")
