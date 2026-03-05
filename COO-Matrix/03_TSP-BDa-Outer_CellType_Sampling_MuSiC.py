# %%

"""
Adapted by Sevahn Vorperian, Quake Lab
sample a specific number of cell type to be used as a reference sample for MuSiC deconvolution from the TSP-BDa matrix.
This also saves the metadata (donor and tissue information for MuSiC deconvolution). Used to select 50 and 100 cells per cell type.

Modified to:
 - add 'cell_group' column (merged group from clusters mapping)
 - set 'sample' column such that:
     - if barcode starts with 'TSP', use the first 3 components of the barcode split by '_'
       (e.g. 'TSP14_SalivaryGland_Sublingual_10X_1_1_AGCAT...' -> 'TSP14_SalivaryGland_Sublingual')
     - otherwise use donor_tissue as before
"""
import numpy as np
import scanpy as sc
import pandas as pd
from random import sample, seed
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import seaborn as sns
import os
from scipy.sparse import issparse

# Set a seed for reproducibility
SEED = 42
seed(SEED)

basePath = "COO-Matrix/DarmanisData/"
adataName = "TSP-BDa-merged-Outer.h5ad"
cellAnnotCol = "cell_ontology_class"
fend = "TSP-BDa_Outer_100each.txt"
clusters_path = "COO-Matrix/TSP-BDa_Outer_All-Compartments_clusters.csv"

# Load the file
adata = sc.read_h5ad(basePath + adataName)
adata.X = adata.layers["counts"]
df = pd.read_csv(clusters_path, index_col=0)

# Filter data
adata = adata[adata.obs["tissue"] != "Eye"]
# Rename the endothelial annotation of Darmanis Brain to endothelial cell to be incorporated with those of the TSP
adata.obs[cellAnnotCol] = adata.obs[cellAnnotCol].replace({"endothelial": "endothelial cell"})

# Create a list of all unique cell types
goodAnnot = set()
category_mapping = {}

# Build mapping from individual types to merged categories
for merged_category in df.index:
    individual_types = merged_category.split('/')
    for cell_type in individual_types:
        cleaned_cell_type = cell_type.strip()
        goodAnnot.add(cleaned_cell_type)
        category_mapping[cleaned_cell_type] = merged_category

goodAnnot = sorted(goodAnnot)
downsampledCells = pd.DataFrame(index=adata.var_names)

# Track sampled cell IDs for metadata
sampled_cell_ids = []
cell_barcodes = []

for cell in goodAnnot:
    obsThisCell = adata[adata.obs[cellAnnotCol] == cell]
    numObs = obsThisCell.shape[0]
    maxObs = 100

    print(f"Processing cell type: {cell}, found {numObs} cells")

    if numObs >= maxObs:
        indexSample = sample(range(0, numObs), maxObs)
    else:
        indexSample = range(0, numObs)

    data = obsThisCell.X[indexSample, :].T
    if issparse(data):
        data = data.toarray()

    # Keep original label as column names (these may be non-unique)
    cellLabs = list(obsThisCell.obs.iloc[indexSample][cellAnnotCol])
    thisCellDF = pd.DataFrame(data=data, index=adata.var_names, columns=cellLabs)

    print(cell, " ", thisCellDF.shape)
    print('all = ', downsampledCells.shape)
    downsampledCells = downsampledCells.join(thisCellDF)

    sampled_ids = obsThisCell.obs.iloc[indexSample].index.tolist()
    sampled_cell_ids.extend(sampled_ids)
    cell_barcodes.extend(sampled_ids)

# Final checks and cleanup
print(f"Sampled cell IDs: {len(sampled_cell_ids)}")

downsampledCells = downsampledCells.loc[~(downsampledCells == 0).all(axis=1)]
downsampledCells = downsampledCells.dropna(axis=1, how='all')
downsampledCells = downsampledCells.fillna(0)

# Rename columns using mapping to match the new groups of cell types
downsampledCells.columns = [category_mapping.get(col, col) for col in downsampledCells.columns]

# Save outputs
fend = fend.replace(".txt", f"_seed{SEED}.txt")
downsampledCells.to_csv(fend, index=True, sep='\t', header=True)

if sampled_cell_ids:
    # Build sampled metadata from adata.obs using sampled barcodes
    sampled_metadata = adata.obs.loc[sampled_cell_ids, ['donor', 'tissue', cellAnnotCol]].copy()
    sampled_metadata.index.name = 'barcode'

    # Add original cell type column (explicit name)
    sampled_metadata['cell_type'] = sampled_metadata[cellAnnotCol].astype(str)

    # Map original cell types to merged group using category_mapping.
    # If a mapping is not found, fall back to the original cell type.
    sampled_metadata['cell_group'] = sampled_metadata['cell_type'].map(category_mapping).fillna(sampled_metadata['cell_type'])

    # Build the default sample from donor and tissue
    default_sample = sampled_metadata['donor'].astype(str) + "_" + sampled_metadata['tissue'].astype(str)

    # For barcodes starting with 'TSP', use the first 3 components of the barcode split by '_'
    # Otherwise, use the default sample (donor_tissue).
    # This operation uses the index (barcode strings).
    barcodes = sampled_metadata.index.astype(str)
    is_tsp = barcodes.str.startswith('TSP')

    # Extract first 3 components safely (if fewer than 3 components exist, join whatever is there)
    barcodes_series = pd.Series(barcodes, index=sampled_metadata.index)  # convert Index to Series
    tsp_sample_series = barcodes_series.str.split('_').apply(
        lambda parts: '_'.join(parts[:3]) if len(parts) > 0 else ''
    )
    
    # Compose final 'sample' column
    sampled_metadata['sample'] = default_sample
    sampled_metadata.loc[is_tsp, 'sample'] = tsp_sample_series[is_tsp].values

    # Optionally drop the raw cellAnnotCol column (we already copied it to 'cell_type')
    sampled_metadata = sampled_metadata.drop(columns=[cellAnnotCol])

    metadata = fend.replace(".txt", "_metadata.txt")
    sampled_metadata.to_csv(metadata, sep="\t")
    print(f"Saved metadata with 'sample' and 'cell_group' to: {metadata}")
else:
    print("No cells were sampled.")
