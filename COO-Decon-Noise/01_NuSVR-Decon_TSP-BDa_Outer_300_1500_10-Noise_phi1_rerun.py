import os
import numpy as np
import pandas as pd
from sklearn.svm import NuSVR
from itertools import product

def fit_nusvr(sample, scaled_basis_np, c_val, nu_val):
    """Fit NuSVR with given C and nu, return non-negative coefficients."""
    clf = NuSVR(C=c_val, nu=nu_val, kernel="linear")
    clf.fit(scaled_basis_np, sample)
    coefs = np.clip(clf.coef_, 0, None)
    return coefs.T

def process_sample_hyperparams(sample_vector, scaled_basis_np, sample_id, c_val, nu_val, coef_columns):
    """Run NuSVR on one (C, nu) pair and compute RMSE + proportions."""
    coefs = fit_nusvr(sample_vector, scaled_basis_np, c_val, nu_val)
    coefs = np.array(coefs)

    # Normalize weights
    coefs /= coefs.sum(axis=0, keepdims=True)

    preds_norm = scaled_basis_np @ coefs
    rmse_pred = np.sqrt(np.mean((sample_vector - preds_norm[:, 0]) ** 2))

    # Convert to percent
    coefs *= 100

    return [sample_id, nu_val, c_val, rmse_pred] + list(coefs.flatten())


if __name__ == "__main__":

    # Array task ID (1–420)
    task_id = int(os.environ.get("SGE_TASK_ID", "1")) - 1

    # Samples that failed originally (0-based indices)
    sample_indices = [
        379, 205, 697, 578, 139, 787, 627,
        644, 346, 461, 323, 26, 804, 23
    ]

    # Hyperparameter grid (30 combinations)
    c_vals = [10, 1, 0.75, 0.5, 0.1]
    nu_vals = [0.05, 0.1, 0.15, 0.25, 0.5, 0.75]
    hyperparam_pairs = list(product(c_vals, nu_vals))

    sample_idx = task_id // len(hyperparam_pairs)
    hyper_idx = task_id % len(hyperparam_pairs)

    if sample_idx >= len(sample_indices):
        print(f"Task {task_id+1} is out of range.")
        exit()

    sample_index = sample_indices[sample_idx]
    c_val, nu_val = hyperparam_pairs[hyper_idx]

    # Input files
    scaled_data_path = "COO-Decon-Noise/CIBERSORTx-Matrix_TSP-BDa_Outer_300_1500_10/Random_v2C-Noisy_phi1.0e+00_All-Counts_CIBERSORTx-Matrix_TSP-BDa_Outer_300_1500_10_scaled_mixture.txt"
    scaled_basis_path = "COO-Decon-Noise/CIBERSORTx-Matrix_TSP-BDa_Outer_300_1500_10/Random_v2C-Noisy_phi1.0e+00_All-Counts_CIBERSORTx-Matrix_TSP-BDa_Outer_300_1500_10_scaled_basis.txt"
    output_dir = "COO-Decon-Noise/Decon-COO-Results_v3_Noise_phi1_nuSVR/"
    os.makedirs(output_dir, exist_ok=True)

    # Load basis + data
    basis = pd.read_csv(scaled_basis_path, sep="\t", index_col=0)
    scaled_basis_np = basis.values
    coef_columns = list(basis.columns)

    data = pd.read_csv(scaled_data_path, sep="\t", index_col=0)
    sample_names = data.columns

    if sample_index >= len(sample_names):
        print("Sample index out of range.")
        exit()

    sample_id = sample_names[sample_index]
    sample_vector = data[sample_id].values

    print(f"Running: sample={sample_id} index={sample_index}  C={c_val} nu={nu_val}")

    result = process_sample_hyperparams(
        sample_vector, scaled_basis_np, sample_id, c_val, nu_val, coef_columns
    )

    # Save
    out_cols = ['Sample', 'nuValue', 'CValue', 'RMSE-PredictedCounts'] + coef_columns
    df = pd.DataFrame([result], columns=out_cols)

    sample_id_clean = sample_id.replace(".h5ad", "")
    outname = f"nuSVR_Rerun_NoisePhi1_{sample_id_clean}_C{c_val}_nu{nu_val}.txt"
    df.to_csv(os.path.join(output_dir, outname), sep="\t", index=False)

    print(f"Saved: {outname}")