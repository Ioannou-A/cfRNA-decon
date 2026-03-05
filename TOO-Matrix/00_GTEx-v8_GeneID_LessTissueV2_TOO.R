#setwd("TOO-Matrix/")

##Load the data of all gene counts per tissue as obtained from GTEx v8 in the ".gct" format.
Adipose_viscelar <- read.delim(file="GTEx_GeneCounts-per-tissue/gene_reads_2017-06-05_v8_adipose_visceral_omentum.gct", skip=2)
Adipose_subcutaneous <- read.delim(file="GTEx_GeneCounts-per-tissue/gene_reads_2017-06-05_v8_adipose_subcutaneous.gct", skip=2)
Adrenal_gland <- read.delim(file="GTEx_GeneCounts-per-tissue/gene_reads_2017-06-05_v8_adrenal_gland.gct", skip=2)
Artery_aorta <- read.delim(file="GTEx_GeneCounts-per-tissue/gene_reads_2017-06-05_v8_artery_aorta.gct", skip=2)
Artery_coronary <- read.delim(file="GTEx_GeneCounts-per-tissue/gene_reads_2017-06-05_v8_artery_coronary.gct", skip=2)
Artery_tibial <- read.delim(file="GTEx_GeneCounts-per-tissue/gene_reads_2017-06-05_v8_artery_tibial.gct", skip=2)
Bladder <- read.delim(file="GTEx_GeneCounts-per-tissue/gene_reads_2017-06-05_v8_bladder.gct", skip=2)
BrainAmygdala <- read.delim(file="GTEx_GeneCounts-per-tissue/gene_reads_2017-06-05_v8_brain_amygdala.gct", skip=2)
BrainACC <- read.delim(file="GTEx_GeneCounts-per-tissue/gene_reads_2017-06-05_v8_brain_anterior_cingulate_cortex_ba24.gct", skip=2)
BrainCaudate <- read.delim(file="GTEx_GeneCounts-per-tissue/gene_reads_2017-06-05_v8_brain_caudate_basal_ganglia.gct", skip=2)
BrainCerebellarHemi <- read.delim(file="GTEx_GeneCounts-per-tissue/gene_reads_2017-06-05_v8_brain_cerebellar_hemisphere.gct", skip=2)
BrainCerebellum <- read.delim(file="GTEx_GeneCounts-per-tissue/gene_reads_2017-06-05_v8_brain_cerebellum.gct", skip=2)
BrainCortex <- read.delim(file="GTEx_GeneCounts-per-tissue/gene_reads_2017-06-05_v8_brain_cortex.gct", skip=2)
BrainFrontalCortex <- read.delim(file="GTEx_GeneCounts-per-tissue/gene_reads_2017-06-05_v8_brain_frontal_cortex_ba9.gct", skip=2)
BrainHippocampus <- read.delim(file="GTEx_GeneCounts-per-tissue/gene_reads_2017-06-05_v8_brain_hippocampus.gct", skip=2)
BrainHypothalamus <- read.delim(file="GTEx_GeneCounts-per-tissue/gene_reads_2017-06-05_v8_brain_hypothalamus.gct", skip=2) 
BrainNucleusAccumbens <- read.delim(file="GTEx_GeneCounts-per-tissue/gene_reads_2017-06-05_v8_brain_nucleus_accumbens_basal_ganglia.gct", skip=2)
BrainPutamen <- read.delim(file="GTEx_GeneCounts-per-tissue/gene_reads_2017-06-05_v8_brain_putamen_basal_ganglia.gct", skip=2)
BrainSpinalCord <- read.delim(file="GTEx_GeneCounts-per-tissue/gene_reads_2017-06-05_v8_brain_spinal_cord_cervical_c-1.gct", skip=2)
BrainSubstantiaNigra <- read.delim(file="GTEx_GeneCounts-per-tissue/gene_reads_2017-06-05_v8_brain_substantia_nigra.gct", skip=2)
Breast <- read.delim(file="GTEx_GeneCounts-per-tissue/gene_reads_2017-06-05_v8_breast_mammary_tissue.gct", skip=2)
Fibroblasts <- read.delim(file="GTEx_GeneCounts-per-tissue/gene_reads_2017-06-05_v8_cells_cultured_fibroblasts.gct", skip=2)
Lymphocytes <- read.delim(file="GTEx_GeneCounts-per-tissue/gene_reads_2017-06-05_v8_cells_ebv-transformed_lymphocytes.gct", skip=2)
CervixEcto <- read.delim(file="GTEx_GeneCounts-per-tissue/gene_reads_2017-06-05_v8_cervix_ectocervix.gct", skip=2)
CervixEndo <- read.delim(file="GTEx_GeneCounts-per-tissue/gene_reads_2017-06-05_v8_cervix_endocervix.gct", skip=2)
ColonSigmoid <- read.delim(file="GTEx_GeneCounts-per-tissue/gene_reads_2017-06-05_v8_colon_sigmoid.gct", skip=2)
ColonTransverse <- read.delim(file="GTEx_GeneCounts-per-tissue/gene_reads_2017-06-05_v8_colon_transverse.gct", skip=2)
EsophagusGJ <- read.delim(file="GTEx_GeneCounts-per-tissue/gene_reads_2017-06-05_v8_esophagus_gastroesophageal_junction.gct", skip=2)
EsophagusMucosa <- read.delim(file="GTEx_GeneCounts-per-tissue/gene_reads_2017-06-05_v8_esophagus_mucosa.gct", skip=2)
EsophagusMuscularis <- read.delim(file="GTEx_GeneCounts-per-tissue/gene_reads_2017-06-05_v8_esophagus_muscularis.gct", skip=2)
FallopianTubes <- read.delim(file="GTEx_GeneCounts-per-tissue/gene_reads_2017-06-05_v8_fallopian_tube.gct", skip=2)
HeartAA <- read.delim(file="GTEx_GeneCounts-per-tissue/gene_reads_2017-06-05_v8_heart_atrial_appendage.gct", skip=2)
HeartLV <- read.delim(file="GTEx_GeneCounts-per-tissue/gene_reads_2017-06-05_v8_heart_left_ventricle.gct", skip=2)
Kidney_cortex <- read.delim(file="GTEx_GeneCounts-per-tissue/gene_reads_2017-06-05_v8_kidney_cortex.gct", skip=2)
Kidney_medulla <- read.delim(file="GTEx_GeneCounts-per-tissue/gene_reads_2017-06-05_v8_kidney_medulla.gct", skip=2)
Liver <- read.delim(file="GTEx_GeneCounts-per-tissue/gene_reads_2017-06-05_v8_liver.gct", skip=2)
Lung <- read.delim(file="GTEx_GeneCounts-per-tissue/gene_reads_2017-06-05_v8_lung.gct", skip=2)
SalivaryGland <- read.delim(file="GTEx_GeneCounts-per-tissue/gene_reads_2017-06-05_v8_minor_salivary_gland.gct", skip=2)
MuscleSkeletal <- read.delim(file="GTEx_GeneCounts-per-tissue/gene_reads_2017-06-05_v8_muscle_skeletal.gct", skip=2)
NerveTibial <- read.delim(file="GTEx_GeneCounts-per-tissue/gene_reads_2017-06-05_v8_nerve_tibial.gct", skip=2)
Ovary <- read.delim(file="GTEx_GeneCounts-per-tissue/gene_reads_2017-06-05_v8_ovary.gct", skip=2)
Pancreas <- read.delim(file="GTEx_GeneCounts-per-tissue/gene_reads_2017-06-05_v8_pancreas.gct", skip=2)
Pituitary <- read.delim(file="GTEx_GeneCounts-per-tissue/gene_reads_2017-06-05_v8_pituitary.gct", skip=2)
Prostate <- read.delim(file="GTEx_GeneCounts-per-tissue/gene_reads_2017-06-05_v8_prostate.gct", skip=2)
Skin_NoSun <- read.delim(file="GTEx_GeneCounts-per-tissue/gene_reads_2017-06-05_v8_skin_not_sun_exposed_suprapubic.gct", skip=2)
Skin_Sun <- read.delim(file="GTEx_GeneCounts-per-tissue/gene_reads_2017-06-05_v8_skin_sun_exposed_lower_leg.gct", skip=2)
SmallIntestine <- read.delim(file="GTEx_GeneCounts-per-tissue/gene_reads_2017-06-05_v8_small_intestine_terminal_ileum.gct", skip=2)
Spleen <- read.delim(file="GTEx_GeneCounts-per-tissue/gene_reads_2017-06-05_v8_spleen.gct", skip=2)
Stomach <- read.delim(file="GTEx_GeneCounts-per-tissue/gene_reads_2017-06-05_v8_stomach.gct", skip=2)
Testis <- read.delim(file="GTEx_GeneCounts-per-tissue/gene_reads_2017-06-05_v8_testis.gct", skip=2)
Thyroid <- read.delim(file="GTEx_GeneCounts-per-tissue/gene_reads_2017-06-05_v8_thyroid.gct", skip=2)
Uterus <-read.delim(file="GTEx_GeneCounts-per-tissue/gene_reads_2017-06-05_v8_uterus.gct", skip=2)
Vagina <- read.delim(file="GTEx_GeneCounts-per-tissue/gene_reads_2017-06-05_v8_vagina.gct", skip=2)
Whole_blood <- read.delim(file="GTEx_GeneCounts-per-tissue/gene_reads_2017-06-05_v8_whole_blood.gct", skip=2)

