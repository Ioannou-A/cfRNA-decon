#!/bin/bash

#$ -t 1-18                 # 18 tasks: each processes 10 samples (last task may do fewer)
#$ -l h_vmem=15G           # 15 GB memory per core
#$ -pe sharedmem 4         # 4 cores for STAR
#$ -cwd
#$ -l h_rt=24:00:00        # Max runtime 24 hours per task
#$ -N AD_Align
#$ -m ae
#$ -M s2556897@ed.ac.uk

# Load required modules
source /etc/profile.d/modules.sh
module load igmm/apps/TrimGalore/0.6.6
module load igmm/apps/cutadapt/4.6
module load igmm/apps/STAR/2.7.11b

# Define directories
BASE_DIR="Raw-Published"
RAW_DIR="${BASE_DIR}/Toden_AD/All-AD-Raw-Fastq"
TRIMMED_DIR="${BASE_DIR}/Toden_AD/All-AD-Trimmed"
ALIGNED_DIR="${BASE_DIR}/Toden_AD/All-AD-Aligned"
SAMPLE_LIST="${BASE_DIR}/Toden_AD/All_AD_sra_ids.txt"

# Create output directories
mkdir -p "$TRIMMED_DIR" "$ALIGNED_DIR"

# Parameters
SAMPLES_PER_TASK=10
TOTAL_SAMPLES=$(grep -c . "$SAMPLE_LIST")   # count non-empty lines safely

# Calculate start and end line for this task
START=$(( (SGE_TASK_ID - 1) * SAMPLES_PER_TASK + 1 ))
END=$(( SGE_TASK_ID * SAMPLES_PER_TASK ))

# Loop over assigned samples
for (( i=START; i<=END && i<=TOTAL_SAMPLES; i++ )); do
    BASENAME=$(sed -n "${i}p" "$SAMPLE_LIST")
    BASENAME=$(echo "$BASENAME" | tr -d '[:space:]')   # strip whitespace
    
    [[ -z "$BASENAME" ]] && continue   # skip empty lines
    
    echo "Processing sample $i: $BASENAME"

    # Define raw FASTQ paths
    R1="${RAW_DIR}/${BASENAME}_1.fastq.gz"
    R2="${RAW_DIR}/${BASENAME}_2.fastq.gz"

    # Check if input files exist
    if [[ ! -f "$R1" || ! -f "$R2" ]]; then
        echo "WARNING: Missing FASTQ files for $BASENAME, skipping." >&2
        continue
    fi

    # Step 1: Trim reads
    echo "Running Trim Galore for $BASENAME..."
    trim_galore --illumina --paired "$R1" "$R2" --output_dir "$TRIMMED_DIR"

    # Define trimmed file paths
    TRIM_R1="${TRIMMED_DIR}/${BASENAME}_1_val_1.fq.gz"
    TRIM_R2="${TRIMMED_DIR}/${BASENAME}_2_val_2.fq.gz"

    # Step 2: Align with STAR
    echo "Running STAR alignment for $BASENAME..."
    STAR --runMode alignReads \
         --readFilesCommand zcat \
         --runThreadN 4 \
         --outFilterMultimapNmax 1 \
         --outReadsUnmapped Fastx \
         --genomeLoad NoSharedMemory \
         --limitBAMsortRAM 3200000000 \
         --genomeDir "${BASE_DIR}/GRCh38-STAR-Index/" \
         --sjdbGTFfile "${BASE_DIR}/gencode.v46.annotation.gtf" \
         --readFilesIn "$TRIM_R1" "$TRIM_R2" \
         --outSAMtype BAM SortedByCoordinate \
         --outFileNamePrefix "${ALIGNED_DIR}/${BASENAME}."

    echo "Sample $BASENAME complete."
done
