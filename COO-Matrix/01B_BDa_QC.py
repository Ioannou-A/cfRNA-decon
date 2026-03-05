import scanpy as sc
import numpy as np

## Script to filter and QC the Darmanis Brain scRNA data. This is the same way as was done for the TSP V1 matrix

# Read the data and sample
sampled_HBA = sc.read_h5ad('COO-Matrix/DarmanisData/Darmanis-Brain.h5ad')

# Compute quality control metrics and log-transform counts
sampled_HBA.var["mt"] = sampled_HBA.var_names.str.startswith("MT-")
sc.pp.calculate_qc_metrics(sampled_HBA, qc_vars=["mt"], inplace=True, log1p=False)
# Identify mitochondrial genes
mito_genes = sampled_HBA.var_names.str.startswith("MT-")  # Adjust based on annotation
non_mito_genes = (sampled_HBA.X[:, ~mito_genes] > 0).sum(axis=1).A1 if isinstance(sampled_HBA.X, np.matrix) else (sampled_HBA.X[:, ~mito_genes] > 0).sum(axis=1)
sampled_HBA.obs["non_mito_genes"] = non_mito_genes 

# Compute non-mitochondrial counts
sampled_HBA.obs["non_mito_counts"] = sampled_HBA.obs["total_counts"] - sampled_HBA.obs["total_counts_mt"]
sc.pp.scrublet(sampled_HBA)

# Pre-filter cells to remove those with very low non-mitochondrial counts & genes
sampled_HBA = sampled_HBA[(sampled_HBA.obs["non_mito_counts"] >= 2500) & (sampled_HBA.obs["non_mito_genes"] >= 200) & (sampled_HBA.obs["predicted_doublet"] == False)].copy()

# Save the processed AnnData object for future analysis
sampled_HBA.write_h5ad('COO-Matrix/DarmanisData/Darmanis-Brain-QC.h5ad')