##Merge tissues together before performing the calculations. These tissues were also removed from all the lists shown bellow.
# Adipose_subcutaneous and Adipose_viscelar to Adipose
Adipose_viscelar <- Adipose_viscelar[ ,4:ncol(Adipose_viscelar)]
Adipose <- cbind(Adipose_subcutaneous, Adipose_viscelar)
rm(Adipose_subcutaneous, Adipose_viscelar)
# Kidney_cortex and Kidney_medulla into Kidney
Kidney_medulla <- Kidney_medulla[,4:ncol(Kidney_medulla)]
Kidney <- cbind(Kidney_cortex, Kidney_medulla)
rm(Kidney_cortex, Kidney_medulla)
# Skin_NoSun and Skin_Sun to Skin
Skin_Sun <- Skin_Sun[,4:ncol(Skin_Sun)]
Skin <- cbind(Skin_NoSun, Skin_Sun)
rm(Skin_NoSun, Skin_Sun)
# HeartAA and HeartLV to Heart
HeartLV <- HeartLV[ ,4:ncol(HeartLV)]
Heart <- cbind(HeartAA, HeartLV)
rm(HeartAA, HeartLV)
# EsophagusGJ and EsophagusMuscularis to Esophagus
EsophagusGJ <- EsophagusGJ[ ,4:ncol(EsophagusGJ)]
Esophagus <- cbind(EsophagusMuscularis, EsophagusGJ)
rm(EsophagusMuscularis, EsophagusGJ)
# CervixEcto, CervixEndo, FallopianTubes, Ovary, Uterus and Vagina to FemaleReproductive
CervixEndo <- CervixEndo[ ,4:ncol(CervixEndo)]
FallopianTubes <- FallopianTubes[ ,4:ncol(FallopianTubes)]
Ovary <- Ovary[ ,4:ncol(Ovary)]
Uterus <- Uterus[ ,4:ncol(Uterus)]
Vagina <- Vagina[ ,4:ncol(Vagina)]
FemaleReproductive <- cbind(CervixEcto, CervixEndo, FallopianTubes, Ovary, Uterus, Vagina)
rm(CervixEcto, CervixEndo, FallopianTubes, Ovary, Uterus, Vagina)
# Artery_aorta, Artery_coronary and Artery_tibial to Arteries
Artery_aorta <- Artery_aorta[ ,4:ncol(Artery_aorta)]
Artery_coronary <- Artery_coronary[ ,4:ncol(Artery_coronary)]
Arteries <- cbind(Artery_tibial, Artery_aorta, Artery_coronary)
rm(Artery_aorta, Artery_coronary, Artery_tibial)
# BrainAmygdala, BrainACC, BrainCaudate, BrainCerebellarHemi, BrainCerebellum, BrainCortex, 
# BrainFrontalCortex, BrainHippocampus, BrainHypothalamus, BrainNucleusAccumbens, BrainPutamen, 
# BrainSpinalCord and BrainSubstantiaNigra to Brain
BrainACC <- BrainACC[ ,4:ncol(BrainACC)]
BrainCaudate <- BrainCaudate[ ,4:ncol(BrainCaudate)]
BrainCerebellarHemi <- BrainCerebellarHemi[ ,4:ncol(BrainCerebellarHemi)]
BrainCerebellum <- BrainCerebellum[ ,4:ncol(BrainCerebellum)]
BrainCortex <- BrainCortex[ ,4:ncol(BrainCortex)]
BrainFrontalCortex <- BrainFrontalCortex[ ,4:ncol(BrainFrontalCortex)]
BrainHippocampus <- BrainHippocampus[ ,4:ncol(BrainHippocampus)]
BrainHypothalamus <- BrainHypothalamus[ ,4:ncol(BrainHypothalamus)]
BrainNucleusAccumbens <- BrainNucleusAccumbens[ ,4:ncol(BrainNucleusAccumbens)]
BrainPutamen <- BrainPutamen[ ,4:ncol(BrainPutamen)]
BrainSpinalCord <- BrainSpinalCord[ ,4:ncol(BrainSpinalCord)]
BrainSubstantiaNigra <- BrainSubstantiaNigra[ ,4:ncol(BrainSubstantiaNigra)]
Brain <- cbind(BrainAmygdala, BrainACC, BrainCaudate, BrainCerebellarHemi, BrainCerebellum, BrainCortex,
               BrainFrontalCortex, BrainHippocampus, BrainHypothalamus, BrainNucleusAccumbens, BrainPutamen,
               BrainSpinalCord, BrainSubstantiaNigra)
