# Command to merge the neurons and non-neurons h5ad file of the Human Brain Cell Atlas v1.0 from the https://data.humancellatlas.org/hca-bio-networks/nervous-system/atlases/brain-v1-0
import scanpy as sc
import anndata as ad

noneurons_HBA = sc.read_h5ad('99f27be8-9fac-451e-9723-9e4c7191589e.h5ad')
neurons_HBA = sc.read_h5ad('c2f66cd5-4ff4-4578-876c-55783a57cf8f.h5ad')

# Concatenate the AnnData objects using anndata.concat
merged_HBA = ad.concat([neurons_HBA, noneurons_HBA], join="outer")

# Save the merged dataset
merged_HBA.write_h5ad('COO-Matrix/HumanBrainAtlas-snRNA-V1/HBA-merged.h5ad')

## Script to rename the HBA (which uses ENSG) to the TS gene name identifiers
adata2 = sc.read_h5ad('COO-Matrix/TSP-V1/merged_TSP_V1.h5ad')

# Create the dictionary with the index and ensembl_id contents
ensembl_dict = dict(zip(adata2.var.index, adata2.var['ensembl_id']))
# Polish the ENSG IDs by removing the information after the dot
ensembl_dict_polished = {key: value.split('.')[0] for key, value in ensembl_dict.items()}

# Rename the var indexes of the merged file (merged_HBA) using the dictionary 
merged_HBA.var.index = merged_HBA.var.index.to_series().apply(lambda x: next((k for k, v in ensembl_dict_polished.items() if v == x), x))

## Script to obtain only 200k cells from the human brain atlas as it contains millions of cells.
# Read the data and sample
sc.pp.subsample(merged_HBA, n_obs=200000, random_state=42)
merged_HBA.write_h5ad('COO-Matrix/HumanBrainAtlas-snRNA-V1/HBA-subsampled_200k.h5ad')




