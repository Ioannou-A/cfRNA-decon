import os
import numpy as np
import pandas as pd
from sklearn import preprocessing
from sklearn.metrics import mean_squared_error
from scipy import stats
from scipy.optimize import nnls

def nnls_deconvolution(data_path, basis_path, groundtruth_path, output_dir):
    # Load the dataset, ignoring commented lines
    data = pd.read_csv(data_path, delimiter="\t", low_memory=False, comment='#')
    data.set_index(data.columns[0], inplace=True)
    
    # Load basis matrix
    basis = pd.read_csv(basis_path, delimiter="\t", low_memory=False, header=0, index_col=0)
    
    # Load ground truth and process it
    groundtruth2 = pd.read_csv(groundtruth_path, delimiter="\t", low_memory=False, header=0, index_col=0)
    groundtruth2 = groundtruth2.drop(columns=['TotalCells']).T
    groundtruth = pd.DataFrame(0.0, index=basis.columns, columns=groundtruth2.columns)
    
    for row in groundtruth.index:
        cell_types = row.split('/')
        for cell_type in cell_types:
            if cell_type in groundtruth2.index:
                groundtruth.loc[row] += groundtruth2.loc[cell_type]
    
    groundtruth = groundtruth.T
    
    # Get common indexes and filter data
    common_indexes = data.index.intersection(basis.index)
    filtered_data = data.loc[common_indexes]
    filtered_basis = basis.loc[common_indexes]
    
    # Scale matrices
    scaledMat = preprocessing.scale(filtered_basis.values)
    scaledMat = pd.DataFrame(data=scaledMat, index=filtered_basis.index, columns=filtered_basis.columns)
    
    scaledMix = preprocessing.scale(filtered_data.values)
    scaledMix = pd.DataFrame(data=scaledMix, index=filtered_data.index, columns=filtered_data.columns)
    
    # Perform NNLS deconvolution
    NNLS_df = pd.DataFrame(index=scaledMat.columns, columns=scaledMix.columns)
    rmse_results = pd.DataFrame()
    
    for i in range(scaledMix.shape[1]):
        mixture = scaledMix.iloc[:, i].values
        coefs, resid = nnls(scaledMat.values, mixture, maxiter=10**5)
        total_sum_column = coefs.sum()
        if total_sum_column != 0:
            coefs = coefs / total_sum_column
        NNLS_df.iloc[:, i] = coefs
    
    NNLS_df = NNLS_df.astype(float).T
    
    # Calculate RMSE and Pearson correlation
    groundtruth2 = scaledMix.values
    preds_norm = np.dot(scaledMat, NNLS_df.T)
    
    for i in range(groundtruth2.shape[1]):
        gt_sample = groundtruth2[:, i]
        pred_sample = preds_norm[:, i]
        rmse_value2 = np.sqrt(mean_squared_error(gt_sample, pred_sample))
        pearsonR_NNLS, pearsonP_NNLS = stats.pearsonr(gt_sample, pred_sample)
        sampName = scaledMix.columns[i]
        rmse_row = pd.DataFrame({'Sample': [sampName], 'RMSE-PredictedCounts': [rmse_value2],
                                 'r-PredictedCounts': [pearsonR_NNLS], 'p-value-PredictedCounts': [pearsonP_NNLS]})
        rmse_results = pd.concat([rmse_results, rmse_row], ignore_index=True)
    
    # Calculate RMSE for composition
    NNLS_df.iloc[:] *= 100
    rmse_values, r_values, p_values = [], [], []
    
    for index, row in NNLS_df.iterrows():
        sample_name = index
        true_values = groundtruth.loc[sample_name].values
        rmse = np.sqrt(mean_squared_error(true_values, row.values))
        r, p = stats.pearsonr(true_values, row.values)
        rmse_values.append(rmse)
        r_values.append(r)
        p_values.append(p)
    
    NNLS_df['RMSE-Composition'] = rmse_values
    NNLS_df['r-Composition'] = r_values
    
    rmse_results.set_index('Sample', inplace=True)
    NNLS_df['RMSE-PredictedCounts'] = rmse_results['RMSE-PredictedCounts']
    NNLS_df['r-PredictedCounts'] = rmse_results['r-PredictedCounts']
    NNLS_df = NNLS_df.round(3)
    
    # Construct output filename
    input_filename = os.path.basename(data_path)
    output_filename = f"NNLS_{input_filename}"
    output_path = os.path.join(output_dir, output_filename)
    
    # Save output
    NNLS_df.to_csv(output_path, sep="\t", index=True, header=True)
    
    print(f"Deconvolution results saved to: {output_path}")


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
    
    print(f"Running NNLS for {basis_path} -> Output: {output_dir}")
    
    # Run the deconvolution function
    nnls_deconvolution(
        data_path=data_path,
        basis_path=basis_path_full,
        groundtruth_path=groundtruth_path,
        output_dir=output_dir
    )

print("All NNLS deconvolution tasks completed.")