rm(BrainAmygdala, BrainACC, BrainCaudate, BrainCerebellarHemi, BrainCerebellum, BrainCortex,
   BrainFrontalCortex, BrainHippocampus, BrainHypothalamus, BrainNucleusAccumbens, BrainPutamen,
   BrainSpinalCord, BrainSubstantiaNigra)

#Generated a list of matrices that will be used to iterate over in a future for loop.
tissue_list <- list(Adipose, Adrenal_gland, Arteries, Bladder, Brain, Breast, FemaleReproductive,
                    Fibroblasts, Lymphocytes, ColonSigmoid, ColonTransverse, Esophagus, EsophagusMucosa,
                    Heart, Kidney, Liver, Lung, SalivaryGland, MuscleSkeletal, NerveTibial, Pancreas, Pituitary, 
                    Prostate, Skin, SmallIntestine, Spleen, Stomach, Testis, Thyroid, Whole_blood)

#Assigned names to the list of matrices that will be used in the future for loop to change the col name and store the result
names(tissue_list) <- c("Adipose", "Adrenal_gland", "Arteries", "Bladder", "Brain", "Breast", "FemaleReproductive", "Fibroblasts",
                        "Lymphocytes", "ColonSigmoid", "ColonTransverse", "Esophagus", "EsophagusMucosa", "Heart", "Kidney", "Liver", 
                        "Lung", "SalivaryGland", "MuscleSkeletal", "NerveTibial", "Pancreas", "Pituitary", "Prostate", "Skin", 
                        "SmallIntestine", "Spleen", "Stomach", "Testis", "Thyroid", "Whole_blood")


