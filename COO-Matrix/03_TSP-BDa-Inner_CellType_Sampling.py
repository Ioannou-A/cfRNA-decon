# %%

"""
Adapted by Sevahn Vorperian, Quake Lab
sample up to 25 of each cell type for basis matrix generation with CIBERSORTx
from the TSP-BDa matrix  
"""
import numpy as np
import scanpy as sc
import pandas as pd
from random import sample
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import seaborn as sns
import os
from scipy.sparse import issparse

basePath = "COO-Matrix/DarmanisData/"
adataName = "TSP-BDa-merged-Inner.h5ad"
cellAnnotCol = "cell_ontology_class"
fend = "TSP-BDa_Inner_25each.txt"
clusters_path = "COO-Matrix/TSP-BDa_Inner_All-Compartments_clusters.csv"

# Load the file
adata = sc.read_h5ad(basePath + adataName) 
adata.X = adata.layers["counts"]
df = pd.read_csv(clusters_path, index_col=0)

# Filter data
adata = adata[adata.obs["tissue"] != "Eye"]
# Rename the endothelial annotation of Darmanis Brain to endothelial cell to be incorporate with those of the TSP
adata.obs[cellAnnotCol] = adata.obs[cellAnnotCol].replace({"endothelial": "endothelial cell"})

# Create a list of all unique cell types
goodAnnot = set()
# Create a mapping dictionary using the clustering
category_mapping = {}

# Process each merged category
for merged_category in df.index:
    individual_types = merged_category.split('/')  # Split merged categories
    for cell_type in individual_types:
        cleaned_cell_type = cell_type.strip()  # Remove leading/trailing spaces
        goodAnnot.add(cleaned_cell_type)  # Add to goodAnnot list
        category_mapping[cleaned_cell_type] = merged_category  # Map to merged category

goodAnnot = sorted(goodAnnot)
downsampledCells = pd.DataFrame(index = adata.var_names)

for cell in goodAnnot:
    obsThisCell = adata[adata.obs[cellAnnotCol] == cell]
    numObs = obsThisCell.shape[0]
    maxObs = 25 # get maximum 25 cells per type

    if numObs >= maxObs:
        indexSample = sample(range(0, numObs), maxObs)
    else:
        indexSample = range(0, numObs)

    # Select cells (columns) for all genes (rows)
    data = obsThisCell.X[indexSample, :].T  # Transpose after selecting the cells
    if issparse(data):
        data = data.toarray()

    # Ensure cell labels correspond to the number of cells sampled
    cellLabs = list(obsThisCell.obs.iloc[indexSample][cellAnnotCol])  
    thisCellDF = pd.DataFrame(data=data, index=adata.var_names, columns=cellLabs)

    print(cell, " ", thisCellDF.shape)
    print('all = ', downsampledCells.shape) 
    downsampledCells = downsampledCells.join(thisCellDF)

downsampledCells = downsampledCells.loc[~(downsampledCells == 0).all(axis = 1)]
downsampledCells = downsampledCells.dropna(axis=1, how='all')
downsampledCells = downsampledCells.fillna(0)

# Apply mapping to rename columns
downsampledCells.columns = [category_mapping.get(col, col) for col in downsampledCells.columns]

# Verify the updated column names
downsampledCells.to_csv(fend, index = True, sep='\t', header = True)
