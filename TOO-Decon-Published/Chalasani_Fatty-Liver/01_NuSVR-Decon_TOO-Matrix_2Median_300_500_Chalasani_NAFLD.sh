#!/bin/bash

#$ -l h_vmem=1G          
#$ -cwd                  
#$ -l h_rt=47:00:00  
#$ -pe sharedmem 12         
#$ -N Sep1_nuSVR_NAFLD
#$ -m ae
#$ -M s2556897@ed.ac.uk

# Load the Python environment (adjust if using a virtual environment or module system)
source /etc/profile.d/modules.sh
module load anaconda
source activate nusvr

# Run the Python script
python3 01_NuSVR-Decon_TOO-Matrix_2Median_300_500_Chalasani_NAFLD.py
