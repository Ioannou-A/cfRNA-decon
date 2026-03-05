import os
import glob
import scanpy as sc

# Get the current working directory
cwd = os.getcwd()

# Define input and output directories
input_dir = os.path.join(cwd, "00_Raw-h5ad")
output_dir = os.path.join(cwd, "01_Modified-h5ad")

# Create output directory if it doesn't exist
os.makedirs(output_dir, exist_ok=True)

# Find all H5 files in the specified input directory
h5ad_files = glob.glob(os.path.join(input_dir, "*.h5ad"))

for h5ad_file in h5ad_files:
    print(f"Processing {h5ad_file}...")

    # Load the AnnData object
    filtered_data = sc.read_h5ad(h5ad_file)

    # Deleting from obsp
    for key in ['connectivities', 'distances']:
        if key in filtered_data.obsp:
            del filtered_data.obsp[key]
    # Deleting from varm
    if 'PCs' in filtered_data.varm:
        del filtered_data.varm['PCs']
    # Deleting from var
    for key in ['pct_dropout_by_counts', 'n_cells_by_counts', 'mean_counts', 'total_counts', 'mean', 'std']:
        if key in filtered_data.layers:
            del filtered_data.layers[key]
    # Deleting from obsm
    for key in ['X_pca', 'X_scvi', 'X_tissue_uncorrected_umap', 'X_umap',
                'X_umap_scvi_full_donorassay', 'X_umap_tissue_scvi_donorassay', 'X_uncorrected_umap']:
        if key in filtered_data.obsm:
            del filtered_data.obsm[key]
    # Deleting from uns
    for key in ['_scvi_manager_uuid', '_scvi_uuid', '_training_mode', 'age_colors', 'assay_colors',
                'compartment_colors', 'donor_colors', 'leiden', 'log1p', 'method_colors',
                'neighbors', 'pca', 'sex_colors', 'tissue_colors', 'umap']:
        if key in filtered_data.uns:
            del filtered_data.uns[key]
    # Deleting from obs
    for key in ['scvi_leiden_res05_tissue', 'n_genes_by_counts', 'total_counts', 'total_counts_mt',
                'pct_counts_mt', 'total_counts_ercc', 'pct_counts_ercc', '_scvi_batch', '_scvi_labels',
                'scvi_leiden_donorassay_full']:
        if key in filtered_data.obs:
            del filtered_data.obs[key]
    # Deleting specific layers
    for key in ['scale_data', 'log_normalized']:
        if key in filtered_data.layers:
            del filtered_data.layers[key]

    # Construct output filename
    base_filename = os.path.splitext(os.path.basename(h5ad_file))[0]
    modified_filename = os.path.join(output_dir, f"{base_filename}_modified.h5ad")
    # Save modified data
    filtered_data.write(modified_filename)
    print(f"Saved modified data to: {modified_filename}")

