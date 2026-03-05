import time
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

bulk_RNAseq_file = 'COO-Decon-Published/Moufarrej_Pre-Eclampsia/GSE192902_Pre-eclampsia_preQC_filtered_counts_UniquePatient_SpecificSample.txt'
output_folder = 'COO-Decon-Published/Moufarrej_Pre-Eclampsia/TSP-BDa_Outer_300_1500_10-Moufarrej_Pre-eclampsia/'

fn_meta = 'COO-Matrix/TSP-HBA_Inner_100each_seed42-ReDeconv_metadata.txt'
fn_exp  = 'COO-Matrix/TSP-HBA_Inner_100each_seed42-ReDeconv.txt'

# Derive prefix from metadata filename
prefix = os.path.basename(fn_meta).replace('_metadata.txt', '')

print(f'\nProcessing pair: {prefix}')

status_data = check_meta_and_scRNAseq_data(fn_meta, fn_exp)
if status_data <= 0:
    print(f'Meta and scRNA-seq data do not match for {prefix}. Exiting.')
    exit(1)

for L_topNo in L_topNo_list:
    tag = f'{prefix}_Top{L_topNo}'
    print(f'  Running with L_topNo = {L_topNo} and L_NoSep_sampleNo_UB = {L_NoSep_sampleNo_UB}')

    fn_ini_sig = f'{output_folder}{tag}_Initial_sig_t_test_fd2.0_corr.tsv'
    fn_mean_std = f'{output_folder}{tag}_Signature_mean_std_fd2.0.tsv'
    fn_heatmap = f'{output_folder}{tag}_Heatmap_signature_gene_matrix.png'
    fn_extra_info = f'{output_folder}{tag}_Signature_genes_extra_information.txt'
    fn_percentage_save = f'{output_folder}{tag}_ReDeconv_results.tsv'

    get_initial_Signature_Candidates(fn_meta, fn_exp, fn_ini_sig,
                                     L_max_pv, L_min_fold_change,
                                     L_CellType_CellNo_LB, L_NoSep_sampleNo_UB)
    Get_signature_gene_matrix(fn_exp, fn_meta, fn_ini_sig, fn_mean_std,
                              L_topNo, fn_heatmap, fn_extra_info)
    ReDeconv(fn_mean_std, bulk_RNAseq_file, fn_percentage_save)

endTime = time.mktime(time.gmtime())
print('\nTotal time =', ((endTime - stTime) / 60), 'minutes')
