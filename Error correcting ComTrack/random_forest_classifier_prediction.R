#####################################################################
##                                                                 ##
##                  ComTrak species predictions                    ##
##                                                                 ##
##               Secondary Classifier Random Forest                ##
##                                                                 ##
##                       Oct 30th 2024                             ##
##                                                                 ##
#####################################################################

rm(list = ls())
options(width = 100)

# general
library(tidyverse)
library(data.table)
library(flextable)

## random forest + GBM
library(rsample)
library(randomForest)

#_______________________________________________________________________________
#### 1. Visual standardisation parameters - from Francesco ####

camera_resolution <- c(5440, 3060)
field_of_view <- c(24, 13.5)

xscale <- camera_resolution[1]/field_of_view[1]
yscale <- camera_resolution[2]/field_of_view[2]

area_scale <- (camera_resolution[1]*camera_resolution[2])/(field_of_view[1]*field_of_view[2])

video_duration <- 12 # seconds

#_______________________________________________________________________________
#### 2. Loading Ground truthed data ####

## 2a. Select which ground truthed data you want to use from:
##
## - "5species"
## - "experiment"
## - "singlespecies"

gt_data <- "5species"
load(paste0("data/groundtruthed_data/groundtruthed_", gt_data, "_videos.RData"),
     verbose = T)

## take a look 
groundtruth_data_raw <- eval(parse(text = paste0("groundtruthed_", gt_data, "_videos")))
glimpse(groundtruth_data_raw)

#_______________________________________________________________________________
#### 3. Random forest classifier ####

## You may need to adjust the select depending on the species you are working on
groundtruth_data <- groundtruth_data_raw %>% 
  mutate(species = as.factor(species)) %>% 
  dplyr::select(species, time_s, didinium_nasutum:velocity)

# creating training and testing samples 
set.seed(420)
gt_split <- initial_split(groundtruth_data, prop = 0.8) 
gt_train <- training(gt_split)
gt_test <- testing(gt_split)

# Un-tuned classifier
set.seed(420)
random_forest_species_classifier <- 
  randomForest(formula = species ~ ., data = gt_train, importance = T)

#_______________________________________________________________________________
#### 4. Test error of the classifier ####

gt_test %>% 
  mutate(pred_species = predict(random_forest_species_classifier, gt_test)) %>% 
  group_by(species, pred_species) %>% 
  summarise(n = n()) %>% ungroup() %>% 
  group_by(species) %>% 
  mutate(error_rate = (sum(n) - n[which(pred_species == species)])/(sum(n))) %>% 
  summarise(`Number of predictions` = sum(n),
            `Test error %` = round(error_rate[1]*100, 1)) %>% 
  rename(Species = species) %>% 
  mutate(Species = gsub("_", " ", Species)) %>% 
  flextable(cwidth = 2) 

#_______________________________________________________________________________
#### 5. Predictions with new data ####

## Set up 5.1 - Your folder in data_to_predict (must be a folder with the / in there)
## Also create this as an empty folder in output/
my_folder <- "multispecies_2024_august/"

## Set up 5.2 - Choose which species you have (delete entries of this vector)
crr_species <- c("DIDnas", "NONpro", "PARbur",  "PARcau", "SPIter", "STEvir")

## Set up 5.3 - Your file list - may need ammendments if you have different types of data
pred_files_all <- list.files(paste0("data/data_to_predict/", my_folder))

## Standardised data extraction code
pred_data <- bind_rows(lapply(pred_files_all, function(x){
  
  # Load raw data with species probabilities
  c_raw = read_delim(paste0("data/data_to_predict/", my_folder, x))
  
  # tracking duration to normalise per video
  tracking_duration = video_duration*(max(c_raw$Frame) - min(c_raw$Frame))/max(c_raw$Frame)
  
  # species not in current prediciton to add columns with 0
  species_to_add = crr_species[which(crr_species %in% colnames(c_raw) == F)]
  
  ### This is the data handling to obtain ABUNDANCE and morphological estimates 
  
  c_raw <- c_raw %>% 
    
    bind_cols(setNames(rep(list(0), length(species_to_add)), species_to_add)) %>% 
    
    # Add Replicate from the file name - POSITION 8 MAY CHANGE BASED ON YOUR NAMING
    mutate(Replicate = gsub(".txt", "", unlist(strsplit(x, "_"))[8])) %>% 
    
    # 1. False IDs (IDs that appear in more than 3 frames)
    group_by(ID) %>% 
    filter(n() > 3) %>% 
    ungroup() %>% 
    
    # 2. Morphology calculations
    mutate(time_s = ((Frame - min(Frame)) / (((max(Frame) - min(Frame)) / tracking_duration))),
           CentroidX_mm = CentroidX / xscale,
           CentroidY_mm = CentroidY / yscale,
           Length_um = (Length / xscale) * 1000,
           Width_um = (Width / yscale) * 1000,
           Area_sqrd_um = (Area / area_scale) * 1000000) %>% 
    
    # 3. Abundance calculations
    group_by(Frame) %>% 
    mutate(abundance_frame = n()) %>% 
    ungroup() %>% 
    
    # 4. Speed calculations
    group_by(ID) %>% 
    mutate(deltaX = CentroidX_mm - dplyr::lag(CentroidX_mm),
           deltaY = CentroidY_mm - dplyr::lag(CentroidY_mm),
           deltaTime = time_s - dplyr::lag(time_s)) %>% 
    ungroup() %>% 
    mutate(velocity = sqrt(deltaX^2 + deltaY^2) / deltaTime) %>% 
    rename_with(tolower) %>% 
    dplyr::select(id, frame, time_s, replicate,
                  non_protist = nonpro, didinium_nasutum = didnas,
                  paramecium_bursaria = parbur,
                  paramecium_caudatum = parcau, spirostomum_teres = spiter,
                  stenostomum_virginianum = stevir, length_um, width_um, 
                  area_sqrd_um, abundance_frame, deltax, deltay, velocity) %>% 
    drop_na()  # Remove rows with missing values
  
  return(c_raw)  
  
}))

### Do the predictions from the random forest classifier
species_predictions <- pred_data %>% 
  mutate(species_prediction = predict(random_forest_species_classifier, .))

glimpse(species_predictions)

## Save to your specific folder in output, need to have created the specific folder name for your use case
save(species_predictions, file = paste0("output/", my_folder, "species_predictions.RData"))


