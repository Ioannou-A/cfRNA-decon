import os
import numpy as np
import pandas as pd
from sklearn.svm import NuSVR
from itertools import product
from joblib import Parallel, delayed

def fit_nusvr(sample, scaled_basis_np, c_val, nu_val):
    clf = NuSVR(C=c_val, nu=nu_val, kernel="linear")
    clf.fit(scaled_basis_np, sample)
    coefs = np.clip(clf.coef_, 0, None)
    return coefs.T

def process_sample_hyperparams(sample_vector, scaled_basis_np, sample_id, c_val, nu_val, coef_columns):
    coefs = fit_nusvr(sample_vector, scaled_basis_np, c_val, nu_val)
    coefs = np.array(coefs)
    coefs /= coefs.sum(axis=0, keepdims=True)
    preds_norm = scaled_basis_np @ coefs
    rmse_pred = np.sqrt(np.mean((sample_vector - preds_norm[:, 0]) ** 2))
    coefs *= 100
    return [sample_id, nu_val, c_val, rmse_pred] + list(coefs.flatten())

def run_sample_batch_parallel(scaled_data_path, scaled_basis_path, output_dir, start_index, end_index, n_jobs=4):
    os.makedirs(output_dir, exist_ok=True)

    print("Loading basis...")
    basis = pd.read_csv(scaled_basis_path, delimiter="\t", index_col=0)
    scaled_basis_np = basis.values
    coef_columns = list(basis.columns)

    print("Loading data...")
    data = pd.read_csv(scaled_data_path, delimiter="\t", index_col=0)
    sample_names = data.columns

    # Prepare list of jobs for parallel processing
    jobs = []
    nu_vals = [0.05, 0.1, 0.15, 0.25, 0.5, 0.75]
    c_vals = [10, 1, 0.75, 0.5, 0.1]

    for sample_index in range(start_index, min(end_index, len(sample_names))):
        sample_id = sample_names[sample_index]
        sample_vector = data[sample_id].values
        for c_val, nu_val in product(c_vals, nu_vals):
            jobs.append((sample_vector, scaled_basis_np, sample_id, c_val, nu_val, coef_columns))

    print(f"Running {len(jobs)} fits in parallel with {n_jobs} jobs...")
    results = Parallel(n_jobs=n_jobs)(delayed(process_sample_hyperparams)(*job) for job in jobs)

    # Convert results to DataFrame
    df = pd.DataFrame(results, columns=['Sample', 'nuValue', 'CValue', 'RMSE-PredictedCounts'] + coef_columns)

    # Save best result per sample based on RMSE-PredictedCounts
    for sample_id in df['Sample'].unique():
        df_sample = df[df['Sample'] == sample_id]
        best_row = df_sample.loc[df_sample['RMSE-PredictedCounts'].idxmin()]
        sample_id_clean = sample_id.replace(".h5ad", "")
        output_filename = f"nuSVR_CountsRMSE_Random_{sample_id_clean}.txt"
        output_path = os.path.join(output_dir, output_filename)
        best_row.to_frame().T.to_csv(output_path, sep="\t", index=False)
        print(f"Saved best result for sample: {sample_id_clean}")

    print("All samples processed.")

if __name__ == "__main__":
    task_id = int(os.environ.get("SGE_TASK_ID", "1"))
    samples_per_task = 1
    start_idx = (task_id - 1) * samples_per_task
    end_idx = start_idx + samples_per_task

    scaled_data_path = "COO-Decon-Noise/CIBERSORTx-Matrix_TSP-BDa_Outer_300_1500_10/Random_v2C-Noisy_phi3.0e+00_All-Counts_CIBERSORTx-Matrix_TSP-BDa_Outer_300_1500_10_scaled_mixture.txt"
    scaled_basis_path = "COO-Decon-Noise/CIBERSORTx-Matrix_TSP-BDa_Outer_300_1500_10/Random_v2C-Noisy_phi3.0e+00_All-Counts_CIBERSORTx-Matrix_TSP-BDa_Outer_300_1500_10_scaled_basis.txt"
    output_dir = "COO-Decon-Noise/Decon-COO-Results_v3_Noise_phi3_nuSVR/"

    run_sample_batch_parallel(scaled_data_path, scaled_basis_path, output_dir, start_idx, end_idx, n_jobs=4)