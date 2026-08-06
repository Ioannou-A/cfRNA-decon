#!/usr/bin/env python3

import os
import re
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
tissue_name = "GTEx_s250_a21_ab1_NewTrain_NewSampling_Dirichtler_Abundant_40k"

external_pseudobulk_txt = "GSE255555_pedInflam_filtered_counts_CPM_GeneNames.txt"
output_csv = "GTEx_TOO_Loy_DECODEPureFalse_Renamed_Stage3Val.txt"
#output_csv = "GTEx_TOO_Loy_DECODEPureFalse_Renamed.txt"
gene_name_lookup_tsv = "GTEx_v8_all_tissues_all_samples_TrainingGeneNames.tsv"
gtf_path = "/exports/eddie/scratch/s2556897/gencode.v46.annotation.gtf"

batch_size = 64
feat_map_w = 256
feat_map_h = 10
epoches = 200
Alpha = 1
Beta = 1

device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
print(f"Using device: {device}")

training_h5ad = "/exports/eddie/scratch/s2556897/DECODE/test-data-TOO/GTEx_v8_rawCounts_GeneSymbol.h5ad"

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
num_tissue = len(type_list)

print(f"Number of training genes: {num_feat}")
print(f"Number of tissues: {num_tissue}")

# -------------------------
# Load external tissue mixtures
# -------------------------
# Input format: genes x tissue mixtures
pb = pd.read_csv(external_pseudobulk_txt, sep="\t", index_col=0)

# Convert to tissue mixtures x genes
pb = pb.T

print(f"External tissue mixtures loaded: {pb.shape[0]}")
print(f"External genes loaded: {pb.shape[1]}")

# -------------------------
# Rename external genes to training gene names
# -------------------------
gene_lookup = pd.read_csv(gene_name_lookup_tsv, sep="\t", dtype=str)

gene_lookup["EnsemblID"] = gene_lookup["EnsemblID"].astype(str).str.strip()
gene_lookup["GeneSymbol"] = gene_lookup["GeneSymbol"].astype(str).str.strip()
gene_lookup["TrainingGeneName"] = gene_lookup["TrainingGeneName"].astype(str).str.strip()

gene_lookup["EnsemblID_clean"] = (
    gene_lookup["EnsemblID"]
    .str.replace(r"\..*$", "", regex=True)
)

# Direct maps from DECODE/GTEx lookup
symbol_to_training = dict(
    zip(gene_lookup["GeneSymbol"], gene_lookup["TrainingGeneName"])
)

ens_to_training = dict(
    zip(gene_lookup["EnsemblID_clean"], gene_lookup["TrainingGeneName"])
)

# -------------------------
# Add GTF bridge:
# current GTF gene name -> Ensembl ID -> DECODE training gene name
# -------------------------
def extract_gtf_info(attr, key):
    match = re.search(f'{key} "([^"]+)"', str(attr))
    return match.group(1) if match else None

gtf = pd.read_csv(
    gtf_path,
    sep="\t",
    comment="#",
    header=None,
    dtype=str,
    low_memory=False
)

gtf.columns = [
    "seqname", "source", "feature", "start", "end",
    "score", "strand", "frame", "attribute"
]

genes_gtf = gtf[gtf["feature"] == "gene"].copy()

genes_gtf["GeneID"] = genes_gtf["attribute"].apply(
    lambda x: extract_gtf_info(x, "gene_id")
)

genes_gtf["GeneName"] = genes_gtf["attribute"].apply(
    lambda x: extract_gtf_info(x, "gene_name")
)

genes_gtf["EnsemblID_clean"] = (
    genes_gtf["GeneID"]
    .astype(str)
    .str.replace(r"\..*$", "", regex=True)
)

gtf_symbol_to_ens = dict(
    zip(genes_gtf["GeneName"], genes_gtf["EnsemblID_clean"])
)

gtf_symbol_to_training = {
    symbol: ens_to_training[ens]
    for symbol, ens in gtf_symbol_to_ens.items()
    if ens in ens_to_training
}

