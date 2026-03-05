#!/bin/bash

#$ -cwd
#$ -l h_rt=360:00:00
#$ -pe sharedmem 4
#$ -t 1-165 
#$ -N Top30_COO
#$ -m a
#$ -M s2556897@ed.ac.uk

# Load the Python environment (adjust if using a virtual environment or module system)
source /etc/profile.d/modules.sh
module load anaconda
source activate nusvr

# Run the Python script
python3 01_NuSVR-Decon_TSP-BDa_Outer_300_1500_10-top_30_percent_removed.py
