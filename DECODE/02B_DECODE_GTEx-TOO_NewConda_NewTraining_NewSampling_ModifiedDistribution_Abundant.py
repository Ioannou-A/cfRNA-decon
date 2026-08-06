#!/usr/bin/env python3

import os
import copy
import pickle
import random
import warnings

import numpy as np
import torch
import anndata as ad
from sklearn.model_selection import train_test_split
from torch.utils.data import DataLoader

from data_process_dirichlet import data_process
from model.deconv_model_with_stage_2 import MBdeconv
from model.utils import *
from model.stage2 import *

warnings.filterwarnings("ignore")

# This script uses a modified sampling approach for the distribution to see if the issue for the low STD variance is based on the distribution

# -------------------------
# Reproducibility + GPU
# -------------------------
seed = 2021
random.seed(seed)
np.random.seed(seed)
torch.manual_seed(seed)
torch.cuda.manual_seed_all(seed)

torch.backends.cudnn.deterministic = True
torch.backends.cudnn.benchmark = False

device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
print(f"Using device: {device}")

if not torch.cuda.is_available():
    raise RuntimeError(
        "CUDA GPU was not detected. This training script uses GPU-dependent "
        "model code from the original notebook."
    )

# -------------------------
# Input / output settings
# -------------------------
input_h5ad = "/exports/eddie/scratch/s2556897/DECODE/test-data-TOO/GTEx_v8_rawCounts_GeneSymbol.h5ad"
tissue_name = "GTEx_s250_a21_ab1_NewTrain_NewSampling_Dirichtler_Abundant_40k"
label_col = "MergedClusters"

os.makedirs(f"data/{tissue_name}", exist_ok=True)
os.makedirs("save_models", exist_ok=True)

# -------------------------
# Pseudobulk generation parameters
# -------------------------
train_sample_num = 35000
sample_size = 250
num_artificial_cells = 20
test_sample_num = 5000

# -------------------------
# Model / training parameters
# -------------------------
batch_size = 64
valid_size = 5000

feat_map_w = 256
feat_map_h = 10

patience = 10
epoches = 200
Alpha = 1
Beta = 1
learning_rate = 0.0001

model_save_name = tissue_name

# -------------------------
# Load data
# -------------------------
adata = ad.read_h5ad(input_h5ad)

if label_col not in adata.obs.columns:
    raise KeyError(f"Could not find adata.obs['{label_col}'].")

adata.obs[label_col] = adata.obs[label_col].astype(str)

type_list = sorted(adata.obs[label_col].dropna().unique().tolist())

print(f"Found {len(type_list)} cell types from adata.obs['{label_col}']:")
for ct in type_list:
    print(f"  - {ct}")

# Keep only valid labelled cells
adata = adata[adata.obs[label_col].isin(type_list)].copy()
adata.obs.reset_index(drop=True, inplace=True)

# -------------------------
# Train/test split from the single input h5ad
# -------------------------
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

print("Train data:", train_data)
print("Test data:", test_data)

print("\nTrain cell counts:")
print(train_data.obs[label_col].value_counts())

print("\nTest cell counts:")
print(test_data.obs[label_col].value_counts())

# -------------------------
# Generate pseudobulk data
# -------------------------

min_test_cells = 2

test_counts = test_data.obs[label_col].value_counts()
test_type_list = sorted(test_counts[test_counts >= min_test_cells].index.tolist())

print(f"\nTraining uses all cell types: {len(type_list)}")
print(f"Testing uses cell types with >= {min_test_cells} cells: {len(test_type_list)}")

# ---- TRAIN: all cell types ----
dp_train = data_process(
    type_list=type_list,
    tissue_name=tissue_name,
    sample_size=sample_size,
    train_sample_num=train_sample_num,
    test_sample_num=0,
    num_artificial_cells=num_artificial_cells,
    random_type=label_col,
)

print("\nGenerating training pseudobulks...")
artificial_cells = dp_train.build_artificial_cell(train_data, num_artificial_cells)

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

# ---- TEST: only abundant test cell types ----
dp_test = data_process(
    type_list=test_type_list,
    tissue_name=tissue_name,
    sample_size=sample_size,
    train_sample_num=0,
    test_sample_num=test_sample_num,
    num_artificial_cells=num_artificial_cells,
    random_type=label_col,
)

print("\nGenerating test pseudobulks from abundant test cell types only...")
test_x_sim, test_y_small = dp_test.build_pseudo_bulk_no_noise(test_data, "test")

# Pad test labels back to full type_list length
test_y = []

for y_small in test_y_small:
    full_y = [0.0] * len(type_list)

    for ct, frac in zip(test_type_list, y_small):
        full_idx = type_list.index(ct)
        full_y[full_idx] = frac

    test_y.append(full_y)

