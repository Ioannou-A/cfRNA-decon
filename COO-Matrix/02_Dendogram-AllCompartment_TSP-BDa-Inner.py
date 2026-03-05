import numpy as np
import scanpy as sc
import pandas as pd
import os
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.cluster.hierarchy import dendrogram, linkage, cut_tree

# Set paths
datPath = "COO-Matrix/DarmanisData/"
adataName = "TSP-BDa-merged-Inner.h5ad"
output_prefix = "TSP-BDa_Inner"
cellAnnotCol = "cell_ontology_class"
comp = 'All-Compartments'

# adjust for tabula sapiens since the adata object is large to rip accordingly
def backtrackLabels_TSP(leafDF, ivlDF):
    leaves = leafDF.index.tolist()
    ogLabels = ["" for i in range(len(leaves))]
    ivlLabels = ivlDF.index.tolist() # the output

    ivlIndex = 0
    for leaf in leaves:
        ogLabels[leaf] = ivlLabels[ivlIndex]
        ivlIndex += 1 # increment to move to the next element
    return(ogLabels)

# Load data
adata = sc.read_h5ad(os.path.join(datPath, adataName))
os.system("echo Loaded adata")

# Preprocess
sc.pp.normalize_total(adata, target_sum=1e6)
sc.pp.log1p(adata)
os.system("echo Normalized and logged")

# Filter data
adata = adata[adata.obs["tissue"] != "Eye"]
# Rename the endothelial annotation of Darmanis Brain to endothelial cell to be incorporate with those of the TSP
adata.obs["cell_ontology_class"] = adata.obs["cell_ontology_class"].replace("endothelial", "endothelial cell")
tspCellTypes = list(np.unique(adata.obs["cell_ontology_class"]))

# Define annotations to exclude
dropMuscle = [i for i in tspCellTypes if "muscle" in i and i not in [
    "atrial cardiac muscle cell", "ventricular cardiac muscle cell", "cell of skeletal muscle",
    "smooth muscle cell", "fast muscle cell", "slow muscle cell"]]
dropFibro = [i for i in tspCellTypes if "fibro" in i and i != "fibroblast"]
# exclude granulocyte because we have basophil/neutrophil
# exclude t follicular helper cell since it's a t cell subtype
# exclude myeloid cell since it's only in pancreas/prostate annotations
# exclude 'mesenchymal stem cell' since this isn't in the immune compartment
badAnnot = ["leucocyte", "immune cell", "granulocyte", "erythroid lineage cell", 'hematopoietic precursor cell', 'myeloid leukocyte',
           't follicular helper cell', 'colon macrophage', "myeloid cell", 'plasmacytoid dendritic cell']

annotExclude = ["epithelial cell", "ocular surface cell", "radial glial cell",
                "lacrimal gland functional unit cell", "connective tissue cell",
                "corneal keratocyte", "ciliary body"] + dropMuscle + dropFibro + badAnnot
goodAnnot = np.setdiff1d(adata.obs["cell_ontology_class"], annotExclude)
adata = adata[adata.obs["cell_ontology_class"].isin(goodAnnot)]

# Compute PCA once on full dataset
sc.pp.pca(adata)
os.system("echo PCA computed for full dataset")

# Process all compartments together

output_comp_prefix = f"{output_prefix}_{comp}"

# Compute dendrogram
zKey = f"dendrogram_{comp}"
sc.tl.dendrogram(adata, n_pcs=50, linkage_method="complete", key_added=zKey, optimal_ordering=False, groupby=cellAnnotCol)
plt.rcParams['figure.figsize'] = [30,10]

# Save linkage matrix
Z = adata.uns[zKey]["linkage"]
pd.DataFrame(Z).to_csv(f"{output_comp_prefix}_linkage.csv")
    
ivlList =  adata.uns[zKey]["dendrogram_info"]['ivl']
ivlDF = pd.DataFrame(index = ivlList)
ivlDF.to_csv(f"{output_comp_prefix}_ivl.csv")

# save the heights of the nodes
dcoordMat = adata.uns[zKey]["dendrogram_info"]["dcoord"]
dcoordDF = pd.DataFrame(data = dcoordMat)
dcoordDF.to_csv(f"{output_comp_prefix}_dcoord.csv")

leafList = adata.uns[zKey]["dendrogram_info"]['leaves']
leafDF = pd.DataFrame(index = leafList)
leafDF.to_csv(f"{output_comp_prefix}_leafDF.csv")

sc.pl.dendrogram(adata, dendrogram_key = zKey, groupby = cellAnnotCol, save = f"{output_comp_prefix}_sc_Dend.png")

IVL = pd.read_csv(f"{output_prefix}_{comp}_ivl.csv", index_col = 0)
IVLabels = IVL.index.tolist()
Linkage = pd.read_csv(f"{output_prefix}_{comp}_linkage.csv", index_col = 0)
Dcoord = pd.read_csv(f"{output_prefix}_{comp}_dcoord.csv", index_col = 0)
leafDF = pd.read_csv(f"{output_prefix}_{comp}_leafDF.csv", index_col = 0)
    
heights = Dcoord.iloc[:,1]
    
# Save dendrogram plot
plt.figure(figsize=(30, 10))
Z = Linkage.values

LabelList = backtrackLabels_TSP(leafDF, IVL)

dn = dendrogram(Z, labels=LabelList, leaf_font_size=14)
plt.xticks(rotation=90)
plt.savefig(f"{output_comp_prefix}_dendrogram.pdf", dpi=300, bbox_inches='tight', transparent=True)
    
# Compute cut height (7.5% of max height)
cutHeight = np.max(heights) * 0.075
plt.axhline(y=cutHeight, c='grey', lw=1, linestyle='dashed')
plt.savefig(f"{output_comp_prefix}_dendrogram_cut.pdf", dpi=300, bbox_inches='tight', transparent=True)
    
# Perform clustering
cut_clusters = cut_tree(Z, height=cutHeight)
cutDF = pd.DataFrame(data=cut_clusters, index = LabelList)
cutDF.columns = ["cluster"]
    
# Merge labels based on cluster assignments
allRows = []
clusters = np.unique(cutDF["cluster"])
for clus in clusters:
    thisClus = cutDF[cutDF["cluster"] == clus]
    joined = "/".join(list(thisClus.index))
    allRows.append(joined)
    
# Save merged cluster labels
mergedLabels = pd.DataFrame(index=allRows, data=clusters, columns=["cluster"])
mergedLabels.to_csv(f"{output_comp_prefix}_clusters.csv")

print("Processing complete. Outputs saved as CSV and PDF for each compartment.")