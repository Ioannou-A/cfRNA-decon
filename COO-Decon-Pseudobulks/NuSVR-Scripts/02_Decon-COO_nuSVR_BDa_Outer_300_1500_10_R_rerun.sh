#!/bin/bash
#$ -cwd
#$ -l h_rt=120:00:00
#$ -t 1-210
#$ -N BDa_O_300
#$ -m a
#$ -M s2556897@ed.ac.uk

source /etc/profile.d/modules.sh
module load anaconda
source activate nusvr

python3 02_Decon-COO_nuSVR_BDa_Outer_300_1500_10_R_rerun.py
