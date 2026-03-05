import time
import glob
import os
from redeconv.__ReDeconv_P import *

print('********************************************************')
print('Running: 1 -- Find initial signature genes (t-test)')
print('         2 -- Compute mean and std of top signature genes')
print('         3 -- Do cell type deconvolution')
print('********************************************************')

stTime = time.mktime(time.gmtime())

# Fixed parameters
L_max_pv = 0.05
L_min_fold_change = 2.0
L_CellType_CellNo_LB = 2  # min number of cells per cell type
L_NoSep_sampleNo_UB = 15
L_topNo_list = [1500]

# Base directories
BASE_DIR = "COO-Decon-Noise"
MIXTURE_DIR = os.path.join(BASE_DIR, "Random_v2C-Noisy_Final3/")
OUTPUT_DIR = os.path.join(BASE_DIR, "ReDeconv-Deconvolution-Noisy_v3")

os.makedirs(OUTPUT_DIR, exist_ok=True)

# Reference files
meta_file = "COO-Matrix/TSP-HBA_Inner_100each_seed42-ReDeconv_" \
"" \
"ta.txt"
exp_file  = "COO-Matrix/TSP-HBA_Inner_100each_seed42-ReDeconv.txt"
prefix = os.path.basename(exp_file).replace("-ReDeconv.txt", "")

# Validate reference files
status_data = check_meta_and_scRNAseq_data(meta_file, exp_file)
if status_data <= 0:
    print(f"Meta and scRNA-seq data do not match for {prefix}. Exiting.")
    exit(1)

# Process all bulk RNA-seq mixture files
mixture_files = sorted(glob.glob(os.path.join(MIXTURE_DIR, "Random_v2C-Noisy_phi*_All-Counts.txt")))

if not mixture_files:
    print("No bulk RNA-seq files found. Exiting.")
    exit(1)

for bulk_RNAseq_file in mixture_files:
    mix_prefix = os.path.basename(bulk_RNAseq_file).replace(".txt", "")
    print(f"\nProcessing mixture: {mix_prefix}")

    for L_topNo in L_topNo_list:
        tag = f"{prefix}_{mix_prefix}_Top{L_topNo}"
        print(f"  Running with L_topNo = {L_topNo} and L_NoSep_sampleNo_UB = {L_NoSep_sampleNo_UB}")

        fn_ini_sig = os.path.join(OUTPUT_DIR, f"{tag}_Initial_sig_t_test_fd2.0_corr.tsv")
        fn_mean_std = os.path.join(OUTPUT_DIR, f"{tag}_Signature_mean_std_fd2.0.tsv")
        fn_heatmap = os.path.join(OUTPUT_DIR, f"{tag}_Heatmap_signature_gene_matrix.png")
        fn_extra_info = os.path.join(OUTPUT_DIR, f"{tag}_Signature_genes_extra_information.txt")
        fn_percentage_save = os.path.join(OUTPUT_DIR, f"{tag}_ReDeconv_results.tsv")

        get_initial_Signature_Candidates(
            meta_file, exp_file, fn_ini_sig,
            L_max_pv, L_min_fold_change, L_CellType_CellNo_LB, L_NoSep_sampleNo_UB
        )
        Get_signature_gene_matrix(
            exp_file, meta_file, fn_ini_sig,
            fn_mean_std, L_topNo, fn_heatmap, fn_extra_info
        )
        ReDeconv(fn_mean_std, bulk_RNAseq_file, fn_percentage_save)

endTime = time.mktime(time.gmtime())
print('\nTotal time =', ((endTime - stTime) / 60), 'minutes')