#### Code for generation of gene expression files and Phenotype class files for 2 Median values per merged tissue (by dividing them into two groups with similar size) #### 
# Loop through each matrix that is present in the matrix_list to make the same calculations in all tissues
for (i in seq_along(tissue_list)) {
  matrix <- tissue_list[[i]]
  
  # Set gene names as row names and keep only expression columns
  rownames(matrix) <- matrix[, 2]
  matrix <- matrix[, 4:ncol(matrix)]
  
  # Normalize to CPM
  matrix_sum <- apply(matrix, 2, sum)
  matrix_new <- matrix
  for (n in seq_len(ncol(matrix))) {
    matrix_new[, n] <- round((matrix[, n] * 1e6) / matrix_sum[n], digits = 3)
  }
  
  # Split samples into two nearly equal groups
  sample_names <- colnames(matrix_new)
  n_samples <- length(sample_names)
  group1_idx <- sample_names[1:floor(n_samples / 2)]
  group2_idx <- sample_names[(floor(n_samples / 2) + 1):n_samples]
  
  # Calculate median CPM per gene for each group
  median_group1 <- apply(matrix_new[, group1_idx, drop = FALSE], 1, median)
  median_group2 <- apply(matrix_new[, group2_idx, drop = FALSE], 1, median)
  
  # Combine into one matrix
  median_matrix <- cbind(median_group1, median_group2)
  
  # Use the actual tissue name for the column names
  tissue_name <- names(tissue_list)[i]
  colnames(median_matrix) <- c(paste0(tissue_name, "1"), paste0(tissue_name, "2"))
    # Assign to an object named like "Liver_MedianCPM"
  matrix_name <- paste0(tissue_name, "_MedianCPM")
  assign(matrix_name, median_matrix)
}

