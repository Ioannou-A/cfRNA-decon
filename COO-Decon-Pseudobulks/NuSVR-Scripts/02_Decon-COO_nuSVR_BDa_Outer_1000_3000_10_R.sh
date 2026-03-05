#!/bin/bash
#$ -cwd
#$ -l h_rt=300:00:00
#$ -pe sharedmem 8
#$ -t 6-825   # Adjust this based on the number of columns
#$ -N BDa-O_1000
#$ -m ae
#$ -M s2556897@ed.ac.uk

source /etc/profile.d/modules.sh
module load anaconda
source activate nusvr

python3 02_Decon-COO_nuSVR_BDa_Outer_1000_3000_10_R.py