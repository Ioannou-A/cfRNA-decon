## Script to merge the two datasets (Tabula sapiesn scRNA and Human Brain Atlas snRNA) using an approach to only keep the shared genes
import anndata as ad

# Define a mapping of column name variations to a standard name
column_name_map = {
    "cell_type": "cell_ontology_class",
    "donor_id": "donor",
    "self_reported_ethnicity_ontology_term_id": "ethnicity",
    "cell_type_ontology_term_id": "cell_ontology_id",
    "suspension_type": "method",
}

adata = ad.read_h5ad("COO-Matrix/HumanBrainAtlas-snRNA-V1/HBA-subsampled_processed.h5ad")
adata.obs = adata.obs.rename(columns={old: new for old, new in column_name_map.items() if old in adata.obs.columns})
adata.obs["batch"] = 'HBA'
adata.obs['anatomical_position'] = adata.obs['tissue']
adata.obs["tissue"] = "Brain" 
adata.obs["compartment"] = "Brain"

adata2 = ad.read_h5ad('COO-Matrix/TSP-V1/merged_TSP_V1.h5ad')
adata2.X = adata2.layers["decontXcounts"].copy()
adata2.obs["batch"] = 'TSP'

common_obs_cols = list(set(adata.obs.columns) & set(adata2.obs.columns))
adata.obs = adata.obs[common_obs_cols]
adata2.obs = adata2.obs[common_obs_cols]

# Outer also keeps non-shared
merged_adata = ad.concat([adata, adata2],axis = 0, join="inner")
merged_adata.layers['counts'] = merged_adata.X.copy()

# Save the processed AnnData object for future analysis
merged_adata.write_h5ad('COO-Matrix/HumanBrainAtlas-snRNA-V1/TSP-HBA-QC-Inner.h5ad')
