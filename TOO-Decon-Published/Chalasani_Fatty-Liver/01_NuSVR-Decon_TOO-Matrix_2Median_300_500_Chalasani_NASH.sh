#!/bin/bash

#$ -l h_vmem=2G          
#$ -cwd                  
#$ -l h_rt=72:00:00  
#$ -pe sharedmem 15         
#$ -N Sep1_NASH
#$ -m ae
#$ -M s2556897@ed.ac.uk

# Load the Python environment (adjust if using a virtual environment or module system)
source /etc/profile.d/modules.sh
module load anaconda
source activate nusvr

# Run the Python script
python3 01_NuSVR-Decon_TOO-Matrix_2Median_300_500_Chalasani_NASH.py

