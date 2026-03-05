import os
import numpy as np
import pandas as pd
from sklearn import preprocessing

def scale_only(data_path, basis_path, output_dir=None):
    print(f"Processing basis: {basis_path}")
    
    if output_dir is None:
        output_dir = os.path.dirname(os.path.abspath(basis_path))
    os.makedirs(output_dir, exist_ok=True)

    print("Loading data...")
    data = pd.read_csv(data_path, delimiter="\t", low_memory=False, comment='#')
    data.set_index(data.columns[0], inplace=True)
    basis = pd.read_csv(basis_path, delimiter="\t", low_memory=False, index_col=0)

    print("Aligning indices...")
    common_indexes = data.index.intersection(basis.index)

    print("Scaling basis matrix...")
    scaled_basis = preprocessing.scale(basis.loc[common_indexes].values)

    print("Scaling mixture matrix...")
    scaled_data = preprocessing.scale(data.loc[common_indexes].values)

    # Extract identifiers
    basis_id = os.path.basename(os.path.dirname(basis_path))  # e.g., CIBERSORTx-Matrix_...
    data_id = os.path.splitext(os.path.basename(data_path))[0]  # e.g., Random_v1_All-Counts

    # Save scaled basis matrix
    basis_scaled_path = os.path.join(output_dir, f"{data_id}_{basis_id}_scaled_basis.txt")
    scaled_basis_df = pd.DataFrame(scaled_basis, index=common_indexes, columns=basis.columns)
    scaled_basis_df.to_csv(basis_scaled_path, sep="\t")
    print(f"Saved scaled basis to {basis_scaled_path}")

    # Save entire scaled mixture (no splitting)
    mixture_scaled_path = os.path.join(output_dir, f"{data_id}_{basis_id}_scaled_mixture.txt")
    scaled_data_df = pd.DataFrame(scaled_data, index=common_indexes, columns=data.columns)
    scaled_data_df.to_csv(mixture_scaled_path, sep="\t")
    print(f"Saved scaled mixture to {mixture_scaled_path}")

# Main run
data_path = "COO-Decon-Pseudobulks/Random_v2C_All-Counts.txt"

basis_paths = [
    "COO-Decon-Pseudobulks/CIBERSORTx-Matrix_TSP-BDa_Inner_1000_3000_10/CIBERSORTx_TSP-BDa_Inner_25each_inferred_phenoclasses.CIBERSORTx_TSP-BDa_Inner_25each_inferred_refsample.bm.K999.txt",
    "COO-Decon-Pseudobulks/CIBERSORTx-Matrix_TSP-BDa_Inner_3000_5000_10/CIBERSORTx_TSP-BDa_Inner_25each_inferred_phenoclasses.CIBERSORTx_TSP-BDa_Inner_25each_inferred_refsample.bm.K999.txt",
    "COO-Decon-Pseudobulks/CIBERSORTx-Matrix_TSP-BDa_Inner_300_1500_10/CIBERSORTx_TSP-BDa_Inner_25each_inferred_phenoclasses.CIBERSORTx_TSP-BDa_Inner_25each_inferred_refsample.bm.K999.txt",
    "COO-Decon-Pseudobulks/CIBERSORTx-Matrix_TSP-BDa_Outer_1000_3000_10/CIBERSORTx_TSP-BDa_Outer_25each_inferred_phenoclasses.CIBERSORTx_TSP-BDa_Outer_25each_inferred_refsample.bm.K999.txt",
    "COO-Decon-Pseudobulks/CIBERSORTx-Matrix_TSP-BDa_Outer_3000_5000_10/CIBERSORTx_TSP-BDa_Outer_25each_inferred_phenoclasses.CIBERSORTx_TSP-BDa_Outer_25each_inferred_refsample.bm.K999.txt",
    "COO-Decon-Pseudobulks/CIBERSORTx-Matrix_TSP-BDa_Outer_300_1500_10/CIBERSORTx_TSP-BDa_Outer_25each_inferred_phenoclasses.CIBERSORTx_TSP-BDa_Outer_25each_inferred_refsample.bm.K999.txt",
    "COO-Decon-Pseudobulks/CIBERSORTx-Matrix_TSP-HBA_Inner_1000_3000_10/CIBERSORTx_TSP-HBA_Inner_25each_inferred_phenoclasses.CIBERSORTx_TSP-HBA_Inner_25each_inferred_refsample.bm.K999.txt",
    "COO-Decon-Pseudobulks/CIBERSORTx-Matrix_TSP-HBA_Inner_3000_5000_10/CIBERSORTx_TSP-HBA_Inner_25each_inferred_phenoclasses.CIBERSORTx_TSP-HBA_Inner_25each_inferred_refsample.bm.K999.txt",
    "COO-Decon-Pseudobulks/CIBERSORTx-Matrix_TSP-HBA_Inner_300_1500_10/CIBERSORTx_TSP-HBA_Inner_25each_inferred_phenoclasses.CIBERSORTx_TSP-HBA_Inner_25each_inferred_refsample.bm.K999.txt",
]

# Iterate over each basis_path and run the function for the Random Counts
for basis_path in basis_paths:
    full_basis_path = os.path.abspath(basis_path)
    scale_only(data_path, full_basis_path)
