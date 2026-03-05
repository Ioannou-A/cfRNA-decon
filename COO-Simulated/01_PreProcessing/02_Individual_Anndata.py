import os
import glob
import scanpy as sc

# Get the current working directory
cwd = os.getcwd()

# Define input and output directories
input_dir = os.path.join(cwd, "01_Modified-h5ad")
output_dir = os.path.join(cwd, "02_Individual-h5ad")

# Create output directory if it doesn't exist
os.makedirs(output_dir, exist_ok=True)

# Find all H5 files in the specified input directory
h5ad_files = glob.glob(os.path.join(input_dir, "*_modified.h5ad"))

donors_to_keep = {'TSP21', 'TSP25', 'TSP27'}

for h5ad_file in h5ad_files:
    print(f"Processing {h5ad_file}...")

    # Load the AnnData object
    filtered_data = sc.read_h5ad(h5ad_file)

    # Check if 'donor' and 'method' columns exist in obs before filtering
    if 'donor' in filtered_data.obs and 'method' in filtered_data.obs:
        for donor in donors_to_keep:
            donor_filtered_data = filtered_data[
                (filtered_data.obs['donor'] == donor) & (filtered_data.obs['method'] == '10X')
            ].copy()

            if donor_filtered_data.n_obs > 0:
                # Split the file name by underscores and extract the first part
                base_filename = os.path.splitext(os.path.basename(h5ad_file))[0]
                parts = base_filename.split('_')
                donor_name = donor
                tissue = parts[0]

                # Construct output filename
                output_filename = f"{donor_name}_{tissue}_10X.h5ad"
                donor_filename = os.path.join(output_dir, output_filename)
                # Save modified data for each donor
                donor_filtered_data.write(donor_filename)
                print(f"Saved modified data for {donor} to: {donor_filename}")

