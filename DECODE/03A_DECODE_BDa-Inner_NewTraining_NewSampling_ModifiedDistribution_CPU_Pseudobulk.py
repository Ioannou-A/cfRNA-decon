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

seed = 2021
random.seed(seed)
np.random.seed(seed)

input_h5ad = "/exports/eddie/scratch/s2556897/DECODE/test-data/TSP-BDa-merged-Inner_matched_DECODE_1500each.h5ad"
tissue_name = "TSP-BDa_Inner_s600_a50_ab1_NewTrain_NewSampling_Dirichtler_81celltypes_50kpseudo"
label_col = "MergedClusters"

train_sample_num = 50000
sample_size = 600
num_artificial_cells = 50
test_sample_num = 8000

os.makedirs(f"data/{tissue_name}", exist_ok=True)

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
    random_state=seed,
    shuffle=True,
    stratify=adata.obs[label_col].values if can_stratify else None,
)

train_data = adata[train_idx].copy()
test_data = adata[test_idx].copy()

train_data.obs.reset_index(drop=True, inplace=True)
test_data.obs.reset_index(drop=True, inplace=True)

test_type_list = type_list

print(f"Training cell types: {len(type_list)}")
print(f"Testing cell types: {len(test_type_list)}")

dp_train = data_process(
    type_list=type_list,
    tissue_name=tissue_name,
    sample_size=sample_size,
    train_sample_num=train_sample_num,
    test_sample_num=0,
    num_artificial_cells=num_artificial_cells,
    random_type=label_col,
)

print("Generating artificial cells...")
artificial_cells = dp_train.build_artificial_cell(train_data, num_artificial_cells)

print("Generating training pseudobulks...")
train_x_sim, train_y = dp_train.build_pseudo_bulk_no_noise(train_data, "train")

train_with_noise_1 = dp_train.build_train_pseudo_bulk_with_noise(
    train_x_sim,
    noise=artificial_cells,
    noise_limit=0.1,
)

train_with_noise_2 = dp_train.build_train_pseudo_bulk_with_noise(
    train_x_sim,
    noise=artificial_cells,
    noise_limit=0.1,
)

dp_test = data_process(
    type_list=test_type_list,
    tissue_name=tissue_name,
    sample_size=sample_size,
    train_sample_num=0,
    test_sample_num=test_sample_num,
    num_artificial_cells=num_artificial_cells,
    random_type=label_col,
)

print("Generating test pseudobulks...")
test_x_sim, test_y_small = dp_test.build_pseudo_bulk_no_noise(test_data, "test")

test_y = []

for y_small in test_y_small:
    full_y = [0.0] * len(type_list)

    for ct, frac in zip(test_type_list, y_small):
        full_idx = type_list.index(ct)
        full_y[full_idx] = frac

    test_y.append(full_y)

print("Normalizing...")
train_x_sim = dp_train.normalize(train_x_sim)
train_with_noise_1 = dp_train.normalize(train_with_noise_1)
train_with_noise_2 = dp_train.normalize(train_with_noise_2)
test_x_sim = dp_train.normalize(test_x_sim)

pkl_path = f"data/{tissue_name}/{tissue_name}{len(type_list)}cell.pkl"

with open(pkl_path, "wb") as f:
    pickle.dump([train_x_sim, train_with_noise_1, train_with_noise_2, train_y], f)
    pickle.dump([test_x_sim, test_y], f)
    pickle.dump([], f)

train_data.write_h5ad(f"data/{tissue_name}/ref_cell.h5ad")

with open(f"data/{tissue_name}/type_list.pkl", "wb") as f:
    pickle.dump(type_list, f)

with open(f"data/{tissue_name}/test_type_list.pkl", "wb") as f:
    pickle.dump(test_type_list, f)

print(f"Saved pseudobulks to: {pkl_path}")