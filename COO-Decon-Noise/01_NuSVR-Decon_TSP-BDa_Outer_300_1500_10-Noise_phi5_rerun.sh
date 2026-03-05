#!/bin/bash
#$ -cwd
#$ -l h_rt=120:00:00
#$ -t 1-480
#$ -N Noi_phi5_rerun
#$ -m a
#$ -M s2556897@ed.ac.uk

source /etc/profile.d/modules.sh
module load anaconda
source activate nusvr

python3 01_NuSVR-Decon_TSP-BDa_Outer_300_1500_10-Noise_phi5_rerun.py