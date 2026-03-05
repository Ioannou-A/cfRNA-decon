import os
import numpy as np
import pandas as pd
import scanpy as sc
import scipy.sparse as sp

def add_nb_noise_after_norm(X, phi_bulk, rng):
    """
    Add Negative Binomial (Gamma–Poisson) noise to per-cell normalized data.
    Works directly on per-cell normalized matrices (each cell sum≈1e4).
    """
    if sp.issparse(X):
        X = X.tocsr()
    else:
        X = np.asarray(X)

    n_cells, n_genes = X.shape
    noisy = np.zeros((n_cells, n_genes), dtype=np.float64)

    for i in range(n_cells):
        expr = X[i, :].toarray().ravel() if sp.issparse(X) else X[i, :]
        mu = np.maximum(expr, 1e-12)

        # Per-gene NB variance: Var = mu + phi_bulk * mu^2
        shape = 1.0 / np.maximum(phi_bulk, 1e-12)
        scale = mu * phi_bulk
        lam = rng.gamma(shape, scale)
        noisy[i, :] = rng.poisson(lam)

    return noisy


def generate_noisy_pseudo_bulk_nb_normed(input_dir, output_prefix,
                                         phi_bulk_grid=(0.0, 1e-6, 5e-6, 1e-5, 5e-5),
                                         seed_base=42):
    """
    Keep same logic as your baseline (normalize each cell, then sum, then CPM),
    but insert mild Negative Binomial noise at the per-cell stage.
    Ensures the same noise pattern across φ levels by fixing the seed per file.
    Writes one full multi-sample counts matrix per φ level.
    """
    files = [f for f in os.listdir(input_dir) if f.endswith(".h5ad")]
    print(f"Found {len(files)} .h5ad files")

    # --- Preload all .h5ad files once to avoid repeated disk reads
    preloaded = []
    for file_idx, file in enumerate(files):
        adata = sc.read_h5ad(os.path.join(input_dir, file))
        adata.X = adata.layers["decontXcounts"]

        # Per-cell normalization (as in baseline)
        sc.pp.normalize_total(adata)

        # Store necessary info
        preloaded.append((file_idx, file, adata.X, adata.var_names))

    # --- Iterate over φ values (noise levels)
    for phi_bulk in phi_bulk_grid:
        print(f"\n=== φ = {phi_bulk:.1e} ===")
        all_results = pd.DataFrame()

        # --- For each sample (.h5ad)
        for file_idx, file, X, var_names in preloaded:
            print(f"  Processing {file} at φ={phi_bulk:.1e}")

            # Fixed RNG per file → same noise field across φ levels
            rng = np.random.default_rng(seed_base + file_idx)

            # Apply per-cell NB noise
            if phi_bulk > 0:
                noisy_X = add_nb_noise_after_norm(X, phi_bulk, rng)
            else:
                noisy_X = X.copy()  # deterministic "no-noise" baseline

            # --- Sum across cells to create pseudo-bulk
            summed_data = noisy_X.sum(axis=0)
            if sp.issparse(summed_data):
                summed_data = np.asarray(summed_data)
            summed_data = np.ravel(summed_data)

            total_sum = summed_data.sum()
            if total_sum <= 0:
                print(f"Warning: total sum = 0 for {file}")
                continue

            # --- CPM normalization
            cpm_data = (summed_data / total_sum) * 1e6

            # Store this sample’s CPM as a column in the output matrix
            df = pd.DataFrame(cpm_data, columns=[file], index=var_names)
            all_results = pd.concat([all_results, df], axis=1)

        # --- Write one full matrix per φ value
        out_file = f"{output_prefix}_phi{phi_bulk:.1e}_All-Counts.txt"
        all_results.fillna(0, inplace=True)
        all_results.astype(float).to_csv(out_file, sep="\t")
        print(f"Saved noisy pseudo-bulks for φ={phi_bulk:.1e} → {out_file}")


# --- Run ---
input_dir = "COO-Simulated/02_Pseudo-bulk/Random_v2C_New"
output_dir = "COO-Simulated/02_Pseudo-bulk/Random_v2C-Noisy_Final3/"
output_prefix = os.path.join(output_dir, "Random_v2C-Noisy")
os.makedirs(output_dir, exist_ok=True)

# Define the phi values to sweep across (noise ladder)
phi_bulk_grid = [1, 2, 3, 5, 10, 20, 30, 50, 100]

# Generate noisy pseudo-bulks across all noise levels
generate_noisy_pseudo_bulk_nb_normed(
    input_dir,
    output_prefix,
    phi_bulk_grid=phi_bulk_grid,
    seed_base=42
)
