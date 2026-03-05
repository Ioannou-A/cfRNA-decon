import os
import glob
import scanpy as sc
import pandas as pd
import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import argrelextrema

# Get the current working directory
cwd = os.getcwd()

# Define input and output directories
input_dir = os.path.join(cwd, "02_Individual-h5ad")
output_dir = os.path.join(cwd, "03_Individual-QC-h5ad")

# Create output directory if it doesn't exist
os.makedirs(output_dir, exist_ok=True)

# Find all H5 files in the specified input directory
h5ad_files = glob.glob(os.path.join(input_dir, "*.h5ad"))

# Define a threshold for count depth (e.g., 10000 as an example)
count_thresh = 300

for h5ad_file in h5ad_files:
    print(f"Processing {h5ad_file}...")

    # Load the data using Scanpy's function for 10X Genomics h5 files
    adata = sc.read_h5ad(h5ad_file)

    # Skip the sample if it has fewer than 250 cells
    if adata.n_obs < 250:
        print(f"Skipping {h5ad_file} because it has fewer than 250 cells.")
        continue

    # Annotate mitochondrial, ribosomal, and hemoglobin genes
    adata.var["mt"] = adata.var_names.str.startswith("MT-")  # Mitochondrial genes
    adata.var["ribo"] = adata.var_names.str.startswith(("RPS", "RPL"))  # Ribosomal genes
    adata.var["hb"] = adata.var_names.str.contains("^HB[^(P)]")  # Hemoglobin genes

    # Compute quality control metrics and log-transform counts
    sc.pp.calculate_qc_metrics(adata, qc_vars=["mt", "ribo", "hb"], inplace=True, log1p=True)

    # Filter out low-quality cells and genes
    sc.pp.filter_cells(adata, min_genes=100)  # Remove cells with fewer than 100 detected genes and less tha 200 counts
    sc.pp.filter_genes(adata, min_cells=3)  # Remove genes detected in fewer than 3 cells

    # Apply Scrublet to detect and annotate doublets in the dataset
    sc.pp.scrublet(adata)

    # Copy decontXcounts to X to override the normalization
    adata.X = adata.layers["decontXcounts"].copy()

    # Normalize total counts per cell to median total counts
    sc.pp.normalize_total(adata)

    # Log-transform the normalized data to stabilize variance
    sc.pp.log1p(adata)

    # Identify and annotate highly variable genes (HVGs)
    sc.pp.highly_variable_genes(adata, n_top_genes=2000)
    sc.pl.highly_variable_genes(adata)

    # Generate QC plots to visualize quality metrics
    g = sc.pl.violin(adata, ["n_genes_by_counts", "total_counts", "pct_counts_mt"],
                     jitter=0.4, multi_panel=True, show=False, color=sns.color_palette()[0], size=1.5)

    # Set titles for each subplot
    titles = ["No. Genes per Spot", "Total counts", "% Mitochondrial Gene Counts"]
    axs = g.axes.flatten()
    for i, title in enumerate(titles):
        axs[i].set_title(title)
        axs[i].set_ylabel("Value")

    # Set the overall plot title
    g.fig.suptitle(f"Violin QC Plots for {os.path.basename(h5ad_file)}", fontsize=22)
    g.fig.subplots_adjust(top=0.85, hspace=0.3)

    # Save or display the plot
    outfile = os.path.join(output_dir, os.path.basename(h5ad_file).replace(".h5ad", "_violin_qc_plot.png"))
    g.fig.savefig(outfile)
    print(f"Saved Violin QC Plot to {outfile}")
    plt.close(g.fig)

    # Create a scatter plot for mitochondrial gene counts
    plt.figure(figsize=(6,6))
    ax = sc.pl.scatter(adata, "total_counts", "n_genes_by_counts", color="pct_counts_mt", show=False)
    ax.set_title(f"% Mitochondrial Gene Counts in {os.path.basename(h5ad_file)}")
    ax.set_xlabel("Total Counts per Spot")
    ax.set_ylabel("No. Genes per Spot")

    # Save the scatter plot
    scatter_outfile = os.path.join(output_dir, os.path.basename(h5ad_file).replace(".h5ad", "_mitochondrial_percentage_plot.png"))
    plt.savefig(scatter_outfile)
    print(f"Saved Mitochondrial Percentage Plot to {scatter_outfile}")
    plt.close()

    # Plot the count depth histogram
    plt.figure(figsize=(6,6))
    sns.histplot(adata.to_df().sum(axis=1))  # Sum counts across genes for each cell
    plt.xlabel("Count Depth")
    plt.ylabel("Frequency")
    plt.title(f"Count Depth per Spot in {os.path.basename(h5ad_file)}")
    plt.axvline(count_thresh, color="red", ls="--", label=f"Threshold at {count_thresh}")
    plt.legend()

    # Save the count depth plot
    count_depth_outfile = os.path.join(output_dir, os.path.basename(h5ad_file).replace(".h5ad", "_count_depth_plot.png"))
    plt.savefig(count_depth_outfile)
    print(f"Saved Count Depth Plot to {count_depth_outfile}")
    plt.close()

    # Compute nearest-neighbor graph for downstream clustering and visualization
    sc.tl.pca(adata)
    sc.pl.pca_variance_ratio(adata, n_pcs=50, log=True)
    sc.pp.neighbors(adata)

    # Compute and visualize UMAP embeddings
    sc.tl.umap(adata)
    sc.tl.leiden(adata, flavor="igraph", n_iterations=2)

    # Extract filename without extension for the title
    file_title = os.path.basename(h5ad_file).replace(".h5ad", "")
    # Define output file path
    umap_outfile = os.path.join(output_dir, f"{file_title}_UMAP_plot.png")
    # Generate UMAP plot with title
    fig = sc.pl.umap(adata, color=["free_annotation"], title=None, return_fig=True)
    fig.suptitle(f"UMAP Plot of {file_title}")
    # Save and clean up
    fig.savefig(umap_outfile, bbox_inches="tight", dpi=300)
    plt.close(fig)
    print(f"Saved UMAP Plot to {umap_outfile}")

    # Create a bar plot for cell types
    celltype_counts = adata.obs["free_annotation"].value_counts().reset_index()
    celltype_counts.columns = ["celltype_major", "count"]
    celltype_counts = celltype_counts.sort_values(by="count", ascending=False)
    plt.figure(figsize=(9,6))
    sns.barplot(x="count", y="celltype_major", data=celltype_counts, hue="celltype_major", order=celltype_counts["celltype_major"])
    plt.title(f"Celltype Composition in {file_title}")
    plt.xlabel("Cell Counts")
    plt.ylabel("Cell Types")
    # Save the count depth plot
    count_depth_outfile = os.path.join(output_dir, os.path.basename(h5ad_file).replace(".h5ad", "_cell_type_plot.png"))
    plt.tight_layout()
    plt.savefig(count_depth_outfile)
    print(f"Saved Count Depth Plot to {count_depth_outfile}")
    plt.close()

    # Construct the output path with the specified output directory and suffix "_processed.h5ad"
    output_path = os.path.join(output_dir, os.path.basename(h5ad_file).replace(".h5ad", "_processed.h5ad"))

    # Save the processed AnnData object for future analysis
    adata.write(output_path)
    print(f"Saved processed data to {output_path}\n")


