#!/bin/bash
#$ -cwd
#$ -l h_rt=384:00:00
#$ -pe sharedmem 8
#$ -t 1-825
#$ -N BDa-O_300
#$ -m ae
#$ -M s2556897@ed.ac.uk

source /etc/profile.d/modules.sh
module load anaconda
source activate nusvr

python3 02_Decon-COO_nuSVR_BDa_Outer_300_1500_10_R.py

## Adapted this to process one sample at a time to make it faster