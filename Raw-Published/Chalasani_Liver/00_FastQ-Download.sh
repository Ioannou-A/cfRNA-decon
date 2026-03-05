#!/bin/bash

# Script to download .sra files using prefetch and convert them to gzipped FASTQ files
# Usage: ./ healthy_sra_ids.txt Healthy-Raw-Fastq
module load igmm/apps/sratoolkit/3.1.1

set -euo pipefail

# Check input arguments
if [ "$#" -ne 2 ]; then
  echo "Usage: $0 <sra_id_list.txt> <output_directory>"
  exit 1
fi

SRA_ID_FILE="$1"
OUTDIR="$2"

# Create output directory
mkdir -p "$OUTDIR"
cd "$OUTDIR"

# Download .sra files
echo "Downloading .sra files..."
while IFS= read -r id; do
  [ -z "$id" ] && continue   # skip blank lines
  echo "  → Prefetching $id..."
  prefetch "$id"
done < "../$SRA_ID_FILE"

# Convert to FASTQ and compress
echo "Converting .sra to FASTQ and compressing..."
while IFS= read -r id; do
  [ -z "$id" ] && continue   # skip blank lines
  echo "  → Processing $id..."
  fasterq-dump "$id" --split-files --threads 8 --outdir ./
  gzip -f "${id}_1.fastq" "${id}_2.fastq"
done < "../$SRA_ID_FILE"