# Normalize using DECODE's normalization
train_x_sim = dp_train.normalize(train_x_sim)
train_with_noise_1 = dp_train.normalize(train_with_noise_1)
train_with_noise_2 = dp_train.normalize(train_with_noise_2)
test_x_sim = dp_train.normalize(test_x_sim)

# Save outputs
with open(f"data/{tissue_name}/{tissue_name}{len(type_list)}cell.pkl", "wb") as f:
    pickle.dump([train_x_sim, train_with_noise_1, train_with_noise_2, train_y], f)
    pickle.dump([test_x_sim, test_y], f)
    pickle.dump([], f)

train_data.write_h5ad(f"data/{tissue_name}/ref_cell.h5ad")

with open(f"data/{tissue_name}/type_list.pkl", "wb") as f:
    pickle.dump(type_list, f)

with open(f"data/{tissue_name}/test_type_list.pkl", "wb") as f:
    pickle.dump(test_type_list, f)

print("Pseudobulk generation complete.")

# -------------------------
# Validation split
# -------------------------
if valid_size >= len(train_x_sim):
    valid_size = max(1, int(0.1 * len(train_x_sim)))

valid_x_sim = train_x_sim[:valid_size]
valid_with_noise_1 = train_with_noise_1[:valid_size]
valid_with_noise_2 = train_with_noise_2[:valid_size]
valid_y = train_y[:valid_size]

train_x_sim = train_x_sim[valid_size:]
train_with_noise_1 = train_with_noise_1[valid_size:]
train_with_noise_2 = train_with_noise_2[valid_size:]
train_y = train_y[valid_size:]

train_dataset = TrainCustomDataset(
    train_x_sim,
    train_with_noise_1,
    train_with_noise_2,
    train_y,
)

test_dataset = TestCustomDataset(test_x_sim, test_y)
valid_dataset = TestCustomDataset(valid_x_sim, valid_y)

train_dataloader = DataLoader(
    train_dataset,
    batch_size=batch_size,
    shuffle=True,
    drop_last=True,
)

test_dataloader = DataLoader(
    test_dataset,
    batch_size=batch_size,
    shuffle=False,
)

valid_dataloader = DataLoader(
    valid_dataset,
    batch_size=batch_size,
    shuffle=False,
)

source_data = data2h5ad(train_x_sim, train_y, type_list)
target_data = data2h5ad(test_x_sim, test_y, type_list)
valid_data = data2h5ad(valid_x_sim, valid_y, type_list)

# -------------------------
# Model setup
# -------------------------
num_feat = len(train_x_sim[0])
num_cell_type = len(type_list)

print(f"Number of features: {num_feat}")
print(f"Number of cell types: {num_cell_type}")

# -------------------------
# Stage 2: DANN training
# -------------------------
model_da = DANN(
    num_epochs=epoches,
    batch_size=50,
    learning_rate=learning_rate,
)

pred_loss, disc_loss, disc_loss_DA, best_model_weights = model_da.train(
    source_data,
    target_data,
    valid_data,
    patience=3,
)

# -------------------------
# Stage 3: MBdeconv training
# -------------------------
model = MBdeconv(
    num_MB=num_feat,
    feat_map_w=feat_map_w,
    feat_map_h=feat_map_h,
    num_cell_type=num_cell_type,
    epoches=epoches,
    Alpha=Alpha,
    Beta=Beta,
    train_data=train_dataloader,
    test_data=test_dataloader,
)

model = model.to(device)

model_da.encoder_da.load_state_dict(best_model_weights["encoder"])
encoder_params = copy.deepcopy(model_da.encoder_da.state_dict())
model.encoder.load_state_dict(encoder_params)

loss1_list, loss2_list, nce_loss_list = model.train_model(
    model_save_name=model_save_name,
    if_pure=True,
    patience=patience,
)

# -------------------------
# Stage 4: Evaluation
# -------------------------
model_test = MBdeconv(
    num_MB=num_feat,
    feat_map_w=feat_map_w,
    feat_map_h=feat_map_h,
    num_cell_type=num_cell_type,
    epoches=epoches,
    Alpha=Alpha,
    Beta=Beta,
    train_data=train_dataloader,
    test_data=test_dataloader,
)

model_path = f"save_models/{num_feat}/{model_save_name}.pt"
model_test.load_state_dict(torch.load(model_path, map_location=device))
model_test = model_test.to(device)
model_test.eval()

CCC, RMSE, Corr, pred, gt = predict(
    test_dataloader,
    type_list,
    model_test,
    if_pure=True,
)

print("\nFinal metrics")
print(f"CCC:  {CCC}")
print(f"RMSE: {RMSE}")
print(f"Corr: {Corr}")

pred.to_csv(f"data/{tissue_name}/predictions.csv", index=False)
gt.to_csv(f"data/{tissue_name}/ground_truth.csv", index=False)

print(f"\nSaved predictions to data/{tissue_name}/predictions.csv")
print(f"Saved ground truth to data/{tissue_name}/ground_truth.csv")
print(f"Saved model to {model_path}")