#!/bin/bash
#$ -cwd
#$ -l h_rt=360:00:00
#$ -pe sharedmem 4
#$ -t 1-825
#$ -N BDa-I_3000
#$ -m ae
#$ -M s2556897@ed.ac.uk

source /etc/profile.d/modules.sh
module load anaconda
source activate nusvr

python3 02_Decon-COO_nuSVR_BDa_Inner_3000_5000_10_R.py