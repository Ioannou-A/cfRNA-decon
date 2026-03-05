#!/bin/bash

module load igmm/apps/sratoolkit/3.1.1
set -euo pipefail

if [ "$#" -ne 2 ]; then
  echo "Usage: $0 <sra_id_list.txt> <sra_directory>"
  exit 1
fi

SRA_ID_FILE="$1"
SRA_DIR="$2"

while read -r id; do
  sra_path="${SRA_DIR}/${id}/${id}.sra"
  if [[ -f "$sra_path" ]]; then
    echo "  → Converting $id..."
    mkdir -p "${SRA_DIR}/tmpdir_${id}"
    fasterq-dump "$sra_path" --threads 8 --outdir "$SRA_DIR" --temp "${SRA_DIR}/tmpdir_${id}"
    echo "  → Compressing $id FASTQ files..."
    gzip "${SRA_DIR}/${id}_1.fastq" "${SRA_DIR}/${id}_2.fastq"
    rm -rf "${SRA_DIR}/tmpdir_${id}"
  else
    echo "  → SRA file for $id not found at $sra_path — skipping."
  fi
done < "$SRA_ID_FILE"

echo "All conversions and compressions completed."
