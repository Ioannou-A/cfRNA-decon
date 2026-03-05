## Script to merge the two datasets (Tabula sapiesn scRNA and Darmanis Brain scRNA data) using an approach to keep all genes
import anndata as ad

# Define a mapping of column name variations to a standard name
column_name_map = {
    "cell_type": "cell_ontology_class",
    "experiment_sample_name": "donor"
}

adata = ad.read_h5ad('COO-Matrix/DarmanisData/Darmanis-Brain-QC.h5ad')
adata.obs = adata.obs.rename(columns={old: new for old, new in column_name_map.items() if old in adata.obs.columns})
adata.obs["batch"] = 'DA'
adata.obs['anatomical_position'] = adata.obs['tissue']
adata.obs["tissue"] = "Brain" 
adata.obs["compartment"] = "Brain"
adata.obs["ethnicity"] = "Unknown"

# Filter the data to exclude cell types that start with 'fetal_' (to keep only adult samples)  or are 'hybrid' (unopure cell populations)
adata = adata[~(adata.obs["cell_ontology_class"].str.startswith("fetal_") | (adata.obs["cell_ontology_class"] == "hybrid")), :]

adata2 = ad.read_h5ad('COO-Matrix/TSP-V1/merged_TSP_V1.h5ad')
adata2.X = adata2.layers["decontXcounts"].copy()
adata2.obs["batch"] = 'TSP'

common_obs_cols = list(set(adata.obs.columns) & set(adata2.obs.columns))
adata.obs = adata.obs[common_obs_cols]
adata2.obs = adata2.obs[common_obs_cols]

# Inner to keep only shared
merged_adata = ad.concat([adata, adata2],axis = 0, join="outer")
merged_adata.layers['counts'] = merged_adata.X.copy()

# Save the processed AnnData object for future analysis
merged_adata.write_h5ad('COO-Matrix/DarmanisData/TSP-BDa-merged-Outer.h5ad')