def rename_gene(g):
    g = str(g).strip()
    g_no_quotes = g.replace('"', '').replace("'", "")
    g_clean = g_no_quotes.split(".")[0]

    # 1. Already an original GTEx/DECODE symbol
    if g in symbol_to_training:
        return symbol_to_training[g]

    # 2. Ensembl ID
    if g_clean in ens_to_training:
        return ens_to_training[g_clean]

    # 3. Current GTF gene symbol
    if g in gtf_symbol_to_training:
        return gtf_symbol_to_training[g]

    return g

old_cols = pb.columns.astype(str).tolist()
new_cols = [rename_gene(g) for g in old_cols]

n_changed = sum(o != n for o, n in zip(old_cols, new_cols))
print(f"External genes renamed: {n_changed}")

# Debug examples
for test_gene in ["ENSG00000238009", "ENSG00000239945", "ENSG00000290826"]:
    print(
        test_gene,
        "->",
        ens_to_training.get(test_gene, "NOT_FOUND_IN_LOOKUP")
    )

pb.columns = new_cols

print(f"External genes after renaming: {pb.shape[1]}")

# If two old gene symbols now map to the same training gene name,
# collapse them by summing counts. Sample/mixture row order is preserved.
if pb.columns.duplicated().any():
    n_dup_cols = pb.columns.duplicated().sum()
    print(f"Duplicate gene columns after renaming: {n_dup_cols}")
    print("Collapsing duplicate genes by summing counts...")

    pb = pb.T.groupby(level=0, sort=False).sum().T

# -------------------------
# Align genes to exact model training order
# -------------------------
missing_genes = [g for g in train_genes if g not in pb.columns]
extra_genes = [g for g in pb.columns if g not in train_genes]

print(f"Missing genes filled with zero: {len(missing_genes)}")
print(f"Extra genes ignored: {len(extra_genes)}")

print("\nTraining gene examples:")
print(train_genes[:20])

print("\nExternal gene examples after renaming:")
print(pb.columns[:20].tolist())

overlap = len(set(train_genes) & set(pb.columns))
print(f"\nGene overlap after renaming: {overlap} / {len(train_genes)}")

if overlap == 0:
    raise ValueError(
        "No gene overlap after renaming. Check GeneSymbol / TrainingGeneName mapping."
    )

# Critical: force columns into exact training order expected by the model
pb = pb.reindex(columns=train_genes, fill_value=0)

if pb.columns.tolist() != train_genes:
    raise ValueError("Gene order mismatch after reindexing.")

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
    num_cell_type=num_tissue,
    epoches=epoches,
    Alpha=Alpha,
    Beta=Beta,
    train_data=None,
    test_data=None,
)

#model_path = f"save_models/{num_feat}/{tissue_name}_train30000_DANNpatience10.pt"
model_path = f"save_models/{num_feat}/{tissue_name}_DANNpatience10_Stage3Val.pt"
print(f"Loading model: {model_path}")

model.load_state_dict(torch.load(model_path, map_location=device))
model = model.to(device)
model.eval()

# -------------------------
# Predict using full forward / if_pure=False
# -------------------------

preds = []

with torch.no_grad():
    for (x,) in loader:
        x = x.to(device)

        extract_cell, noise, pred_rate = model.forward(x)

        preds.append(pred_rate.detach().cpu().numpy())

preds = np.vstack(preds)

pred_df = pd.DataFrame(
    preds,
    index=pb_norm.index,
    columns=type_list,
)

print(f"\nPrediction matrix shape: {pred_df.shape}")
print(f"Number of tissue mixtures (rows): {pred_df.shape[0]}")
print(f"Number of predicted tissues (columns): {pred_df.shape[1]}")

# Optional sanity check: each row should sum to ~1
pred_df["sum_check"] = pred_df.sum(axis=1)
print(pred_df["sum_check"].describe())
pred_df = pred_df.drop(columns=["sum_check"])

pred_df.to_csv(output_csv, sep="\t", index=True)

print(f"Saved DECODE predictions to: {output_csv}")