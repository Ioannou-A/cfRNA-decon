#!/bin/bash
#$ -cwd
#$ -l h_rt=72:00:00
#$ -l h_vmem=3G
#$ -pe sharedmem 6
#$ -t 1-165   # Adjust this based on the number of columns
#$ -N BDa-I_1000
#$ -m ae
#$ -M s2556897@ed.ac.uk

source /etc/profile.d/modules.sh
module load anaconda
source activate nusvr

python3 02_Decon-COO_nuSVR_BDa_Inner_1000_3000_10_R.py