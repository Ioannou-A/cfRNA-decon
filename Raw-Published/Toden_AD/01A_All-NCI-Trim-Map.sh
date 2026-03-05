#!/bin/bash
# Load required modules
module load igmm/apps/TrimGalore/0.6.6
module load igmm/apps/cutadapt/4.6
module load igmm/apps/STAR/2.7.11b

# Define directories
BASE_DIR="Raw-Published"
RAW_DIR="${BASE_DIR}/Toden_AD/All-NCI-Raw-Fastq"
TRIMMED_DIR="${BASE_DIR}/Toden_AD/All-NCI-Trimmed"
ALIGNED_DIR="${BASE_DIR}/Toden_AD/All-NCI-Aligned"
SAMPLE_LIST="${BASE_DIR}/Toden_AD/All_NCI_sra_ids.txt"

# Create output directories
mkdir -p "$TRIMMED_DIR" "$ALIGNED_DIR"

# Loop through all forward read files
for R1_FILE in "$RAW_DIR"/*_1.fastq.gz; do
    # Extract sample basename (e.g., SRR13795881)
    BASENAME=$(basename "$R1_FILE" _1.fastq.gz)

    echo "Trimming sample: $BASENAME"

    # Define file paths for forward and reverse reads
    R1="$RAW_DIR/${BASENAME}_1.fastq.gz"
    R2="$RAW_DIR/${BASENAME}_2.fastq.gz"
    trim_galore --illumina --paired "$R1" "$R2" --output_dir ${TRIMMED_DIR}
done

for R1_FILE in "$TRIMMED_DIR"/*_1_val_1.fq.gz; do
    # Extract sample basename (e.g., SRR13795881)
    BASENAME=$(basename "$R1_FILE" _1_val_1.fq.gz)

    echo "Mapping sample: $BASENAME"

    # Define file paths for forward and reverse reads
    R1="$TRIMMED_DIR/${BASENAME}_1_val_1.fq.gz"
    R2="$TRIMMED_DIR/${BASENAME}_2_val_2.fq.gz"

    # Run STAR alignment
    STAR --runMode alignReads \
         --readFilesCommand zcat \
         --runThreadN 12 \
         --outFilterMultimapNmax 1 \
         --outReadsUnmapped Fastx \
         --genomeLoad NoSharedMemory \
         --limitBAMsortRAM 3200000000 \
         --genomeDir ${BASE_DIR}/GRCh38-STAR-Index/ \
         --sjdbGTFfile ${BASE_DIR}/gencode.v46.annotation.gtf \
         --readFilesIn "$R1" "$R2" \
         --outSAMtype BAM SortedByCoordinate \
         --outFileNamePrefix "${ALIGNED_DIR}/${BASENAME}"
done
