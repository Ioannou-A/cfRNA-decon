#!/bin/bash

#$ -cwd
#$ -l h_rt=47:00:00
#$ -l h_vmem=3G
#$ -pe sharedmem 4
#$ -t 19-26
#$ -N Toden_AD
#$ -m ae
#$ -M s2556897@ed.ac.uk

# Load the Python environment (adjust if using a virtual environment or module system)
source /etc/profile.d/modules.sh
module load anaconda
source activate nusvr

# Run the Python script
python3 01_NuSVR-Decon_TSP-BDa_Outer_300_1500_10-Toden_AD.py