#Generated a list of the result matrices (containing the median CPM values) to be used in a cbind command for merging all the results in a single matrix
tissue_list_medianCPM <- list(Adipose_MedianCPM, Adrenal_gland_MedianCPM, Arteries_MedianCPM, Bladder_MedianCPM, Brain_MedianCPM,  Breast_MedianCPM,
                              FemaleReproductive_MedianCPM, Fibroblasts_MedianCPM, Lymphocytes_MedianCPM, ColonSigmoid_MedianCPM, ColonTransverse_MedianCPM, 
                              Esophagus_MedianCPM, EsophagusMucosa_MedianCPM, Heart_MedianCPM, Kidney_MedianCPM, Liver_MedianCPM, Lung_MedianCPM, SalivaryGland_MedianCPM,
                              MuscleSkeletal_MedianCPM, NerveTibial_MedianCPM, Pancreas_MedianCPM, Pituitary_MedianCPM, Prostate_MedianCPM, Skin_MedianCPM, 
                              SmallIntestine_MedianCPM, Spleen_MedianCPM, Stomach_MedianCPM, Testis_MedianCPM, Thyroid_MedianCPM, Whole_blood_MedianCPM)

#Use do.call with cbind to merge horizontally the results from all tissues into a single tissue_matrix
Median_CPM_Per_Tissue <- do.call(cbind, tissue_list_medianCPM)

#Extract the 2nd and 3rd columns of a matrix (as they are all identical to create a dictionary.
#The EnsblID are the keys and the GeneDescription are the values of the dictionary. 
keys <- Liver[, 2]
values <- Liver[, 3]
dictionary <- as.list(setNames(values, keys))

EnsblID_to_GeneName <- cbind(keys, values)

# Use this dictionary to change the rownames from EnsblID to GeneID 
# 1. Get the current rownames from Median_CPM_Per_Tissue
ensembl_ids <- rownames(Median_CPM_Per_Tissue)
# 2. Find the matching gene names for the Ensembl IDs using EnsblID_to_GeneName
gene_names <- EnsblID_to_GeneName[match(ensembl_ids, EnsblID_to_GeneName[, 1]), 2]
# 3. Add a new column with the gene names and title it 'GeneID'
Median_CPM_Per_Tissue <- cbind(GeneID = gene_names, Median_CPM_Per_Tissue)

