#!/bin/bash
#$ -cwd
#$ -l h_rt=655:00:00
#$ -pe sharedmem 4
#$ -t 1-825   # Adjust this based on the number of columns
#$ -N BDa-O_3000
#$ -m ae
#$ -M s2556897@ed.ac.uk

source /etc/profile.d/modules.sh
module load anaconda
source activate nusvr

python3 02_Decon-COO_nuSVR_BDa_Outer_3000_5000_10_R.py