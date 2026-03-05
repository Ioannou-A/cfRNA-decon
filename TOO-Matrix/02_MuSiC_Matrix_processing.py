import pandas as pd
import re
import os

# Directory containing the files
directory = "TOO-Matrix/TOO-Matrices_MuSiC/"

# List of filenames to process
filenames = [
    "20250405_GeneID_LessTissueV2_2Median-Unique.tsv",
    "20250405_GeneID_LessTissueV2_Sampling10-Unique.tsv",
    "20250405_GeneID_LessTissueV2_Sampling5-Unique.tsv"
]

for fname in filenames:
    path = os.path.join(directory, fname)
    df = pd.read_csv(path, sep='\t')
    
    # Clean column names
    df.columns = [re.sub(r'\d+$', '', col) if col != 'GeneID' else col for col in df.columns]
    
    # Overwrite the original file
    df.to_csv(path, sep='\t', index=False)

print("All files cleaned and saved.")
