#!/bin/bash

#$ -cwd
#$ -l h_rt=96:00:00
#$ -pe sharedmem 8
#$ -t 1-25 
#$ -N Un20_COO
#$ -m ae
#$ -M s2556897@ed.ac.uk

# Load the Python environment (adjust if using a virtual environment or module system)
source /etc/profile.d/modules.sh
module load anaconda
source activate nusvr

# Run the Python script
python3 01_NuSVR-Decon_TSP-BDa_Outer_300_1500_10-20_percent_removed.py

