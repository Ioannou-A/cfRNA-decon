#!/usr/bin/bash

## Script explaining the retrieval and indexing of the human genome
cd TOO-Raw-Simulated

## Download the human genome fasta file and GTF file
wget ftp://ftp.ebi.ac.uk/pub/databases/gencode/Gencode_human/release_46/GRCh38.primary_assembly.genome.fa.gz
## Need to unzip the file as the STAR pipeline works withthe unzipped file only
wget ftp://ftp.ebi.ac.uk/pub/databases/gencode/Gencode_human/release_46/gencode.v46.annotation.gtf.gz
gunzip GRCh38.primary_assembly.genome.fa.gz
gunzip gencode.v46.annotation.gtf.gz

## Creation of the STAR Index using combined reference genome for alignment
module load igmm/apps/STAR/2.7.8a

mkdir GRCh38-STAR-Index
STAR --runThreadN 10 --runMode genomeGenerate --sjdbOverhang 49 --genomeDir TOO-Raw-Simulated/GRCh38-STAR-Index \
 --genomeFastaFiles TOO-Raw-Simulated/GRCh38.primary_assembly.genome.fa \
 --sjdbGTFfile TOO-Raw-Simulated/gencode.v46.annotation.gtf




