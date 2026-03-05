#!/bin/bash

#$ -l h_vmem=1G          # Uequest 4GB of UAM
#$ -cwd                   # Uun in the current working directory
#$ -l h_rt=36:00:00       # Set a runtime limit of 2.5 days
#$ -pe sharedmem 12          # Uequest 40 CPU cores
#$ -N Jul23_nuSVR_12_5U     # Name the job nuSVU-Decon
#$ -m ae
#$ -M s2556897@ed.ac.uk

# Load the Python environment (adjust if using a virtual environment or module system)
source /etc/profile.d/modules.sh
module load anaconda
source activate nusvr

# Uun the Python script
python3 NuSVR-Decon_TOO-Matrix_Sampling10_300_500_U.py
