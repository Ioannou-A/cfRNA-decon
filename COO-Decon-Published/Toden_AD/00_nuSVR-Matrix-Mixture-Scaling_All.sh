#!/bin/bash

#$ -l h_vmem=4G          # Request 4GB of RAM
#$ -cwd                   # Run in the current working directory
#$ -l h_rt=48:00:00       # Set a runtime limit of 2.5 days
#$ -N Noisy_nuSVR_Scale     # Name theto job nuSVR-Decon
#$ -m ae
#$ -M s2556897@ed.ac.uk

# Load the Python environment (adjust if using a virtual environment or module system)
source /etc/profile.d/modules.sh
module load anaconda
source activate nusvr

# Run the Python script
python3 00_nuSVR-Matrix-Mixture-Scaling_All.py
