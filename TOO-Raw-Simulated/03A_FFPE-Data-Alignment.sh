#!/bin/bash

mkdir -p TOO-Raw-Simulated/results/STAR-Alignment
inputdir="TOO-Raw-Simulated/FFPE-Data-Raw"
outputdir="TOO-Raw-Simulated/results/STAR-Alignment"
genomeDir="TOO-Raw-Simulated/GRCh38-STAR-Index"

## Load necessary module
module load igmm/apps/STAR/2.7.8a
module load igmm/apps/samtools/1.16.1

## Alignment of the files using STAR
## List of SRR accessions
## Representing FFPE-2, FFPE-3, FFPE-4 and FFPE-5 from Suntsova et al, 2019
SRR_LIST=("SRR7961209" "SRR7961215" "SRR7961197" "SRR7961219" "SRR7961229"\
        "SRR7961233" "SRR7961239" "SRR7961203" "SRR7961210" "SRR7961216"\
        "SRR7961198" "SRR7961220" "SRR7961230" "SRR7961234" "SRR7961214"\
        "SRR7961232" "SRR7961196" "SRR7961208" "SRR7961228" "SRR7961235"\
        "SRR7961199" "SRR7961211" "SRR7961221" "SRR7961227")

for SRR in "${SRR_LIST[@]}"; do
  STAR --runMode alignReads --runThreadN 4 --readFilesCommand zcat --outFilterMultimapNmax 1 \
       --genomeDir ${genomeDir} --genomeLoad NoSharedMemory --limitBAMsortRAM 3200000000 \
       --outSAMtype BAM SortedByCoordinate --outFileNamePrefix ${outputdir}/STAR/${SRR}_ \
       --readFilesIn ${inputdir}/${SRR}.fastq.gz
done