## Generation of a phenotype classes file, required by the CIBERSORTx
## Containing 1 in the corresponding tissue and 2 for the rest.

# Convert the column names into a matrix with one column
# Create a 30x60 matrix filled with the number 2 and substitute the diagonal with 1
matrix_of_twos <- matrix(2, nrow = 30, ncol = 60)
# Modify the matrix to set 1 in specific positions of the tissues
for (i in 1:30) {
  matrix_of_twos[i, (2*i-1):(2*i)] <- 1  # Set columns (2i-1) and (2i) to 1 in each row
}

# Create a matrix with 1 column and 30 rows using tissue names
Phenotype <- matrix(names(tissue_list), ncol = 1)

PhenotypeMatrix <- cbind(Phenotype, matrix_of_twos)
write.table(PhenotypeMatrix, file = "20250405_PhenotypeClass_LessTissueV2_2Median.tsv", sep = "\t", col.names = FALSE, row.names = FALSE, quote = FALSE)

## Generation of a Median_CPM_Per_Tissue file containing only unique gene entries, required by the CIBERSORTx
# Step 1: Extract the first column from the Median_CPM_Per_Tissue matrix
first_column <- Median_CPM_Per_Tissue[, 1]
# Step 2: Identify the first instance of each value (removing duplicates)
unique_rows <- !duplicated(first_column)
# Step 3: Subset the matrix to keep only rows with the first occurrence of duplicates
Median_CPM_Per_Tissue_unique <- as.matrix(Median_CPM_Per_Tissue[unique_rows, ])
write.table(Median_CPM_Per_Tissue_unique, file = "20250405_GeneID_LessTissueV2_2Median-Unique.tsv", sep = "\t", row.names = FALSE, quote = FALSE)
column_names <- colnames(Median_CPM_Per_Tissue_unique)

write.table(Median_CPM_Per_Tissue_unique, file = "20250405_Both_LessTissueV2_2Median-Unique.tsv", sep = "\t", row.names = TRUE, quote = FALSE)

#### Code for generation of gene expression files and Phenotype class files for 5 unique samples per merged tissue #### 
# Loop through each matrix that is present in the matrix_list to make the same calculations in all tissues
for (i in seq_along(tissue_list)) {
  matrix <- tissue_list[[i]]
  
  # Set gene names as row names and keep only expression columns
  rownames(matrix) <- matrix[, 2]
  matrix <- matrix[, 4:ncol(matrix)]
  
  # Normalize to CPM
  matrix_sum <- apply(matrix, 2, sum)
  matrix_new <- matrix
  for (n in seq_len(ncol(matrix))) {
    matrix_new[, n] <- round((matrix[, n] * 1e6) / matrix_sum[n], digits = 3)
  }
  
  # Sample 5 random columns
  sampled_cols <- sample(ncol(matrix_new), 5)
  sampled_matrix <- matrix_new[, sampled_cols]
  
  # Rename columns to Tissue1, Tissue2, ..., Tissue5
  tissue_name <- names(tissue_list)[i]  # get the name (e.g., "Liver")
  colnames(sampled_matrix) <- paste0(tissue_name, seq_len(5))
  
  # Assign the result to an object named like "Liver_5Unique"
  matrix_name <- paste0(tissue_name, "_5Unique")
  assign(matrix_name, sampled_matrix)
}

#Generated a list of the result matrices (containing the median CPM values) to be used in a cbind command for merging all the results in a single matrix
tissue_list_5Unique <- list(Adipose_5Unique, Adrenal_gland_5Unique, Arteries_5Unique, Bladder_5Unique, Brain_5Unique,  Breast_5Unique,
                              FemaleReproductive_5Unique, Fibroblasts_5Unique, Lymphocytes_5Unique, ColonSigmoid_5Unique, ColonTransverse_5Unique, 
                              Esophagus_5Unique, EsophagusMucosa_5Unique, Heart_5Unique, Kidney_5Unique, Liver_5Unique, Lung_5Unique, SalivaryGland_5Unique,
                              MuscleSkeletal_5Unique, NerveTibial_5Unique, Pancreas_5Unique, Pituitary_5Unique, Prostate_5Unique, Skin_5Unique, 
                              SmallIntestine_5Unique, Spleen_5Unique, Stomach_5Unique, Testis_5Unique, Thyroid_5Unique, Whole_blood_5Unique)

