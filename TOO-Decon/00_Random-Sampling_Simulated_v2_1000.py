import pandas as pd
import numpy as np
import random

def simulate_T00v2_random_samples(input_file, expression_output_file, metadata_output_file, repeats_per_patient=3):
    """
    Simulates pseudo-bulk samples by randomly selecting tissues and assigning random proportions 
    (that add up to 100 and range between 5 - 85%) from multiple tissue samples belonging to the same patient,
    excluding Skin, Tonsil, and Mammary-gland tissues. Each sample is named as 
    T00_v2_{patient}_{random seed}_{num of selected tissues}. Avoids sampling more than one
    FemaleReproductive tissue (Cervix, Uterus, Ovary) per sample.

    Parameters:
        input_file (str): Path to the input expression matrix (tab-delimited with Geneid as first column).
        expression_output_file (str): Path to save the simulated expression matrix (tab-delimited .txt).
        metadata_output_file (str): Path to save tissue composition metadata (tab-delimited .txt).
        repeats_per_patient (int): Number of simulated samples to generate per patient.
    """
    # Set global seed for reproducibility
    random.seed(42)
    np.random.seed(42)

    # Load and prepare data
    expr = pd.read_csv(input_file, delim_whitespace=True)
    expr.set_index('Geneid', inplace=True)
    expr = expr.apply(pd.to_numeric)

    # CPM normalization
    def cpm_normalize(df):
        return df.div(df.sum(axis=0), axis=1) * 1e6

    cpm_expr = cpm_normalize(expr)

    # Extract patient IDs and tissues
    def extract_patient(col_name):
        return col_name.split('_')[0]

    def extract_tissue(col_name):
        return col_name.split('_', 1)[1] if '_' in col_name else ""

    patients = cpm_expr.columns.to_series().apply(extract_patient)
    tissues = cpm_expr.columns.to_series().apply(extract_tissue)

    excluded_tissues = {"Skin", "Tonsil", "Mammary-gland"}
    female_repro_tissues = {"Cervix", "Uterus", "Ovary"}
    simulated_samples = {}
    metadata_records = []

    unique_patients = patients.unique()

    for patient in unique_patients:
        # Filter valid columns for this patient
        valid_cols = (patients == patient) & (~tissues.isin(excluded_tissues))
        cols_for_patient = cpm_expr.loc[:, valid_cols]
        tissue_for_cols = tissues[valid_cols]

        num_tissues = cols_for_patient.shape[1]
        if num_tissues < 4:
            print(f"Skipping {patient}: only {num_tissues} usable tissues (need at least 4)")
            continue

        for _ in range(repeats_per_patient):
            max_attempts = 100  # to avoid infinite loops
            for attempt in range(max_attempts):
                num_to_select = random.randint(4, num_tissues)
                seed = random.randint(1000, 999999)
                selected_cols = cols_for_patient.sample(n=num_to_select, axis=1, random_state=seed)
                selected_tissues = tissue_for_cols[selected_cols.columns]

                # Check FemaleReproductive constraint
                selected_female_repro = set(selected_tissues).intersection(female_repro_tissues)
                if len(selected_female_repro) <= 1:
                    break  # valid selection
            else:
                print(f"Skipping one sample for {patient} after {max_attempts} failed attempts")
                continue  # move to next repeat

            # Generate random proportions that sum to 100 and are between 5% and 85%
            proportions = []
            remaining_percentage = 100  # We need the proportions to add up to 100
            for _ in range(num_to_select - 1):  # Select num_to_select - 1 proportions
                proportion = random.uniform(5, min(85, remaining_percentage - (num_to_select - len(proportions) - 1) * 5))
                proportions.append(proportion)
                remaining_percentage -= proportion

            # Add the remaining proportion to the last tissue to ensure the sum is 100
            proportions.append(remaining_percentage)

            # Round the proportions to 3 decimal places
            proportions = np.round(proportions, 3)

            # Simulate sample using weighted average of expression values
            weighted_sample = (selected_cols * proportions).sum(axis=1) / 100
            sim_name = f"T00_v2_{patient}_{seed}_{num_to_select}"
            simulated_samples[sim_name] = weighted_sample

            # Record tissue proportions
            tissue_props = dict(zip(selected_tissues, proportions))
            tissue_props["Sample"] = sim_name
            metadata_records.append(tissue_props)

    # Save expression matrix
    simulated_df = pd.DataFrame(simulated_samples)
    simulated_df.to_csv(expression_output_file, sep='\t')

    # Save metadata
    metadata_df = pd.DataFrame(metadata_records).fillna(0)
    metadata_df = metadata_df.set_index("Sample")
    metadata_df.to_csv(metadata_output_file, sep='\t')

simulate_T00v2_random_samples("20250616_All-Tissues-NoDup_Counts_Clean.txt", "20250616_All-Tissues-NoDup_Random_Simulated_v2_Counts.txt", "20250616_All-Tissues-NoDup_Random_Simulated_v2_Proportions.txt", repeats_per_patient=125)
