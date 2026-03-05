def simulate_T00v2_uniform_samples(input_file, expression_output_file, metadata_output_file, total_repeats=100):
    """
    Simulates a fixed total number of pseudo samples by averaging CPM-normalized expression values
    from multiple tissue samples belonging to the same patient. Avoids Skin, Tonsil, Mammary-gland tissues,
    and limits to one FemaleReproductive tissue (Cervix, Uterus, Ovary) per simulated sample.

    Each sample is named as T00_v2_{patient}_{random seed}_{number of selected tissues}.

    Parameters:
        input_file (str): Path to input expression matrix (tab-delimited, Geneid as first column).
        expression_output_file (str): Path to save simulated expression matrix.
        metadata_output_file (str): Path to save tissue composition metadata.
        total_repeats (int): Total number of unique simulated samples to generate across all patients.
    """
    import pandas as pd
    import numpy as np
    import random
    from itertools import combinations

    # Set seed for reproducibility
    random.seed(42)
    np.random.seed(42)

    # Load the input expression matrix and preprocess
    expr = pd.read_csv(input_file, delim_whitespace=True)
    expr.set_index('Geneid', inplace=True)
    expr = expr.apply(pd.to_numeric)

    # CPM normalization: counts per million
    def cpm_normalize(df):
        return df.div(df.sum(axis=0), axis=1) * 1e6

    cpm_expr = cpm_normalize(expr)

    # Extract patient and tissue identifiers from column names
    def extract_patient(col_name):
        return col_name.split('_')[0]

    def extract_tissue(col_name):
        return col_name.split('_', 1)[1] if '_' in col_name else ""

    patients = cpm_expr.columns.to_series().apply(extract_patient)
    tissues = cpm_expr.columns.to_series().apply(extract_tissue)

    # Define tissue constraints
    excluded_tissues = {"Skin", "Tonsil", "Mammary-gland"}
    female_repro_tissues = {"Cervix", "Uterus", "Ovary"}

    # Output containers
    simulated_samples = {}       # Simulated expression profiles
    metadata_records = []        # Tissue composition per sample

    # Get list of all patients and initialize duplicate-check dict
    unique_patients = patients.unique()
    used_combinations = {patient: set() for patient in unique_patients}

    total_generated = 0  # Global counter for total number of samples

    # Continue sampling until the desired number of total samples is reached
    while total_generated < total_repeats:
        # Randomly choose a patient
        patient = random.choice(unique_patients)

        # Filter out excluded tissues for this patient
        valid_cols = (patients == patient) & (~tissues.isin(excluded_tissues))
        cols_for_patient = cpm_expr.loc[:, valid_cols]
        tissue_for_cols = tissues[valid_cols]
        num_tissues = cols_for_patient.shape[1]

        # Skip if not enough tissues to simulate
        if num_tissues < 3:
            continue

        # Try up to N times to find a valid, unique tissue combination
        max_attempts = 50
        for _ in range(max_attempts):
            # Randomly choose a number of tissues to combine
            num_to_select = random.randint(3, num_tissues)

            # Sample the columns and get associated tissues
            seed = random.randint(1000, 9999)
            selected_cols = cols_for_patient.sample(n=num_to_select, axis=1, random_state=seed)
            selected_tissues = tissue_for_cols[selected_cols.columns]

            # Sort tissue names for consistent comparison
            selected_tissue_list = tuple(sorted(selected_tissues.tolist()))

            # Skip if this tissue combination has been used before for this patient
            if selected_tissue_list in used_combinations[patient]:
                continue

            # Check FemaleReproductive constraint
            selected_female_repro = set(selected_tissues).intersection(female_repro_tissues)
            if len(selected_female_repro) > 1:
                continue  # Invalid sample

            # Passed all checks — use this combination
            used_combinations[patient].add(selected_tissue_list)

            # Create simulated expression by averaging
            simulated_sample = selected_cols.mean(axis=1)
            sim_name = f"T00_v2_{patient}_{seed}_{num_to_select}"
            simulated_samples[sim_name] = simulated_sample

            # Record tissue proportions (normalized)
            tissue_counts = selected_tissues.value_counts(normalize=True).sort_index()
            tissue_props = tissue_counts.to_dict()
            tissue_props["Sample"] = sim_name
            metadata_records.append(tissue_props)

            total_generated += 1
            break  # Stop retrying this patient, move on to next

    # Save expression matrix
    simulated_df = pd.DataFrame(simulated_samples)
    simulated_df.to_csv(expression_output_file, sep='\t')

    # Save metadata
    metadata_df = pd.DataFrame(metadata_records).fillna(0)
    metadata_df = metadata_df.set_index("Sample")
    metadata_df.to_csv(metadata_output_file, sep='\t')

simulate_T00v2_uniform_samples("20250616_All-Tissues-NoDup_Counts_Clean.txt", "20250616_All-Tissues-NoDup_Uniform_Simulated_v2_Counts.txt", "20250616_All-Tissues-NoDup_Uniform_Simulated_v2_Proportions.txt", total_repeats=250)