#Use do.call with cbind to merge horizontally the results from all tissues into a single tissue_matrix
Sampling5_CPM_Per_Tissue <- do.call(cbind, tissue_list_5Unique)

# Use the dictionary to change the rownames from EnsblID to GeneID 
# 1. Get the current rownames from Median_CPM_Per_Tissue
ensembl_ids <- rownames(Sampling5_CPM_Per_Tissue)
# 2. Find the matching gene names for the Ensembl IDs using EnsblID_to_GeneName
gene_names <- EnsblID_to_GeneName[match(ensembl_ids, EnsblID_to_GeneName[, 1]), 2]
# 3. Add a new column with the gene names and title it 'GeneID'
Sampling5_CPM_Per_Tissue <- cbind(GeneID = gene_names, Sampling5_CPM_Per_Tissue)

## Generation of a phenotype classes file, required by the CIBERSORTx
## Containing 1 in the corresponding tissue and 2 for the rest.
# Extract the column names (excluding the first one)
col_names <- colnames(Sampling5_CPM_Per_Tissue)[-1]
# Convert the column names into a matrix with one column
Phenotype <- matrix(names(tissue_list), ncol = 1)
# Create a 30x30 matrix filled with the number 2 and substitute the diagonal with 1
matrix_of_twos <- matrix(2, nrow = 30, ncol = 150)
# Modify the matrix to set 1 in specific positions
for (i in 1:30) {
  matrix_of_twos[i, ((5 * (i - 1) + 1):(5 * i))] <- 1  # Set columns 1-5, 6-10, etc., to 1 in each row
}

PhenotypeMatrix <- cbind(Phenotype, matrix_of_twos)
write.table(PhenotypeMatrix, file = "20250405_PhenotypeClass_LessTissueV2_Sampling5.tsv", sep = "\t", col.names = FALSE, row.names = FALSE, quote = FALSE)

## Generation of a Sampling5_CPM_Per_Tissue file containing only unique gene entries, required by the CIBERSORTx
# Step 1: Extract the first column from the Sampling5_CPM_Per_Tissue matrix
first_column <- Sampling5_CPM_Per_Tissue[, 1]
# Step 2: Identify the first instance of each value (removing duplicates)
unique_rows <- !duplicated(first_column)
# Step 3: Subset the matrix to keep only rows with the first occurrence of duplicates
Sampling5_CPM_Per_Tissue <- as.matrix(Sampling5_CPM_Per_Tissue[unique_rows, ])
write.table(Sampling5_CPM_Per_Tissue, file = "20250405_GeneID_LessTissueV2_Sampling5-Unique.tsv", sep = "\t", row.names = FALSE, quote = FALSE)

#### Code for generation of gene expression files and Phenotype class files for 10 unique samples per merged tissue #### 
# Loop through each matrix that is present in the matrix_list to make the same calculations in all tissues
for (i in seq_along(tissue_list)) {
  matrix <- tissue_list[[i]]
  
  # Set gene names as row names and keep only expression columns
  rownames(matrix) <- matrix[, 2]
  matrix <- matrix[, 4:ncol(matrix)]
  
  # Normalize to CPM
  matrix_sum <- apply(matrix, 2, sum)
  matrix_new <- matrix
  for (n in seq_len(ncol(matrix))) {
    matrix_new[, n] <- round((matrix[, n] * 1e6) / matrix_sum[n], digits = 3)
  }
  
  # Sample 10 random columns
  sampled_cols <- sample(ncol(matrix_new), 10)
  sampled_matrix <- matrix_new[, sampled_cols]
  
  # Rename columns to Tissue1, Tissue2, ..., Tissue10
  tissue_name <- names(tissue_list)[i]  # get the name (e.g., "Liver")
  colnames(sampled_matrix) <- paste0(tissue_name, seq_len(10))
  
  # Assign the result to an object named like "Liver_10Unique"
  matrix_name <- paste0(tissue_name, "_10Unique")
  assign(matrix_name, sampled_matrix)
}

