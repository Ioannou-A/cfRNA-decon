#!/bin/bash

# All the NASH passed the rRNA and DNA contamination thresholds
module load anaconda
conda activate featurecounts

NASH_dir="Raw-Published/Chalasani_Liver/All-NASH-Aligned"
gtf="Raw-Published/gencode.v46.annotation.gtf"

# All the NASH passed the rRNA and DNA contamination thresholds

featureCounts -p -g gene_name -t exon -a "$gtf" -Q 10 -T 10 -F GTF -o "$NASH_dir/All-NASH_Counts_v46.txt" "$NASH_dir"/*nodup.bam

# 2) Clean header + drop cols 2–6 -> counts-only table
clean_counts="$NASH_dir/All-NASH_Counts_v46_Clean.txt"
tail -n +2 "$NASH_dir/All-NASH_Counts_v46.txt" | \
  cut -f1,7- | \
  awk 'BEGIN{OFS="\t"}
       NR==1 {
         # Clean each sample name separately: strip path and remove "..nodup.bam"
         for (i=2; i<=NF; i++) {
           sub(".*/","",$i);                 # basename
           gsub("\\.\\.nodup\\.bam$","",$i) # drop ..nodup.bam
           gsub("\\.bam$","",$i)            # (just in case)
         }
         print; next
       }
       { print }' \
  > "$clean_counts"