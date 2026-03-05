import os
import numpy as np
import pandas as pd
from sklearn.svm import NuSVR
from itertools import product


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


if __name__ == "__main__":
    task_id = int(os.environ.get("SGE_TASK_ID", "1")) - 1

    sample_indices = [
        312, 154, 41, 126, 141, 101, 821, 404, 522, 804, 23, 422
    ]
    
    c_vals = [10, 1, 0.75, 0.5, 0.1]
    nu_vals = [0.05, 0.1, 0.15, 0.25, 0.5, 0.75]
    hyperparam_pairs = list(product(c_vals, nu_vals))

    sample_idx = task_id // len(hyperparam_pairs)
    hyper_idx = task_id % len(hyperparam_pairs)

    if sample_idx >= len(sample_indices):
        print(f"Task {task_id+1} out of range.")
        exit()

    sample_index = sample_indices[sample_idx]
    c_val, nu_val = hyperparam_pairs[hyper_idx]

    scaled_data_path = "COO-Decon-Noise/CIBERSORTx-Matrix_TSP-BDa_Outer_300_1500_10/Random_v2C-Noisy_phi1.0e+02_All-Counts_CIBERSORTx-Matrix_TSP-BDa_Outer_300_1500_10_scaled_mixture.txt"
    scaled_basis_path = "COO-Decon-Noise/CIBERSORTx-Matrix_TSP-BDa_Outer_300_1500_10/Random_v2C-Noisy_phi1.0e+02_All-Counts_CIBERSORTx-Matrix_TSP-BDa_Outer_300_1500_10_scaled_basis.txt"
    output_dir = "COO-Decon-Noise/Decon-COO-Results_v3_Noise_phi100_nuSVR/"
    os.makedirs(output_dir, exist_ok=True)

    basis = pd.read_csv(scaled_basis_path, sep="\t", index_col=0)
    scaled_basis_np = basis.values
    coef_columns = list(basis.columns)

    data = pd.read_csv(scaled_data_path, sep="\t", index_col=0)
    sample_names = data.columns

    sample_id = sample_names[sample_index]
    sample_vector = data[sample_id].values

    print(f"Running sample={sample_id}, index={sample_index}, C={c_val}, nu={nu_val}")

    result = process_sample_hyperparams(
        sample_vector, scaled_basis_np, sample_id, c_val, nu_val, coef_columns
    )

    out_cols = ['Sample', 'nuValue', 'CValue', 'RMSE-PredictedCounts'] + coef_columns
    df = pd.DataFrame([result], columns=out_cols)

    sample_clean = sample_id.replace(".h5ad", "")
    outfile = f"nuSVR_Rerun_Noisephi100_{sample_clean}_C{c_val}_nu{nu_val}.txt"

    df.to_csv(os.path.join(output_dir, outfile), sep="\t", index=False)

    print(f"Saved {outfile}")
