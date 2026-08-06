#!/bin/bash

#$ -N Val_GTEx_GPU_5000
#$ -cwd
#$ -q gpu
#$ -l gpu=1
#$ -l h_rt=47:30:00
#$ -l h_rss=24G
#$ -pe sharedmem 10
#$ -m ae
#$ -M s2556897@ed.ac.uk

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

#python 05C_DECODE_GTEx-TOO_NewTraining_GPU_Training_DANNpatience3.py
#python 05C_DECODE_GTEx-TOO_NewTraining_GPU_Training_DANNpatience5.py
#python 05C_DECODE_GTEx-TOO_NewTraining_GPU_Training_DANNpatience10.py
#python 05C_DECODE_GTEx-TOO_NewTraining_GPU_Training_DANNpatience15.py
python 05C_DECODE_GTEx-TOO_NewTraining_GPU_Training_Curve.py

echo "End time: $(date)"
echo "Job finished"