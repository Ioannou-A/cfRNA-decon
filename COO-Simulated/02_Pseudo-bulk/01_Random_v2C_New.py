import os
import numpy as np
import scanpy as sc
import pandas as pd

def subsample_random(ref_path, out_dir, min_cells_per_ct=50, total_cells=500, 
                      write=True, ct_key="cell_ontology_class", random_seed=None, repeats=1):
    # Read the input AnnData file
    ref_adata = sc.read_h5ad(ref_path)
    
    # Set random seed for reproducibility if provided
    if random_seed is not None:
        np.random.seed(random_seed)
    
    # Extract a unique identifier from the reference file name
    tsp = os.path.basename(ref_path).split('_')[0]
    
    # Create output directory if it doesn't exist
    os.makedirs(out_dir, exist_ok=True)
    
    # Precompute cell type indices for efficiency
    cell_type_indices = ref_adata.obs.groupby(ct_key, observed=False)[[]].apply(lambda x: x.index.to_list()).to_dict()
    
    # Filter out cell types with fewer than min_cells_per_ct occurrences
    valid_cell_types = [ct for ct in cell_type_indices if len(cell_type_indices[ct]) >= min_cells_per_ct]
    all_selected_cts = set()
    proportion_records = []  # Store proportions for all subsampled datasets
    all_adatas = []
    all_paths = []
    
    for i in range(repeats):  # Perform multiple independent subsampling runs
        # Randomly select between 4 and 15 cell types
        num_selected_cts = np.random.randint(4, min(16, len(valid_cell_types) + 1))
        selected_cts = np.random.choice(valid_cell_types, num_selected_cts, replace=False)
        all_selected_cts.update(selected_cts)  # Track all selected cell types
        
        # Determine the maximum allowable cells for each selected cell type
        max_cells_per_ct = {ct: len(cell_type_indices[ct]) for ct in selected_cts}
        
        # --- NEW SAFE BLOCK (no while loop) ---
        proportions = np.random.dirichlet(np.ones(num_selected_cts))
        proportions = np.round(proportions, 2)
        required_cells = {}
        remaining = total_cells

        # Assign all but the last CT
        for ct, prop in zip(selected_cts[:-1], proportions[:-1]):
            n = int(total_cells * prop)
            n = max(min_cells_per_ct, min(n, max_cells_per_ct[ct]))  # enforce min/max
            required_cells[ct] = n
            remaining -= n

        # Assign remainder to the last CT
        last_ct = selected_cts[-1]
        n_last = max(min_cells_per_ct, min(remaining, max_cells_per_ct[last_ct]))
        required_cells[last_ct] = n_last

        # Adjustment: fix total to exactly total_cells
        diff = total_cells - sum(required_cells.values())
        if diff != 0:
            required_cells[last_ct] = max(min_cells_per_ct,
                                          min(max_cells_per_ct[last_ct],
                                              required_cells[last_ct] + diff))
        # --- END NEW SAFE BLOCK ---
        
        # Generate output file path using the corrected filename format
        filename = f"{tsp}_random_rep{i+1}_seed{random_seed}_{min_cells_per_ct}_{total_cells}.h5ad"
        path = os.path.join(out_dir, filename)
        
        # Sample cells based on adjusted proportions
        sampled_indices = []
        for cell_type, num_samples in required_cells.items():
            sampled_indices.extend(np.random.choice(cell_type_indices[cell_type], size=num_samples, replace=False))
        
        # Subset the data to the sampled indices and create a new AnnData object
        adata_sub = ref_adata[sampled_indices].copy()
        
        # Store the proportions used for this subsampling as percentages rounded to 3 decimal places
        proportion_percentages = {ct: round((count / adata_sub.n_obs) * 100, 3) for ct, count in required_cells.items()}
        
        # Append the proportion record with filename
        proportion_records.append({"Filename": filename, "TotalCells": adata_sub.n_obs, ** proportion_percentages})

        # Optionally write the subsampled data to disk
        if write:
            adata_sub.write(path)
            print("Write AnnData to", path)
        
        # Store results from this repeat
        all_adatas.append(adata_sub)
        all_paths.append(path)
    
    # Convert proportion records to DataFrame
    proportion_df = pd.DataFrame(proportion_records)
    
    # Ensure all columns for selected cell types exist, filling missing values with 0
    proportion_df = proportion_df.reindex(columns=["Filename", "TotalCells"] + sorted(all_selected_cts))
    proportion_df.fillna(0, inplace=True)
    
    # Save proportions to a tab-separated text file
    proportion_file = os.path.join(out_dir, f"{tsp}_seed{random_seed}_{min_cells_per_ct}_{total_cells}_subsampling_proportions.txt")
    proportion_df.to_csv(proportion_file, sep='\t', index=False)
    print("Saved proportions to", proportion_file)
    
    return all_adatas, all_paths

# --- MAIN SCRIPT ---

# Define input parameters
out_dir = "Random_v2C_New"
write = True
ct_key = "cell_ontology_class"
repeats = 5

# Donors to iterate over
donors = ["TSP21", "TSP25", "TSP27"]

# Random seeds
random_seeds = [8, 9, 10, 11, 12, 13, 3, 4, 5, 6, 7]

# Combinations of min_cells_per_ct and total_cells
cell_params = [
    (10, 200),
    (20, 400),
    (30, 600),
    (40, 800),
    (50, 1000),
]

# Loop over donors, random seeds, and cell parameter combinations
for donor in donors:
    ref_path = f"COO-Simulated/02_Pseudo-bulk/{donor}/{donor}_merged_processed_filtered.h5ad"

    # Ensure the input file exists before processing
    if not os.path.exists(ref_path):
        print(f"Skipping {ref_path} (file not found)")
        continue

    for random_seed in random_seeds:
        for min_cells_per_ct, total_cells in cell_params:
            print(f"Running for donor={donor}, min_cells_per_ct={min_cells_per_ct}, total_cells={total_cells}, seed={random_seed}")

            # Call the function
            subsample_random(
                ref_path=ref_path,
                out_dir=out_dir,
                min_cells_per_ct=min_cells_per_ct,
                total_cells=total_cells,
                write=write,
                ct_key=ct_key,
                random_seed=random_seed,
                repeats=repeats
            )
