#!/usr/bin/env Rscript

# Load necessary libraries
suppressWarnings(library(BayesPrism))

# Read command line arguments
args <- commandArgs(trailingOnly = TRUE)
if(length(args) < 3) {
  stop("Usage: Rscript run_bayesprism.R <bulk_expr.txt> <sc_expr.txt> <output_file.txt>")
}
bulk_path <- args[1]
sc_path <- args[2]
output_file <- args[3]

# Load input data
bulk_gene_expression <- read.table(bulk_path, sep = "\t", header = TRUE, row.names = 1)
single_cell_object <- read.table(sc_path, sep = "\t", header = TRUE, row.names = 1)

# Transpose the matrices to ensure genes are columns
bulk_gene_expression <- t(bulk_gene_expression)
single_cell_object <- t(single_cell_object)

# Process row names: Remove substring after the last period
row_names_vector <- rownames(single_cell_object)
processed_vector <- gsub("[0-9]+$", "", row_names_vector)

# Create a new BayesPrism object
myPrism <- BayesPrism::new.prism(
  reference = single_cell_object,
  mixture = bulk_gene_expression,
  input.type = "count.matrix",
  cell.type.labels = processed_vector,
  cell.state.labels = NULL,
  key = NULL
)

# Run the BayesPrism analysis
bp.res <- BayesPrism::run.prism(
  prism = myPrism,
  n.cores = 12
)

# Extract the theta matrix
theta <- get.fraction(bp = bp.res, which.theta = "final", state.or.type = "type")

# Save result
write.table(theta, file = output_file, sep = "\t", quote = FALSE, col.names = NA)
