#!/usr/bin/env python3

import os
import copy
import pickle
import random
import warnings

import numpy as np
import torch
from torch.utils.data import DataLoader

from model.deconv_model_with_stage_2 import MBdeconv
from model.utils import *
from model.stage2 import *

warnings.filterwarnings("ignore")

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
    raise RuntimeError("CUDA GPU was not detected.")

tissue_name = "TSP-HBA_Inner_s600_a50_ab1_NewTrain_NewSampling_Dirichtler_81celltypes_81.5kpseudo_20kHVG"

# Number of pseudo bulks used for model training after reserving
# 8,000 of the 81,500-pseudo-bulk pool for validation.
# Values evaluated in the training-size analysis:
# 10,500, 21,000, 31,500, 42,000, 52,500, 63,000 and 73,500.
subset_size = 73500

# DANN early-stopping patience.
# Values evaluated for COO:
# 5, 10, 15, 20, 25 and 30.
dann_patience = 25

model_save_name = tissue_name + f"_train{subset_size}_DANNpatience{dann_patience}" + "_Stage3Val"
batch_size = 64
valid_size = 8000

feat_map_w = 256
feat_map_h = 10

patience = 10
epoches = 800
Alpha = 1
Beta = 1
learning_rate = 0.0001

pkl_path = f"data/{tissue_name}/{tissue_name}69cell.pkl"

with open(f"data/{tissue_name}/type_list.pkl", "rb") as f:
    type_list = pickle.load(f)

with open(pkl_path, "rb") as f:
    train = pickle.load(f)
    test = pickle.load(f)
    test_with_noise = pickle.load(f)

train_x_sim, train_with_noise_1, train_with_noise_2, train_y = train
test_x_sim, test_y = test

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

# -------------------------
# Training saturation subset
# -------------------------
train_x_sim_all = train_x_sim
train_with_noise_1_all = train_with_noise_1
train_with_noise_2_all = train_with_noise_2
train_y_all = train_y

if subset_size > len(train_x_sim_all):
    raise ValueError(
        f"subset_size={subset_size} is larger than available training pseudobulks "
        f"after validation split: {len(train_x_sim_all)}"
    )

train_x_sim = train_x_sim_all[:subset_size]
train_with_noise_1 = train_with_noise_1_all[:subset_size]
train_with_noise_2 = train_with_noise_2_all[:subset_size]
train_y = train_y_all[:subset_size]

print(f"Using {len(train_x_sim)} training pseudobulks")
print(f"Using {len(valid_x_sim)} validation pseudobulks")
print(f"Using {len(test_x_sim)} test pseudobulks")

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

num_feat = len(train_x_sim[0])
num_cell_type = len(type_list)

print(f"Number of features: {num_feat}")
print(f"Number of cell types: {num_cell_type}")

model_da = DANN(
    num_epochs=epoches,
    batch_size=50,
    learning_rate=learning_rate,
)

pred_loss, disc_loss, disc_loss_DA, best_model_weights = model_da.train(
    source_data,
    target_data,
    valid_data,
    patience=dann_patience
)

model = MBdeconv(
    num_MB=num_feat,
    feat_map_w=feat_map_w,
    feat_map_h=feat_map_h,
    num_cell_type=num_cell_type,
    epoches=epoches,
    Alpha=Alpha,
    Beta=Beta,
    train_data=train_dataloader,
    test_data=valid_dataloader,
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

pred.to_csv(f"data/{tissue_name}/predictions_train{subset_size}_DANNpatience{dann_patience}_Stage3Val.csv", index=False)
gt.to_csv(f"data/{tissue_name}/ground_truth_train{subset_size}_DANNpatience{dann_patience}_Stage3Val.csv", index=False)

print(f"Saved predictions to data/{tissue_name}/predictions_train{subset_size}_DANNpatience{dann_patience}_Stage3Val.csv")
print(f"Saved ground truth to data/{tissue_name}/ground_truth_train{subset_size}_DANNpatience{dann_patience}_Stage3Val.csv")
print(f"Saved model to {model_path}")