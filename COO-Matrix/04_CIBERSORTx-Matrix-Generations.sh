#!/bin/bash

# Insert here your credentials of CIBERSORTx generated from https://cibersortx.stanford.edu/
CIBERSORTX_USERNAME="your_email@domain"
CIBERSORTX_TOKEN="your_token_here"

# Define your specific combinations for gmin and gmax
gmin_gmax_pairs=("300 1500" "1000 3000" "3000 5000")

# Define the other lists
replicates=(10)
conditions=("TSP-HBA_Inner" "TSP-BDa_Outer" "TSP-BDa_Inner")

# Loop over the gmin-gmax combinations
for pair in "${gmin_gmax_pairs[@]}"; do
  # Split the pair into gmin and gmax
  gmin=$(echo $pair | cut -d ' ' -f 1)
  gmax=$(echo $pair | cut -d ' ' -f 2)

  for r in "${replicates[@]}"; do
    for cond in "${conditions[@]}"; do
        # Create the directory
        dir_name="CIBERSORTx-Matrix_${cond}_${gmin}_${gmax}_${r}"
        mkdir "$dir_name"
      
        # Generate this combinations of ref matrices
        docker run -v COO-Matrix:/src/data -v COO-Matrix/${dir_name}:/src/outdir cibersortx/fractions --username "$CIBERSORTX_USERNAME" --token "$CIBERSORTX_TOKEN" \
         --single_cell TRUE --refsample ${cond}_25each.txt --G.min ${gmin} --G.max ${gmax} --fraction 0.25 --replicates ${r}
    done
  done
done
