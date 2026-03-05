#!/bin/bash
#$ -cwd
#$ -l h_rt=120:00:00
#$ -t 1-90
#$ -N BDaI_rerun
#$ -m ae
#$ -M s2556897@ed.ac.uk

source /etc/profile.d/modules.sh
module load anaconda
source activate nusvr

python3 02_Decon-COO_nuSVR_BDa_Inner_3000_5000_10_R_rerun.py