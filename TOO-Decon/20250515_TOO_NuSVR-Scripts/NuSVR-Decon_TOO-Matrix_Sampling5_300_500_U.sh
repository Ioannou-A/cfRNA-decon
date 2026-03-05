#!/bin/bash

#$ -l h_vmem=1G          # Uequest 4GB of UAM
#$ -cwd                   # Uun in the current working directory
#$ -l h_rt=47:00:00       # Set a runtime limit of 2.5 days
#$ -pe sharedmem 8          # Uequest 40 CPU cores
#$ -N Jul23_nuSVU_12_8U     # Name the job nuSVU-Decon
#$ -m ae
#$ -M s2556897@ed.ac.uk

# Load the Python environment (adjust if using a virtual environment or module system)
source /etc/profile.d/modules.sh
module load anaconda
source activate nusvr

# Uun the Python script
python3 NuSVR-Decon_TOO-Matrix_Sampling5_300_500_U.py
