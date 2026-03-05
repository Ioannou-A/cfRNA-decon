# This is crucial to work as it was wrong and had to change it over christmas
# 

import pandas as pd
import numpy as np

proportions_file = "Random_v2C_New_All-Proportions.txt"

def reformat_proportions(
    counts_file: str,
    output_file: str,
    proportions_file: str = proportions_file,
    print_mapping: bool = True,          # Option 1
    check_merges: bool = True,           # Option 2
    n_rows_check: int = 5,               # how many rows to check
    random_rows: bool = False,           # set True to sample rows instead of first N
    seed: int = 0
):
    # Load headers
    with open(counts_file) as f:
        counts_header = f.readline().strip().split('\t')

    with open(proportions_file) as f:
        prop_header = f.readline().strip().split('\t')

    # Load proportions data
    prop_df = pd.read_csv(proportions_file, sep='\t', header=0)

    # First two columns are 'Filename' and 'TotalCells'
    fixed_cols = prop_header[:2]
    prop_celltypes = prop_header[2:]

    # --- Build mapping: exact first, fallback to substring only if no exact matches exist
    mapping = {}
    for ct in counts_header:
        parts = [p.strip() for p in ct.split('/')]

        # exact matches (preferred)
        exact = [p for p in prop_celltypes if p in parts]

        if exact:
            matched = exact
        else:
            matched = [p for p in prop_celltypes if any(part in p for part in parts)]

        mapping[ct] = matched

        # Diagnostics
        if len(matched) == 0:
            print(f"[NO MATCH] {ct}")
        elif len(matched) > len(parts):
            print(f"[WIDE MATCH] {ct} -> {matched}")

    # --- Option 1: Focused mapping print (merged only)
    if print_mapping:
        print("\n=== MAPPING (merged counts headers only) ===")
        for ct, cols in mapping.items():
            if "/" in ct and cols:
                print(f"{ct}  <--  {cols}")
        print("=== END MAPPING ===\n")

    # --- Build transformed dataframe
    transformed = prop_df[fixed_cols].copy()

    for ct in counts_header:
        matched_cols = mapping[ct]
        if matched_cols:
            transformed[ct] = prop_df[matched_cols].sum(axis=1)
        else:
            transformed[ct] = 0

    # --- Option 2: Arithmetic check (prove sum is correct)
    if check_merges:
        # choose rows to check
        if random_rows:
            rng = np.random.default_rng(seed)
            rows_to_check = rng.choice(transformed.index, size=min(n_rows_check, len(transformed)), replace=False)
        else:
            rows_to_check = transformed.index[:min(n_rows_check, len(transformed))]

        print("\n=== MERGE ARITHMETIC CHECK ===")

        # check only merged headers that actually matched something
        for ct, matched_cols in mapping.items():
            if "/" not in ct or not matched_cols:
                continue

            summed = prop_df.loc[rows_to_check, matched_cols].sum(axis=1)
            outcol = transformed.loc[rows_to_check, ct]
            diff = (outcol - summed)

            max_abs_diff = diff.abs().max()
            if max_abs_diff > 1e-10:
                print(f"[FAIL] {ct}: max |diff| = {max_abs_diff}")
            else:
                print(f"[OK]   {ct}: max |diff| = {max_abs_diff}")

        print("=== END MERGE CHECK ===\n")

    # Save to file
    transformed.to_csv(output_file, sep='\t', index=False)


# --- Run for the three references ---
reformat_proportions(
    counts_file="TSP-BDa_Inner_300_1500_10-Random_v2/QP_Random_v2C_All-Counts_modified.txt",
    output_file="TSP-BDa_Inner_Random_v2C_New_All-Proportions.txt",
    print_mapping=True,
    check_merges=True,
    n_rows_check=5,
    random_rows=False
)

reformat_proportions(
    counts_file="TSP-BDa_Outer_300_1500_10-Random_v2/QP_Random_v2C_All-Counts_modified.txt",
    output_file="TSP-BDa_Outer_Random_v2C_New_All-Proportions.txt",
    print_mapping=True,
    check_merges=True,
    n_rows_check=5,
    random_rows=False
)

reformat_proportions(
    counts_file="TSP-HBA_Inner_300_1500_10-Random_v2/QP_Random_v2C_All-Counts_modified.txt",
    output_file="TSP-HBA_Inner_Random_v2C_New_All-Proportions.txt",
    print_mapping=True,
    check_merges=True,
    n_rows_check=5,
    random_rows=False
)

