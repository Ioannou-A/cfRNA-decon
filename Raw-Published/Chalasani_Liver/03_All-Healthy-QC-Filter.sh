#!/bin/bash

module load igmm/apps/samtools/1.20
module load anaconda
conda activate featurecounts

inputdir="Raw-Published/Chalasani_Liver/All-Healthy-Aligned"
gtfdir="Raw-Published/"
outputdir="Raw-Published/Chalasani_Liver/All-Healthy-QC"

mkdir -p "$outputdir"

riboqc="${outputdir}/RibosomalQC.txt"
intronicqc="${outputdir}/IntronExonQC.txt"
failed_samples="${outputdir}/FailedSamples.txt"

# Header for QC reports
echo -e "Sample\tRiboFraction" > "$riboqc"
echo -e "Sample\tIntronCount\tExonCount\tIntron/Exon_Ratio" > "$intronicqc"
echo -e "Sample\tReason" > "$failed_samples"

# Ribosomal QC 
for FILE in "${inputdir}"/*.nodup.bam; do
     BASENAME=$(basename "$FILE" .nodup.bam)
     echo "Processing $BASENAME..."

     if [ ! -f "${FILE}.bai" ]; then
         samtools index "$FILE"
     fi

     RIBO_READS=$(samtools view -c "$FILE" "GL000220.1:105424-118780")
     TOTAL_READS=$(samtools view -c "$FILE")

     if [ "$TOTAL_READS" -gt 0 ]; then
         RIBO_FRACTION=$(echo "$RIBO_READS / $TOTAL_READS" | bc -l)
     else
         RIBO_FRACTION="NA"
     fi
     echo -e "${BASENAME}\t${RIBO_FRACTION}" >> "$riboqc"

     if [[ "$RIBO_FRACTION" != "NA" ]] && (( $(echo "$RIBO_FRACTION > 0.2" | bc -l) )); then
         echo -e "${BASENAME}\tribosomal_fraction>${RIBO_FRACTION}" >> "$failed_samples"
     fi
done

# Run featureCounts for introns and exons
featureCounts -p -T 4 -t intron -a "${gtfdir}/gencode.v45.annotation.introns-unique.gtf" \
    -Q 10 -F GTF -o "${outputdir}/IntronCounts.txt" "${inputdir}"/*nodup.bam

featureCounts -p -T 4 -t exon -a "${gtfdir}/gencode.v45.ERCC-Exon.gtf" \
    -Q 10 -F GTF -o "${outputdir}/ExonCounts.txt" "${inputdir}"/*nodup.bam

# Summarize intron and exon counts per sample
awk '
NR==2 {
    for (i=7; i<=NF; i++) samples[i] = $i
}
NR>2 {
    for (i=7; i<=NF; i++) sums[i] += $i
}
END {
    for (i=7; i<=NF; i++) print samples[i], sums[i]
}' "${outputdir}/IntronCounts.txt" > "${outputdir}/IntronSum.txt"

awk '
NR==2 {
    for (i=7; i<=NF; i++) samples[i] = $i
}
NR>2 {
    for (i=7; i<=NF; i++) sums[i] += $i
}
END {
    for (i=7; i<=NF; i++) print samples[i], sums[i]
}' "${outputdir}/ExonCounts.txt" > "${outputdir}/ExonSum.txt"

# Join sums and calculate ratio
join <(sort "${outputdir}/IntronSum.txt") <(sort "${outputdir}/ExonSum.txt") | \
awk -v intronicqc="$intronicqc" -v failed_samples="$failed_samples" '
{
    sample = $1
    intron = $2
    exon = $3
    if (exon > 0) {
        ratio = intron / exon
    } else {
        ratio = "NA"
    }
    print sample "\t" intron "\t" exon "\t" ratio >> intronicqc
    if (ratio != "NA" && ratio > 3) {
        print sample "\tintron_exon_ratio>" ratio >> failed_samples
    }
}'

# Cleanup
rm "${outputdir}/IntronSum.txt" "${outputdir}/ExonSum.txt"

