#!/bin/bash

# Insert here your credentials of CIBERSORTx generated from https://cibersortx.stanford.edu/
CIBERSORTX_USERNAME="your_email@domain"
CIBERSORTX_TOKEN="your_token_here"

# Define your specific combinations for gmin and gmax
gmin_gmax_pairs=("300 500" "500 1000" "1000 1500" "1500 2000")

# Define the other lists
conditions=("Sampling5_5" "Sampling10_10" "2Median_2")

# Loop over the gmin-gmax combinations
for pair in "${gmin_gmax_pairs[@]}"; do
  # Split the pair into gmin and gmax
  gmin=$(echo $pair | cut -d ' ' -f 1)
  gmax=$(echo $pair | cut -d ' ' -f 2)

  for pair2 in "${conditions[@]}"; do
    rep=$(echo $pair2 | cut -d '_' -f 2)
    condition=$(echo $pair2 | cut -d '_' -f 1)

    for cond in "${condition[@]}"; do
  
      sed '1s/[0-9]//g; 1s/_/ /g' TOO-Matrix/20250405_GeneID_LessTissueV2_${cond}-Unique.tsv > TOO-Matrix/20250405_GeneID_LessTissueV2_${cond}.txt
      awk 'BEGIN {FS=OFS="\t"} { $1 = gensub(/[0-9]+/, "", "g", $1); $1 = gensub(/_/, " ", "g", $1); print }' TOO-Matrix/20250405_PhenotypeClass_LessTissueV2_${cond}.tsv > TOO-Matrix/20250405_PhenotypeClass_LessTissueV2_${cond}.txt
      # Create the directory
      dir_name="CIBERSORTx-TOO-Matrix_${cond}_${gmin}_${gmax}"
      mkdir "$dir_name"

      # Q cutoff of 0.01 was used for all initial matrices
      # Generate this combinations of ref matrices. Rep represent the number of tissues sampled
      docker run -v "$PWD":/src/data -v "$PWD"/${dir_name}:/src/outdir cibersortx/fractions --username "$CIBERSORTX_USERNAME" --token "$CIBERSORTX_TOKEN" \
        --replicates ${rep} --refsample TOO-Matrix/20250405_GeneID_LessTissueV2_${cond}.txt --phenoclasses TOO-Matrix/20250405_PhenotypeClass_LessTissueV2_${cond}.txt --G.min ${gmin} --G.max ${gmax} --q.value 0.01
    done  
  done
done
