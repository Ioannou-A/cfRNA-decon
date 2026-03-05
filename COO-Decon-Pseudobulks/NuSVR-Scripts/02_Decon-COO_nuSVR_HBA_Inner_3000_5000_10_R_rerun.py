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
    """Run NuSVR for one (C, nu) combination and return RMSE + coefficients."""
    coefs = fit_nusvr(sample_vector, scaled_basis_np, c_val, nu_val)
    coefs = np.array(coefs)
    coefs /= coefs.sum(axis=0, keepdims=True)
    preds_norm = scaled_basis_np @ coefs
    rmse_pred = np.sqrt(np.mean((sample_vector - preds_norm[:, 0]) ** 2))
    coefs *= 100
    return [sample_id, nu_val, c_val, rmse_pred] + list(coefs.flatten())


if __name__ == "__main__":
    # Get array task ID (1–270)
    task_id = int(os.environ.get("SGE_TASK_ID", "1")) - 1

    # Samples to rerun (0-based indices from all_samples.txt)
    sample_indices = [312, 105, 145, 587, 189, 325, 26, 418, 376]

    # Hyperparameter grid
    c_vals = [10, 1, 0.75, 0.5, 0.1]
    nu_vals = [0.05, 0.1, 0.15, 0.25, 0.5, 0.75]
    hyperparam_pairs = list(product(c_vals, nu_vals))  # 30 combinations

    # Map array ID to (sample, hyperparam)
    sample_idx = task_id // len(hyperparam_pairs)
    hyper_idx = task_id % len(hyperparam_pairs)

    if sample_idx >= len(sample_indices):
        print(f"Task {task_id + 1} out of range for rerun list.")
        exit()

    sample_index = sample_indices[sample_idx]
    c_val, nu_val = hyperparam_pairs[hyper_idx]

    # File paths
    scaled_basis_path = "COO-Decon-Pseudobulks/CIBERSORTx-Matrix_TSP-HBA_Inner_3000_5000_10/Random_v2C_All-Counts_CIBERSORTx-Matrix_TSP-HBA_Inner_3000_5000_10_scaled_basis.txt"
    scaled_data_path = "COO-Decon-Pseudobulks/CIBERSORTx-Matrix_TSP-HBA_Inner_3000_5000_10/Random_v2C_All-Counts_CIBERSORTx-Matrix_TSP-HBA_Inner_3000_5000_10_scaled_mixture.txt"
    output_dir = "COO-Decon-Pseudobulks/CIBERSORTx-Matrix_TSP-HBA_Inner_3000_5000_10/"
    os.makedirs(output_dir, exist_ok=True)

    # Load data
    print(f"Task {task_id + 1}: sample_index={sample_index}, C={c_val}, nu={nu_val}")
    basis = pd.read_csv(scaled_basis_path, delimiter="\t", index_col=0)
    scaled_basis_np = basis.values
    coef_columns = list(basis.columns)

    data = pd.read_csv(scaled_data_path, delimiter="\t", index_col=0)
    sample_names = data.columns

    if sample_index >= len(sample_names):
        print(f"Sample index {sample_index} out of range.")
        exit()

    sample_id = sample_names[sample_index]
    sample_vector = data[sample_id].values

    # Run deconvolution for one (sample, C, ν)
    result = process_sample_hyperparams(sample_vector, scaled_basis_np, sample_id, c_val, nu_val, coef_columns)

    # Save output
    columns = ['Sample', 'nuValue', 'CValue', 'RMSE-PredictedCounts'] + coef_columns
    df = pd.DataFrame([result], columns=columns)
    sample_id_clean = sample_id.replace(".h5ad", "")
    output_filename = f"nuSVR_Rerun_{sample_id_clean}_C{c_val}_nu{nu_val}.txt"
    output_path = os.path.join(output_dir, output_filename)
    df.to_csv(output_path, sep="\t", index=False)

    print(f"Saved result for {sample_id_clean} (C={c_val}, nu={nu_val}) -> {output_filename}")
