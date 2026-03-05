#!/bin/bash

#$ -l h_vmem=1G          # Request 4GB of RAM
#$ -cwd                   # Run in the current working directory
#$ -l h_rt=47:00:00       # Set a runtime limit of 47 hours
#$ -pe sharedmem 12          # Request 40 CPU cores
#$ -N Jul26_top40     # Name the job nuSVR-Decon
#$ -m ae
#$ -M s2556897@ed.ac.uk

# Load the Python environment (adjust if using a virtual environment or module system)
source /etc/profile.d/modules.sh
module load anaconda
source activate nusvr

# Run the Python script
# python3 NuSVR-Decon_TOO-Matrix_2Median_300_500_top10_R.py
# python3 NuSVR-Decon_TOO-Matrix_2Median_300_500_top20_R.py
# python3 NuSVR-Decon_TOO-Matrix_2Median_300_500_top30_R.py
python3 NuSVR-Decon_TOO-Matrix_2Median_300_500_top40_R.py
