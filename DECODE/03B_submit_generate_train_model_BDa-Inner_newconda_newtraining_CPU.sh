#!/bin/bash

#$ -N CPU_BDa_Inner_s600_a50_ab1_Final_extra31.5k
#$ -cwd
#$ -l h_rt=100:00:00
#$ -l h_rss=24G
#$ -pe sharedmem 10
#$ -m ae
#$ -M s2556897@ed.ac.uk

set -euo pipefail

source /etc/profile.d/modules.sh
module load anaconda
conda activate DECODE_h200

echo "Job started on $(hostname)"
echo "Start time: $(date)"

#python 03A_DECODE_BDa-Inner_NewTraining_NewSampling_ModifiedDistribution_CPU_Pseudobulk.py
python 03A_DECODE_BDa-Inner_NewTraining_NewSampling_ModifiedDistribution_CPU_Pseudobulk_extra.py

echo "End time: $(date)"
echo "Job finished"