import pandas as pd
import numpy as np

def simulate_T00v2_pseudobulk(expression_file, proportions_file, output_file):
    """
    Generates bulk samples by combining tissue-specific expression data
    according to predefined proportions (from the existing TOO v2 file).

    Parameters:
        input_file (str): Path to the input expression matrix (tab-delimited with Geneid as first column).
        proportions_file (str): Path to the existing proportions file.
        output_file (str): Path to save the simulated pseudo-bulk expression matrix.
    """
    # Load expression and proportions
    expr = pd.read_csv(expression_file, delim_whitespace=True)
    expr.set_index('Geneid', inplace=True)
    expr = expr.apply(pd.to_numeric)

    proportions_df = pd.read_csv(proportions_file, delim_whitespace=True)
    proportions_df.set_index('Sample', inplace=True)

    # CPM normalization
    cpm_expr = expr.div(expr.sum(axis=0), axis=1) * 1e6

    simulated_samples = {}

    for sample_name, tissue_props in proportions_df.iterrows():
        # Identify patient from sample_name
        patient = sample_name.split('_')[2]

        # Determine columns in expr corresponding to the tissues for this patient
        selected_cols = []
        selected_weights = []

        for tissue, prop in tissue_props.items():
            if prop > 0:
                # Match columns like "patient_tissue_simN"
                pattern = f"{patient}_{tissue}"
                matched_cols = [col for col in cpm_expr.columns if col.startswith(pattern)]
                if matched_cols:
                    # pick first match (or could sample)
                    selected_cols.append(matched_cols[0])
                    selected_weights.append(prop)

        if not selected_cols:
            print(f"Warning: no matching columns for sample {sample_name}")
            continue

        # Compute weighted sum
        selected_df = cpm_expr[selected_cols]
        weights = np.array(selected_weights)
        weighted_sample = (selected_df * weights).sum(axis=1) / weights.sum()
        simulated_samples[sample_name] = weighted_sample

    # Save simulated expression matrix
    simulated_df = pd.DataFrame(simulated_samples)
    simulated_df.to_csv(output_file, sep='\t')


# Define file paths
proportions_file = "20250616_All-Tissues-NoDup_Random_Simulated_v2_Proportions.txt"

for noise_level in range(1, 11):  # 0.1 to 1.0
    noise_value = noise_level / 10
    input_file = f"20250616_All-Tissues-NoDup_Noise{noise_value}.txt"
    output_file = f"20250616_All-Tissues-NoDup_Noise{noise_value}_Counts.txt"

    simulate_T00v2_pseudobulk(input_file, proportions_file, output_file)
    print(f"Processed noise level {noise_value}")
