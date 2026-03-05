#!/bin/bash

#$ -cwd
#$ -l h_rt=47:00:00
#$ -pe sharedmem 4
#$ -t 1-91 
#$ -N Moufarrej_Norm_BDa-Outer
#$ -m ae
#$ -M s2556897@ed.ac.uk

# Load the Python environment
source /etc/profile.d/modules.sh
module load anaconda
source activate nusvr

# Run the Python script
python3 01_NuSVR-Decon_TSP-BDa_Outer_300_1500_10-Moufarrej_Normotensive.py
