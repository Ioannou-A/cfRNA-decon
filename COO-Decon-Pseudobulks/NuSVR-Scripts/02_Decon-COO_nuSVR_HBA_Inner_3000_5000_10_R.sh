#!/bin/bash
#$ -cwd
#$ -l h_rt=384:00:00
#$ -pe sharedmem 8
#$ -t 1-825
#$ -N HBA_3000
#$ -m ae
#$ -M s2556897@ed.ac.uk

source /etc/profile.d/modules.sh
module load anaconda
source activate nusvr

python3 02_Decon-COO_nuSVR_HBA_Inner_3000_5000_10_R.py