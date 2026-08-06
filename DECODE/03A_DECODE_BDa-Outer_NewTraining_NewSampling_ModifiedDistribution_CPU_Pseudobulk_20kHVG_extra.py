#!/usr/bin/env python3

import os
import pickle
import random
import warnings

import numpy as np
import anndata as ad
from sklearn.model_selection import train_test_split

from data_process_dirichlet import data_process

warnings.filterwarnings("ignore")

# Keep split identical to original
split_seed = 2021

# Change generation seed so new pseudobulks are different
generation_seed = 2022
random.seed(generation_seed)
np.random.seed(generation_seed)

input_h5ad = "/exports/eddie/scratch/s2556897/DECODE/test-data/TSP-BDa-merged-Outer_matched_DECODE_1500each_20kHVG.h5ad"
extra_tissue_name = "TSP-BDa_Outer_s600_a50_ab1_NewTrain_NewSampling_Dirichtler_81celltypes_20kHVG_extra25kpseudo"

label_col = "MergedClusters"

extra_train_sample_num = 31500
sample_size = 600
num_artificial_cells = 50

os.makedirs(f"data/{extra_tissue_name}", exist_ok=True)

adata = ad.read_h5ad(input_h5ad)
adata.obs[label_col] = adata.obs[label_col].astype(str)

type_list = sorted(adata.obs[label_col].dropna().unique().tolist())
adata = adata[adata.obs[label_col].isin(type_list)].copy()
adata.obs.reset_index(drop=True, inplace=True)

cell_counts = adata.obs[label_col].value_counts()
can_stratify = cell_counts.min() >= 2
indices = np.arange(adata.n_obs)

train_idx, test_idx = train_test_split(
    indices,
    test_size=0.25,
    random_state=split_seed,
    shuffle=True,
    stratify=adata.obs[label_col].values if can_stratify else None,
)

train_data = adata[train_idx].copy()
test_data = adata[test_idx].copy()

train_data.obs.reset_index(drop=True, inplace=True)
test_data.obs.reset_index(drop=True, inplace=True)

print(f"Training cell types: {len(type_list)}")
print("Generating extra training pseudobulks only...")

dp_train = data_process(
    type_list=type_list,
    tissue_name=extra_tissue_name,
    sample_size=sample_size,
    train_sample_num=extra_train_sample_num,
    test_sample_num=0,
    num_artificial_cells=num_artificial_cells,
    random_type=label_col,
)

print("Generating artificial cells...")
artificial_cells = dp_train.build_artificial_cell(train_data, num_artificial_cells)

print("Generating extra training pseudobulks...")
extra_train_x_sim, extra_train_y = dp_train.build_pseudo_bulk_no_noise(train_data, "train")

extra_train_with_noise_1 = dp_train.build_train_pseudo_bulk_with_noise(
    extra_train_x_sim,
    noise=artificial_cells,
    noise_limit=0.1,
)

extra_train_with_noise_2 = dp_train.build_train_pseudo_bulk_with_noise(
    extra_train_x_sim,
    noise=artificial_cells,
    noise_limit=0.1,
)

print("Normalizing extra training pseudobulks...")
extra_train_x_sim = dp_train.normalize(extra_train_x_sim)
extra_train_with_noise_1 = dp_train.normalize(extra_train_with_noise_1)
extra_train_with_noise_2 = dp_train.normalize(extra_train_with_noise_2)

extra_pkl_path = f"data/{extra_tissue_name}/{extra_tissue_name}{len(type_list)}cell_extra_train_only.pkl"

with open(extra_pkl_path, "wb") as f:
    pickle.dump(
        [extra_train_x_sim, extra_train_with_noise_1, extra_train_with_noise_2, extra_train_y],
        f,
    )

with open(f"data/{extra_tissue_name}/type_list.pkl", "wb") as f:
    pickle.dump(type_list, f)

train_data.write_h5ad(f"data/{extra_tissue_name}/ref_cell.h5ad")

print(f"Saved extra training pseudobulks to: {extra_pkl_path}")