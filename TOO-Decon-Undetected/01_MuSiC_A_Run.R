#!/usr/bin/env Rscript

args <- commandArgs(trailingOnly = TRUE)
reference_path <- args[1]
mixture_path <- args[2]
output_path <- args[3]

library(MuSiC)
library(SingleCellExperiment)
library(S4Vectors)

# Read cell type labels from header
raw_reference <- readLines(reference_path)
header <- unlist(strsplit(raw_reference[1], "\t"))
tissue_types <- header[-1]

# Read matrices
reference <- read.table(reference_path, sep = "\t", header = TRUE, row.names = 1, check.names = FALSE)
mixture <- read.table(mixture_path, sep = "\t", header = TRUE, row.names = 1)

# Trim mixture for quick test
mixture_less <- as.matrix(mixture)

# Format reference SingleCellExperiment
unique_tissue_ids <- paste0("Tissue", seq_len(ncol(reference)))
colnames(reference) <- unique_tissue_ids

# Create reference metadata
reference_meta <- data.frame(
  donor = seq_along(unique_tissue_ids)
)
rownames(reference_meta) <- unique_tissue_ids
# Add tissue_types
reference_meta$TissueTypes <- tissue_types

ref_sce <- SingleCellExperiment(
  assays = list(counts = as.matrix(reference)),
  colData = reference_meta
)

# Run MuSiC
music_result = music_prop(
  bulk.mtx = mixture_less,
  sc.sce = ref_sce,
  clusters = "TissueTypes",
  samples = "donor"
)

# Output results to the specified file path
write.table(
  music_result$Est.prop.weighted,
  file = output_path,
  sep = "\t",
  quote = FALSE,
  col.names = NA
)
