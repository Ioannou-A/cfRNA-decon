#!/bin/bash
#$ -cwd
#$ -l h_rt=168:00:00
#$ -t 1-30
#$ -N HBA_300
#$ -m a
#$ -M s2556897@ed.ac.uk

source /etc/profile.d/modules.sh
module load anaconda
source activate nusvr

python3 02_Decon-COO_nuSVR_HBA_Inner_300_1500_10_R_rerun.py