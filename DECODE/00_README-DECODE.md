# DECODE analysis

This directory contains the DECODE workflows used for the tissue-of-origin
(TOO) and cell-of-origin (COO) analyses reported in the manuscript.

## Workflow overview

| Step | Scripts | Description |
|---|---|---|
| 01 | `01_*.ipynb` | Prepare the GTEx and TSP reference datasets |
| 02 | `02A_*.sh`, `02B_*.py` | Generate GTEx TOO pseudo-bulk mixtures |
| 03 | `03A_*.py`, `03A_*.ipynb`, `03B_*.sh` | Generate and merge COO pseudo-bulk mixtures |
| 04 | `04_*.py`, `04_*.sh` | Train DECODE models across the selected training-size and DANN-patience settings |
| 05 | `05_apply_model_*.py`, `05_*_infer_GPU.sh` | Apply trained models to simulated tissue and cell type test data |
| 06 | `06_apply_model_Loy_*.py`, `06_*_infer_Loy_GPU.sh` | Apply trained models to the Loy inflammatory-syndrome cohort (Loy et al., 2024) |
| 07 | `07_Training-Plots.ipynb` | Plot training-size and DANN-patience results |

## Notes

- DECODE simulation metrics were calculated using the same procedures and notebooks as the other deconvolution methods in `TOO-Decon-Published/` and `COO-Decon-Pseudobulks/`. The archived notebooks were updated to recognise DECODE prediction files as additional inputs. The resulting DECODE values were incorporated into the final comparative heatmaps during figure assembly.
- Scripts for analysing and plotting DECODE outputs from the clinical-cohort analyses are provided in the corresponding `Loy_Inflammatory-Syndromes/` directories.
- Final trained model checkpoints used for inference are provided in `save_models/`.