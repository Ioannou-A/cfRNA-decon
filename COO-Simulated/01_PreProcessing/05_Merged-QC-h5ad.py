import os
import glob
import scanpy as sc
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Define the input and output directories
cwd = os.getcwd()
input_dir = os.path.join(cwd, "04_Merged-PerDonor-h5ad")
output_dir = os.path.join(cwd, "05_Merged-PerDonor-QC-h5ad")

# Create the output directory if it doesn't exist
os.makedirs(output_dir, exist_ok=True)

# Get all H5 files from the input directory
h5ad_files = glob.glob(os.path.join(input_dir, "*.h5ad"))

# Define a count depth threshold
count_thresh = 300

# Iterate over each H5 file
for h5ad_file in h5ad_files:
    print(f"Processing {h5ad_file}...")

    # Load the AnnData object
    adata = sc.read_h5ad(h5ad_file)

    # Annotate genes: mitochondrial, ribosomal, and hemoglobin
    adata.var["mt"] = adata.var_names.str.startswith("MT-")
    adata.var["ribo"] = adata.var_names.str.startswith(("RPS", "RPL"))
    adata.var["hb"] = adata.var_names.str.contains("^HB[^(P)]")

    # Override normalization with decontXcounts
    adata.X = adata.layers["decontXcounts"].copy()

    # Normalize and log-transform the data
    sc.pp.normalize_total(adata)
    sc.pp.log1p(adata)

    # Identify highly variable genes (HVGs)
    sc.pp.highly_variable_genes(adata, n_top_genes=2000)
    sc.pl.highly_variable_genes(adata)

    # Plot the count depth histogram
    plt.figure(figsize=(6, 6))
    sns.histplot(adata.to_df().sum(axis=1))  # Sum counts per cell
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

    # Compute nearest-neighbor graph, PCA, and UMAP embeddings
    sc.tl.pca(adata)
    sc.pl.pca_variance_ratio(adata, n_pcs=50, log=True)
    sc.pp.neighbors(adata)
    sc.tl.umap(adata)
    sc.tl.leiden(adata, flavor="igraph", n_iterations=2)

    # Generate and save the UMAP plot for tissues
    file_title = os.path.basename(h5ad_file).replace(".h5ad", "")
    umap_outfile = os.path.join(output_dir, f"{file_title}_tissue_UMAP_plot.png")
    fig = sc.pl.umap(adata, color=["tissue"], title=None, return_fig=True)
    fig.suptitle(f"UMAP Plot of {file_title}")
    fig.savefig(umap_outfile, bbox_inches="tight", dpi=300)
    plt.close(fig)
    print(f"Saved UMAP Plot to {umap_outfile}")

    # Generate and save the UMAP plot for cell types
    umap_outfile = os.path.join(output_dir, f"{file_title}_celltype_UMAP_plot.png")
    # Generate UMAP plot with title
    fig = sc.pl.umap(adata, color=["cell_ontology_class"], palette="tab20", title=None, return_fig=True)
    fig.suptitle(f"UMAP Plot of {file_title}")
    # Save and clean up
    fig.savefig(umap_outfile, bbox_inches="tight", dpi=300)
    plt.close(fig)
    print(f"Saved UMAP Plot to {umap_outfile}")

    # Plot the tissue type composition bar chart
    tissue_counts = adata.obs["tissue"].value_counts().reset_index()
    tissue_counts.columns = ["tissue_major", "count"]
    tissue_counts = tissue_counts.sort_values(by="count", ascending=False)
    plt.figure(figsize=(9, 6))
    sns.barplot(x="count", y="tissue_major", data=tissue_counts, hue="tissue_major", order=tissue_counts["tissue_major"])
    plt.title(f"Tissue Composition in {file_title}")
    plt.xlabel("Cell Counts")
    plt.ylabel("Tissue Types")

    # Save the tissue type plot
    tissue_type_outfile = os.path.join(output_dir, os.path.basename(h5ad_file).replace(".h5ad", "_tissue_type_plot.png"))
    plt.tight_layout()
    plt.savefig(tissue_type_outfile)
    print(f"Saved Tissue Type Plot to {tissue_type_outfile}")
    plt.close()

    celltype_counts = adata.obs["cell_ontology_class"].value_counts().reset_index()
    celltype_counts.columns = ["celltype_major", "count"]
    celltype_counts = celltype_counts.sort_values(by="count", ascending=False)
    plt.figure(figsize=(11,6))

    # Plot the cell type composition bar chart
    # Select the top 20 most populated cell types
    top_30_celltypes = celltype_counts.head(30)

    sns.barplot(x="count", y="celltype_major", data=top_30_celltypes, order=top_30_celltypes["celltype_major"], palette='viridis')
    plt.title(f"Celltype Composition in {file_title}")
    plt.xlabel("Cell Counts")
    plt.ylabel("Cell Types")
    # Save the count depth plot
    count_depth_outfile = os.path.join(output_dir, os.path.basename(h5ad_file).replace(".h5ad", "_cell_type_plot.png"))
    plt.tight_layout()
    plt.savefig(count_depth_outfile)
    print(f"Saved Count Depth Plot to {count_depth_outfile}")
    plt.close()

    # Save the processed AnnData object
    output_path = os.path.join(output_dir, os.path.basename(h5ad_file).replace(".h5ad", "_processed.h5ad"))
    adata.write(output_path)
    print(f"Saved processed data to {output_path}\n")

