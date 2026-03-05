import os
import pandas as pd
import numpy as np
from sklearn import preprocessing
from sklearn.svm import NuSVR
from joblib import Parallel, delayed
from itertools import product

def nusvr_deconvolution(data_path, basis_path, output_dir):
    os.makedirs(output_dir, exist_ok=True)
    
    print("Loading data...")
    data = pd.read_csv(data_path, delimiter="\t", low_memory=False, comment='#')
    data.set_index(data.columns[0], inplace=True)
    basis = pd.read_csv(basis_path, delimiter="\t", low_memory=False, index_col=0)

    print("Aligning and scaling data...")
    common_indexes = data.index.intersection(basis.index)
    scaled_basis = preprocessing.scale(basis.loc[common_indexes].values)
    scaled_data = preprocessing.scale(data.loc[common_indexes].values)

    scaled_basis_df = pd.DataFrame(scaled_basis, index=common_indexes, columns=basis.columns)
    scaled_data_df = pd.DataFrame(scaled_data, index=common_indexes, columns=data.columns)
    
    scaled_basis_np = scaled_basis_df.values
    scaled_data_np = scaled_data_df.values

    nu_vals = [0.05, 0.1, 0.15, 0.25, 0.5, 0.75]
    c_vals = [10, 1, 0.75, 0.5, 0.1]
    
    def fit_nusvr(sample, scaled_basis_np, c_val, nu_val):
        clf = NuSVR(C=c_val, nu=nu_val, kernel="linear")
        clf.fit(scaled_basis_np, sample)
        coefs = np.clip(clf.coef_, 0, None)
        return coefs.T
    
    def process_hyperparams_sample(c_val, nu_val, sample_index):
        print(f"Processing hyperparameters: C={c_val}, nu={nu_val}, sample={sample_index}")
        coefs = fit_nusvr(scaled_data_np[:, sample_index], scaled_basis_np, c_val, nu_val)
        coefs = np.array(coefs)
        
        # Normalize coefficients
        print(f"Before normalization: coefs shape: {coefs.shape}, sum: {coefs.sum(axis=0)}")
        coefs /= coefs.sum(axis=0, keepdims=True)
        print(f"After normalization: sum: {coefs.sum(axis=0)}")
        
        # Compute predicted counts
        preds_norm = scaled_basis_np @ coefs

        # RMSE for predicted counts
        rmse_values = np.sqrt(np.mean((scaled_data_np[:, sample_index] - preds_norm[:, 0]) ** 2))

        # Convert to percentages
        coefs *= 100

        return [scaled_data_df.columns[sample_index], nu_val, c_val, rmse_values] + list(coefs.flatten())

    # Run in parallel over hyperparameter combinations and samples
    results_nested = Parallel(n_jobs=-1, backend="loky")(
        delayed(process_hyperparams_sample)(c_val, nu_val, sample_index)
        for c_val, nu_val, sample_index in product(c_vals, nu_vals, range(scaled_data_np.shape[1]))
    )
    
    print("Saving results...")
    coef_columns = list(scaled_basis_df.columns)
    df_results = pd.DataFrame(results_nested, columns=['Sample', 'nuValue', 'CValue', 'RMSE-PredictedCounts'] + coef_columns)
    best_predicted_counts = df_results.loc[df_results.groupby('Sample')['RMSE-PredictedCounts'].idxmin()]

    output_filename = os.path.splitext(os.path.basename(data_path))[0]
    best_predicted_counts.to_csv(os.path.join(output_dir, f"nuSVR_CountsRMSE_{output_filename}.txt"), sep="\t", index=False)
    
    print("NuSVR deconvolution completed.")

data = "TOO-Decon/20250616_All-Tissues-NoDup_Random_Simulated_v2_Counts.txt"
basis = "TOO-Matrix/TOO-Matrices_Renamed/CIBERSORTx-TOO-Matrix_2Median_300_500/CIBERSORTx_20250405_PhenotypeClass_LessTissueV2_2Median.CIBERSORTx_20250405_GeneID_LessTissueV2_2Median.withGTFNames.txt"
output = "TOO-Decon/Decon-Results_2Median_300_500-Random_TOOv2_1000"

nusvr_deconvolution(data, basis, output)
