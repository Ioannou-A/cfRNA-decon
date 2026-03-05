#!/bin/bash

mkdir TOO-Raw-Simulated/FFPE-Data-Raw
cd TOO-Raw-Simulated/FFPE-Data-Raw

## Load necessary module
module load igmm/apps/sratoolkit/3.0.0

## List of SRR accessions
## Representing FFPE-2, FFPE-3, FFPE-4 and FFPE-5 from Suntsova et al, 2019
SRR_LIST=("SRR7961209" "SRR7961215" "SRR7961197" "SRR7961219" "SRR7961229"\
	"SRR7961233" "SRR7961239" "SRR7961203" "SRR7961210" "SRR7961216"\
	"SRR7961198" "SRR7961220" "SRR7961230" "SRR7961234" "SRR7961214"\
	"SRR7961232" "SRR7961196" "SRR7961208" "SRR7961228" "SRR7961235"\
	"SRR7961199" "SRR7961211" "SRR7961221" "SRR7961227")

## Iterate over each accession in the list
for SRR_ACCESSION in "${SRR_LIST[@]}"
do
    # Prefetch SRA data
    prefetch $SRR_ACCESSION

    # Convert SRA to fastq
    fastq-dump $SRR_ACCESSION
done

gzip *.fastq
