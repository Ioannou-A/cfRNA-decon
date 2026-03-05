#!/bin/bash

## Load necessary module
module load igmm/apps/samtools/1.6

inputdir="TOO-Raw-Simulated/results/STAR-Alignment/STAR"
outputdir="TOO-Raw-Simulated/results/STAR-Alignment"
genome="TOO-Raw-Simulated/gencode.v46.annotation.gtf"

for bamfile in "${inputdir}"/*.sortedByCoord.out.bam; do
    filename=$(basename "$bamfile")
    sample="${filename%%_Aligned.sortedByCoord.out.bam}"
    
    echo "Processing $sample..."

    # Step 1: Filter to keep only lines with 'chr' in the reference column
    samtools view -h "$bamfile" | \
    awk '{if ($1 ~ /^@/ || $3 ~ "chr"){print $0}}' | \
    samtools view -Sb - > "${outputdir}/${sample}.filtered.bam"

    # Step 2: Sort the filtered BAM (required for markdup)
    samtools sort -o "${outputdir}/${sample}.filtered.sorted.bam" -@ 4 "${outputdir}/${sample}.filtered.bam"

    # Step 3: Remove duplicates
    samtools markdup -r "${outputdir}/${sample}.filtered.sorted.bam" "${outputdir}/${sample}.nodup.bam"
done

module load anaconda
conda activate featurecounts

# Command to count all filtered bam files of the retrieved RNA-Later and FFPE data
featureCounts -g gene_name -t exon -a ${genome} -Q 10 -T 24 -F GTF -o ${outputdir}/20250616_All-Tissues-NoDup_Counts.txt ${outputdir}/*.nodup.bam

# Clean the output by removing columns 2 to 6, remove the comment line and adjusting the header to remove paths
cut --complement -f2-6 ${outputdir}/20250616_All-Tissues-NoDup_Counts.txt | sed '1d' | sed '1,2{
s|TOO-Raw-Simulated/results/STAR-Alignment/||g
s|\.nodup\.bam||g
}' > ${outputdir}/20250616_All-Tissues_Counts_temp.txt

# Renames the columns from the SRR number to match a Donor_Tissue pattern
awk -F"\t" '
FNR==NR { map[$3] = $1"_"$2; next }
{
  for (i=2; i<=NF; i++) {
    if ($i in map) $i = map[$i]
  }
  OFS="\t"; print
}
' 20250416_All-Tissues_mapping.txt "${outputdir}/20250616_All-Tissues_Counts_temp.txt" > "${outputdir}/20250616_All-Tissues-NoDup_Counts_Clean.txt"

rm -rf ${outputdir}/20250616_All-Tissues_Counts_temp.txt