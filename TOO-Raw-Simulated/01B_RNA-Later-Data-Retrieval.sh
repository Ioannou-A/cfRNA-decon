#!/bin/bash

mkdir TOO-Raw-Simulated/RNA-Later-Data-Raw
cd TOO-Raw-Simulated/RNA-Later-Data-Raw

## Load necessary module
module load igmm/apps/sratoolkit/3.0.0

## List of SRR accessions
## Representing Later-8, Later-16, Later-2 and Later-12 from Suntsova et al, 2019
SRR_LIST=("SRR7961288" "SRR7961284" "SRR7961290" "SRR7961286" "SRR7961280" \
          "SRR7961291" "SRR7961289" "SRR7961281" "SRR7961285" "SRR7961279" \
          "SRR7961278" "SRR7961283" "SRR7961282" "SRR7961287" "SRR7961309" \
          "SRR7961310" "SRR7961319" "SRR7961311" "SRR7961312" "SRR7961313" \
          "SRR7961314" "SRR7961315" "SRR7961316" "SRR7961318" "SRR7961317" \
          "SRR7961261" "SRR7961255" "SRR7961258" "SRR7961259" "SRR7961256" \
          "SRR7961254" "SRR7961257" "SRR7961301" "SRR7961295" "SRR7961297" \
          "SRR7961293" "SRR7961302" "SRR7961304" "SRR7961300" "SRR7961292" \
          "SRR7961294" "SRR7961296" "SRR7961299" "SRR7961303" "SRR7961305" \
          "SRR7961306" "SRR7961307" "SRR7961308")

## Iterate over each accession in the list
for SRR_ACCESSION in "${SRR_LIST[@]}"
do
    # Prefetch SRA data
    prefetch $SRR_ACCESSION

    # Convert SRA to fastq
    fastq-dump $SRR_ACCESSION
done

gzip *.fastq
cd TOO-Raw-Simulated
