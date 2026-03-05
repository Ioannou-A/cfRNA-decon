#!/usr/bin/env Rscript

args <- commandArgs(trailingOnly = TRUE)
reference_path <- args[1]
reference_path_meta <- args[2]
mixture_path <- args[3]
output_path <- args[4]

library(MuSiC)
library(SingleCellExperiment)
library(S4Vectors)

# Read cell type labels from header
raw_reference <- readLines(reference_path)
header <- unlist(strsplit(raw_reference[1], "\t"))
cell_types <- header[-1]

# Read matrices
reference <- read.table(reference_path, sep = "\t", header = TRUE, row.names = 1, check.names = FALSE)
mixture <- read.table(mixture_path, sep = "\t", header = TRUE, row.names = 1)
reference_meta <- read.table(reference_path_meta, sep = "\t", header = TRUE)

## Trim mixture for quick test
mixture_less <- as.matrix(mixture)

# Add cell_types
reference_meta$CellTypes <- cell_types

# Format reference SingleCellExperiment
unique_cell_ids <- paste0("Cell", seq_len(ncol(reference)))
colnames(reference) <- unique_cell_ids
rownames(reference_meta) <- unique_cell_ids

ref_sce <- SingleCellExperiment(
  assays = list(counts = as.matrix(reference)),
  colData = reference_meta
)

# Run MuSiC
music_result <- music_prop(
  bulk.mtx = as.matrix(mixture),
  sc.sce = ref_sce,
  clusters = "cell_group",   # matches column in meta file
  samples = "sample" # matches column in meta file
)
# none is 50427348 and gives 70
# none 50437961 and gives 70

# Output results to the specified file path
write.table(
  music_result$Est.prop.weighted,
  file = output_path,
  sep = "\t",
  quote = FALSE,
  col.names = NA
)