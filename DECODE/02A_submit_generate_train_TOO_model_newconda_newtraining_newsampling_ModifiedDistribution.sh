#!/bin/bash

#$ -N GTEx_TOO_Abundant
#$ -cwd
#$ -q gpu
#$ -l gpu=1
#$ -l h_rt=47:30:00
#$ -l h_rss=24G
#$ -pe sharedmem 10
#$ -m ae

set -euo pipefail

source /etc/profile.d/modules.sh
module load cuda/12.1.1
module load anaconda
conda activate DECODE_h200

echo "Job started on $(hostname)"
echo "Start time: $(date)"

python - <<'EOF'
import torch
print("CUDA available:", torch.cuda.is_available())
print("Torch CUDA version:", torch.version.cuda)
if torch.cuda.is_available():
    print("GPU:", torch.cuda.get_device_name(0))
EOF

python 02B_DECODE_GTEx-TOO_NewConda_NewTraining_NewSampling_ModifiedDistribution_Abundant.py

echo "End time: $(date)"
echo "Job finished"