#Generated a list of the result matrices (containing the median CPM values) to be used in a cbind command for merging all the results in a single matrix
tissue_list_10Unique <- list(Adipose_10Unique, Adrenal_gland_10Unique, Arteries_10Unique, Bladder_10Unique, Brain_10Unique,  Breast_10Unique,
                            FemaleReproductive_10Unique, Fibroblasts_10Unique, Lymphocytes_10Unique, ColonSigmoid_10Unique, ColonTransverse_10Unique, 
                            Esophagus_10Unique, EsophagusMucosa_10Unique, Heart_10Unique, Kidney_10Unique, Liver_10Unique, Lung_10Unique, SalivaryGland_10Unique,
                            MuscleSkeletal_10Unique, NerveTibial_10Unique, Pancreas_10Unique, Pituitary_10Unique, Prostate_10Unique, Skin_10Unique, 
                            SmallIntestine_10Unique, Spleen_10Unique, Stomach_10Unique, Testis_10Unique, Thyroid_10Unique, Whole_blood_10Unique)

#Use do.call with cbind to merge horizontally the results from all tissues into a single tissue_matrix
Sampling10_CPM_Per_Tissue <- do.call(cbind, tissue_list_10Unique)

# Use the dictionary to change the rownames from EnsblID to GeneID 
# 1. Get the current rownames from Median_CPM_Per_Tissue
ensembl_ids <- rownames(Sampling10_CPM_Per_Tissue)
# 2. Find the matching gene names for the Ensembl IDs using EnsblID_to_GeneName
gene_names <- EnsblID_to_GeneName[match(ensembl_ids, EnsblID_to_GeneName[, 1]), 2]
# 3. Add a new column with the gene names and title it 'GeneID'
Sampling10_CPM_Per_Tissue <- cbind(GeneID = gene_names, Sampling10_CPM_Per_Tissue)

## Generation of a phenotype classes file, required by the CIBERSORTx
## Containing 1 in the corresponding tissue and 2 for the rest.
# Convert the column names into a matrix with one column
Phenotype <- matrix(names(tissue_list), ncol = 1)
# Create a 30x30 matrix filled with the number 2 and substitute the diagonal with 1
matrix_of_twos <- matrix(2, nrow = 30, ncol = 300)
for (i in 1:30) {
  matrix_of_twos[i, ((10 * (i - 1) + 1):(10 * i))] <- 1  # Set columns 1-10, 11-20, etc., to 1 in each row
}
PhenotypeMatrix <- cbind(Phenotype, matrix_of_twos)
write.table(PhenotypeMatrix, file = "20250405_PhenotypeClass_LessTissueV2_Sampling10.tsv", sep = "\t", col.names = FALSE, row.names = FALSE, quote = FALSE)

## Generation of a Sampling10_CPM_Per_Tissue file containing only unique gene entries, required by the CIBERSORTx
# Step 1: Extract the first column from the Sampling10_CPM_Per_Tissue matrix
first_column <- Sampling10_CPM_Per_Tissue[, 1]
# Step 2: Identify the first instance of each value (removing duplicates)
unique_rows <- !duplicated(first_column)
# Step 3: Subset the matrix to keep only rows with the first occurrence of duplicates
Sampling10_CPM_Per_Tissue <- as.matrix(Sampling10_CPM_Per_Tissue[unique_rows, ])
write.table(Sampling10_CPM_Per_Tissue, file = "20250405_GeneID_LessTissueV2_Sampling10-Unique.tsv", sep = "\t", row.names = FALSE, quote = FALSE)
