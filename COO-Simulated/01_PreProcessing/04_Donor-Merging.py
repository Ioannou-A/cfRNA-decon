import scanpy as sc
import anndata
import glob
import os
import pandas as pd

# Define donors
donors = ["TSP21", "TSP25", "TSP27"]

# Define input and output directories (relative to the current working directory)
input_dir = "./Individual-QC-h5ad"
output_dir = "./04_Merged-PerDonor-h5ad"

# Create output directory if it doesn't exist
os.makedirs(output_dir, exist_ok=True)

# Process each donor separately
for donor in donors:
    # Find all h5ad files for the donor
    donor_files = sorted(glob.glob(f"{input_dir}/{donor}_*_10X_processed.h5ad"))

    if not donor_files:
        print(f"No files found for {donor}, skipping...")
        continue

    print(f"Found {len(donor_files)} files for {donor}.")

    # Load datasets
    adatas = [sc.read_h5ad(f) for f in donor_files]

    # Ensure unique categorical values before merging
    for i, adata in enumerate(adatas):
        tissue_label = donor_files[i].split("_")[1]  # Extract tissue name from filename
        adata.obs["tissue"] = tissue_label  # Assign tissue name

        # Convert categorical columns to strings and ensure uniqueness
        for col in adata.obs.select_dtypes(["category"]).columns:
            adata.obs[col] = adata.obs[col].astype(str)
            adata.obs[col] = pd.Categorical(adata.obs[col])  # Convert back to categorical

    # Concatenate while ensuring shared genes/features
    merged_adata = anndata.concat(adatas, join="outer", label="tissue", keys=[f.split("_")[1] for f in donor_files])

    # Save merged dataset
    output_file = f"{output_dir}/{donor}_merged.h5ad"
    merged_adata.write_h5ad(output_file)

    print(f"Merged {len(donor_files)} files for {donor} and saved to {output_file}.")

