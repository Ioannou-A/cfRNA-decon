#!/bin/bash
#$ -cwd
#$ -l h_rt=47:00:00
#$ -l h_vmem=2G
#$ -pe sharedmem 6
#$ -t 1-165   # Adjust this based on the number of columns
#$ -N BDa-I_300
#$ -m ae
#$ -M s2556897@ed.ac.uk

source /etc/profile.d/modules.sh
module load anaconda
source activate nusvr

python3 02_Decon-COO_nuSVR_BDa_Inner_300_1500_10_R.py