# %%

"""
Adapted by Sevahn Vorperian, Quake Lab
Modified by Ioannou A
Sample up to 100 of each cell type to be used as a reference sample for ReDeconv normalisation and deconvolution 
from the TSP-BDa Inner matrix.
This also saves the metadata (donor information etc)
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
adataName = "TSP-BDa-merged-Inner.h5ad"
cellAnnotCol = "cell_ontology_class"
fend = "TSP-BDa_Inner_100each.txt"
clusters_path = "COO-Matrix/TSP-BDa_Inner_All-Compartments_clusters.csv"

# Load the file
adata = sc.read_h5ad(basePath + adataName)
adata.X = adata.layers["counts"]
df = pd.read_csv(clusters_path, index_col=0)

# Filter data
adata = adata[adata.obs["tissue"] != "Eye"]
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

# Track sampled cell IDs and metadata
sampled_cell_ids = []
barcode_to_merged_category = {}

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

    sampled_barcodes = obsThisCell.obs.iloc[indexSample].index.tolist()
    sampled_cell_ids.extend(sampled_barcodes)

    # Store merged category for each barcode
    for bc in sampled_barcodes:
        barcode_to_merged_category[bc] = category_mapping[cell]

    thisCellDF = pd.DataFrame(data=data, index=adata.var_names, columns=sampled_barcodes)
    downsampledCells = downsampledCells.join(thisCellDF)

# Final cleanup
print(f"Sampled cell IDs: {len(sampled_cell_ids)}")

downsampledCells = downsampledCells.loc[~(downsampledCells == 0).all(axis=1)]
downsampledCells = downsampledCells.dropna(axis=1, how='all')
downsampledCells = downsampledCells.fillna(0)

# Save outputs
fend = fend.replace(".txt", f"_seed{SEED}-ReDeconv.txt")
downsampledCells.to_csv(fend, index=True, sep='\t', header=True)

# Metadata output
if sampled_cell_ids:
    # Build sampled metadata from adata.obs using sampled barcodes
    sampled_metadata = adata.obs.loc[sampled_cell_ids, ['donor', 'tissue', cellAnnotCol]].copy()
    sampled_metadata.index.name = 'barcode'

    # Map original cell types to merged group using category_mapping.
    # If a mapping is not found, fall back to the original cell type.
    sampled_metadata['merged_cell_type'] = sampled_metadata[cellAnnotCol].map(category_mapping).fillna(sampled_metadata[cellAnnotCol])

    # Build the default sample from donor and tissue
    default_sample = sampled_metadata['donor'].astype(str) + "_" + sampled_metadata['tissue'].astype(str)

    # Handle special case for barcodes starting with 'TSP'
    barcodes = sampled_metadata.index.astype(str)
    is_tsp = barcodes.str.startswith('TSP')
    barcodes_series = pd.Series(barcodes, index=sampled_metadata.index)
    tsp_sample_series = barcodes_series.str.split('_').apply(
        lambda parts: '_'.join(parts[:3]) if len(parts) >= 3 else '_'.join(parts)
    )

    sampled_metadata['sample'] = default_sample
    sampled_metadata.loc[is_tsp, 'sample'] = tsp_sample_series[is_tsp].values

    # Keep only required columns
    sampled_metadata = sampled_metadata[['merged_cell_type', 'sample']]

    # Save metadata
    metadata = fend.replace(".txt", "_metadata.txt")
    sampled_metadata.to_csv(metadata, sep="\t")
    print(f"Saved metadata with 'merged_cell_type' and 'sample' to: {metadata}")
else:
    print("No cells were sampled.")


