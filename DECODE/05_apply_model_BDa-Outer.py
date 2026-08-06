#!/usr/bin/env python3

import os
import pickle
import numpy as np
import pandas as pd
import torch
import anndata as ad
from torch.utils.data import DataLoader, TensorDataset

from model.deconv_model_with_stage_2 import MBdeconv

# -------------------------
# Settings
# -------------------------
tissue_name = "TSP-BDa_Outer_s600_a50_ab1_NewTrain_NewSampling_Dirichtler_81celltypes_81.5kpseudo_20kHVG"

external_pseudobulk_txt = "Random_v2C_All-Counts.txt"
output_csv = "TSP-BDa_Outer_Random_v2C_DECODE-PureTrue_predictions_Stage3Val.txt"
#output_csv = "TSP-BDa_Outer_Random_v2C_DECODE-PureTrue_predictions.txt"

batch_size = 64
feat_map_w = 256
feat_map_h = 10
epoches = 800
Alpha = 1
Beta = 1

device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
print(f"Using device: {device}")

training_h5ad = "/exports/eddie/scratch/s2556897/DECODE/test-data/TSP-BDa-merged-Outer_matched_DECODE_1500each_20kHVG.h5ad"

# -------------------------
# Load type list and training gene order
# -------------------------
with open(f"data/{tissue_name}/type_list.pkl", "rb") as f:
    type_list = pickle.load(f)

with open(f"data/{tissue_name}/{tissue_name}{len(type_list)}cell.pkl", "rb") as f:
    train = pickle.load(f)
    test = pickle.load(f)
    _ = pickle.load(f)

train_x_sim, _, _, _ = train

# The pkl stores numeric indices, so get the real gene names from the h5ad
adata_ref = ad.read_h5ad(training_h5ad)
train_genes = adata_ref.var_names.astype(str).tolist()

if len(train_genes) != len(train_x_sim[0]):
    raise ValueError(
        f"Gene number mismatch: h5ad has {len(train_genes)} genes, "
        f"but trained pseudobulk has {len(train_x_sim[0])} features."
    )

num_feat = len(train_genes)
num_cell_type = len(type_list)

print(f"Number of training genes: {num_feat}")
print(f"Number of cell types: {num_cell_type}")

# -------------------------
# Load external pseudobulks
# -------------------------
# Input format: genes x pseudobulks
pb = pd.read_csv(external_pseudobulk_txt, sep="\t", index_col=0)

# Convert to pseudobulks x genes
pb = pb.T

print(f"External pseudobulks loaded: {pb.shape[0]}")
print(f"External genes loaded: {pb.shape[1]}")

# Align genes to training order
missing_genes = [g for g in train_genes if g not in pb.columns]
extra_genes = [g for g in pb.columns if g not in train_genes]

print(f"Missing genes filled with zero: {len(missing_genes)}")
print(f"Extra genes ignored: {len(extra_genes)}")

print("\nTraining gene examples:")
print(train_genes[:20])

print("\nExternal gene examples:")
print(pb.columns[:20].tolist())

overlap = len(set(train_genes) & set(pb.columns))
print(f"\nGene overlap: {overlap} / {len(train_genes)}")

if overlap == 0:
    raise ValueError(
        "No gene overlap between training genes and external pseudobulk genes. "
        "Check whether one uses gene symbols and the other uses Ensembl IDs, "
        "or whether training genes were loaded as numeric indices."
    )

pb = pb.reindex(columns=train_genes, fill_value=0)

# -------------------------
# Apply DECODE normalization
# -------------------------
# Same logic as data_process.normalize(): each pseudobulk / its max value
pb = pb.fillna(0)
pb[pb < 0] = 0

max_vals = pb.max(axis=1)
max_vals[max_vals == 0] = 1

pb_norm = pb.div(max_vals, axis=0)

# -------------------------
# Create dataloader
# -------------------------
x_tensor = torch.FloatTensor(pb_norm.values)
dataset = TensorDataset(x_tensor)

loader = DataLoader(
    dataset,
    batch_size=batch_size,
    shuffle=False,
)

# -------------------------
# Load trained DECODE model
# -------------------------
model = MBdeconv(
    num_MB=num_feat,
    feat_map_w=feat_map_w,
    feat_map_h=feat_map_h,
    num_cell_type=num_cell_type,
    epoches=epoches,
    Alpha=Alpha,
    Beta=Beta,
    train_data=None,
    test_data=None,
)

#model_path = f"save_models/{num_feat}/{tissue_name}_train52500_DANNpatience20.pt"
model_path = f"save_models/{num_feat}/{tissue_name}_train73500_DANNpatience25_Stage3Val.pt"

print(f"Loading model: {model_path}")

model.load_state_dict(torch.load(model_path, map_location=device))
model = model.to(device)
model.eval()

# -------------------------
# Predict using pure_forward
# -------------------------
preds = []

with torch.no_grad():
    for (x,) in loader:
        x = x.to(device)

        # DECODE evaluation uses pure_forward when if_pure=True
        _, pred_rate = model.pure_forward(x)

        preds.append(pred_rate.detach().cpu().numpy())

preds = np.vstack(preds)

pred_df = pd.DataFrame(
    preds,
    index=pb_norm.index,
    columns=type_list,
)

print(f"\nPrediction matrix shape: {pred_df.shape}")
print(f"Number of pseudobulks (rows): {pred_df.shape[0]}")
print(f"Number of predicted cell types (columns): {pred_df.shape[1]}")

# Optional sanity check: each row should sum to ~1
pred_df["sum_check"] = pred_df.sum(axis=1)
print(pred_df["sum_check"].describe())
pred_df = pred_df.drop(columns=["sum_check"])

pred_df.to_csv(output_csv, sep="\t", index=True)

print(f"Saved DECODE predictions to: {output_csv}")