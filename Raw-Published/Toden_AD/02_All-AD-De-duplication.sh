#!/bin/bash
#$ -l h_vmem=15G
#$ -pe sharedmem 8
#$ -cwd
#$ -l h_rt=47:00:00
#$ -N AD_Dedup
#$ -m ae
#$ -M s2556897@ed.ac.uk

# Load samtools
source /etc/profile.d/modules.sh
module load igmm/apps/samtools/1.20

ALIGNED_DIR="Raw-Published/Toden_AD/All-AD-Aligned"

for FILE in "$ALIGNED_DIR"/*Aligned.sortedByCoord.out.bam; do
    BASENAME=$(basename "$FILE" Aligned.sortedByCoord.out.bam)
    echo "Processing sample: $BASENAME"

    # Step 1: Sort by name
    samtools sort -n --threads 8 "$FILE" -o "${ALIGNED_DIR}/${BASENAME}.name_sorted.bam"

    # Step 2: Fixmate
    samtools fixmate -m --threads 8 "${ALIGNED_DIR}/${BASENAME}.name_sorted.bam" "${ALIGNED_DIR}/${BASENAME}.fixmate.bam"

    # Step 3: Sort by coordinate
    samtools sort --threads 8 "${ALIGNED_DIR}/${BASENAME}.fixmate.bam" -o "${ALIGNED_DIR}/${BASENAME}.coord_sorted.bam"

    # Step 4: Markdup (remove duplicates)
    samtools markdup -r --threads 8 "${ALIGNED_DIR}/${BASENAME}.coord_sorted.bam" "${ALIGNED_DIR}/${BASENAME}.nodup.bam"

    # Step 5: Index deduplicated BAM
    samtools index "${ALIGNED_DIR}/${BASENAME}.nodup.bam"

    # Step 6 (Optional): Clean up intermediate files
    rm "${ALIGNED_DIR}/${BASENAME}.name_sorted.bam" \
       "${ALIGNED_DIR}/${BASENAME}.fixmate.bam" \
       "${ALIGNED_DIR}/${BASENAME}.coord_sorted.bam"

    echo "Finished processing $BASENAME"
done
