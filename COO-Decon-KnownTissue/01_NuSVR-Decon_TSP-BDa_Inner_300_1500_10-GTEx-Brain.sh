#!/bin/bash

#$ -l h_vmem=2G          
#$ -cwd                  
#$ -l h_rt=120:00:00  
#$ -pe sharedmem 15         
#$ -N Jul16_nuSVR_Healthy     
#$ -m ae
#$ -M s2556897@ed.ac.uk

# Load the Python environment (adjust if using a virtual environment or module system)
source /etc/profile.d/modules.sh
module load anaconda
source activate nusvr

# Run the Python script
python3 01_NuSVR-Decon_TSP-BDa_Inner_300_1500_10-GTEx-Brain.py
