##################################################################
##                                                              ##
##                  ComTrak species detections                  ##
##                                                              ##
##                Groundtruthed data extraction                 ##
##                                                              ##
##                       Oct 30th 2024                          ##
##                                                              ##
##################################################################
rm(list = ls())
options(width = 100)

library(tidyverse)
library(data.table)

#_______________________________________________________________________________
#### 1. Visual standardisation parameters - from Francesco ####

camera_resolution <- c(5440, 3060)
field_of_view <- c(24, 13.5)

xscale <- camera_resolution[1]/field_of_view[1]
yscale <- camera_resolution[2]/field_of_view[2]

area_scale <- (camera_resolution[1]*camera_resolution[2])/(field_of_view[1]*field_of_view[2])

video_duration <- 12 # seconds

#_______________________________________________________________________________
#### 2. 5-species community ####

## Obtaining file names
allfiles_5spp <- list.files("data/groundtruthed_data/5_species_community/")
rawfiles_5spp <- allfiles_5spp[grep("multispp", allfiles_5spp)]

groundtruthed_5species_videos <- 
  bind_rows(lapply(rawfiles_5spp, function(x){
  
  # raw data with species probabilities
  c_raw = read_delim(paste0("data/groundtruthed_data/5_species_community/", x))
  
  # validated species names
  c_speciesnames = read_delim(paste0("data/groundtruthed_data/5_species_community/", gsub("TC_multispp", "labels", x))) %>% 
    dplyr::select(Frame, ID, Species = Label)
  
  # tracking duration to normalise per video
  tracking_duration = video_duration*(max(c_raw$Frame)-min(c_raw$Frame))/max(c_raw$Frame)
  
  # go through and wrangle
  c_raw %>% 
    left_join(x= ., y = c_speciesnames, by = c("ID", "Frame")) %>% 
    mutate(Replicate = as.numeric(unlist(strsplit(x, "_"))[4])) %>% 
    # getting rid of non-protist/mixed data for now
    filter(!(Species %in% c("MIXspp", "NONpro"))) %>% 
    # 1. false IDs
    group_by(ID) %>% 
    filter(n() > 3) %>% 
    ungroup() %>% 
    # 2. morphology
    mutate(time_s = ((Frame-min(Frame))/(((max(Frame)-min(Frame))/tracking_duration))), 
           CentroidX_mm = CentroidX/xscale, CentroidY_mm = CentroidY/yscale, 
           Length_um = (Length/xscale)*1000, Width_um = (Width/yscale)*1000,
           Area_sqrd_um = (Area/area_scale)*1000000) %>% 
    # 3. abundance
    group_by(Frame) %>% 
    mutate(abundance_frame = n()) %>% 
    ungroup() %>% 
    # 4. speed
    group_by(ID) %>% 
    mutate(deltaX = CentroidX_mm - shift(CentroidX_mm, 1L, type = "lag"),
           deltaY = CentroidY_mm - shift(CentroidY_mm, 1L, type = "lag"),
           deltaTime = time_s - shift(time_s, 1L, type = "lag")) %>% 
    ungroup() %>% 
    mutate(velocity = sqrt(deltaX^2 + deltaY^2)/deltaTime) %>% 
    mutate(Species = case_when(
      Species == "PARcau" ~ "Paramecium_caudatum",
      Species == "PARbur" ~ "Paramecium_bursaria",
      Species == "SPIter" ~ "Spirostomum_teres",
      Species == "STEvir" ~ "Stenostomum_virginianum",
      Species == "DIDnas" ~ "Didinium_nasutum")) %>% 
    rename_with(tolower) %>% 
    dplyr::select(id, frame, time_s, replicate, species, didinium_nasutum = didnas,
                  non_protist = nonpro, paramecium_bursaria = parbur,
                  paramecium_caudatum = parcau, spirostomum_teres = spiter,
                  stenostomum_virginianum = stevir, length_um, width_um, 
                  area_sqrd_um, abundance_frame, deltax, deltay, velocity) %>% 
    drop_na()
  
}))

save(groundtruthed_5species_videos, file = "data/groundtruthed_data/groundtruthed_5species_videos.RData")

#_______________________________________________________________________________
#### 3. Real experimental data ####

## getting natural experiment files
exp_test_files <- list.files("data/groundtruthed_data/natural_experiment_test/")[-9]
exp_train_files <- list.files("data/groundtruthed_data/natural_experiment_test/comtrak_train/")

## file names from track and class (TC)
exp_test_tc <- exp_test_files[grep("TC", exp_test_files)]
exp_train_tc <- exp_train_files[grep("TC", exp_train_files)]

exp_tc_all <- c(exp_test_tc, exp_train_tc)

groundtruthed_experiment_videos <- bind_rows(lapply(exp_tc_all, function(x){
  
  ## Add specification for whether its a test/training file from comtrak
  if(x %in% exp_test_tc == TRUE){
    c_type = "test"
    
    # raw data with species probabilities
    c_raw = read_delim(paste0("data/groundtruthed_data/natural_experiment_test/", x))
    
    # validated species names
    c_speciesnames = read_delim(paste0("data/groundtruthed_data/natural_experiment_test/", gsub("TC", "labels", x))) %>% 
      dplyr::select(Frame, ID, Species = Label)
  }
  
  else{
    c_type = "training"
    
    # raw data with species probabilities
    c_raw = read_delim(paste0("data/groundtruthed_data/natural_experiment_test/comtrak_train/", x))
    
    # validated species names
    c_speciesnames = read_delim(paste0("data/groundtruthed_data/natural_experiment_test/comtrak_train/", gsub("TC", "labels", x))) %>% 
      dplyr::select(Frame, ID, Species = Label)
  }
  
  # tracking duration to normalise per video
  tracking_duration = video_duration*(max(c_raw$Frame)-min(c_raw$Frame))/max(c_raw$Frame)
  
  # go through and wrangle
  c_raw %>% 
    left_join(x= ., y = c_speciesnames, by = c("ID", "Frame")) %>% 
    mutate(Replicate = as.numeric(unlist(strsplit(x, "_"))[4])) %>% 
    # getting rid of non-protist/mixed data for now
    filter(!(Species %in% c("MIXspp", "NONpro"))) %>% 
    # 1. false IDs
    group_by(ID) %>% 
    filter(n() > 3) %>% 
    ungroup() %>% 
    # 2. morphology
    mutate(time_s = ((Frame-min(Frame))/(((max(Frame)-min(Frame))/tracking_duration))), 
           CentroidX_mm = CentroidX/xscale, CentroidY_mm = CentroidY/yscale, 
           Length_um = (Length/xscale)*1000, Width_um = (Width/yscale)*1000,
           Area_sqrd_um = (Area/area_scale)*1000000) %>% 
    # 3. abundance
    group_by(Frame) %>% 
    mutate(abundance_frame = n()) %>% 
    ungroup() %>% 
    # 4. speed
    group_by(ID) %>% 
    mutate(deltaX = CentroidX_mm - shift(CentroidX_mm, 1L, type = "lag"),
           deltaY = CentroidY_mm - shift(CentroidY_mm, 1L, type = "lag"),
           deltaTime = time_s - shift(time_s, 1L, type = "lag")) %>% 
    ungroup() %>% 
    mutate(velocity = sqrt(deltaX^2 + deltaY^2)/deltaTime) %>% 
    mutate(Species = case_when(
      Species == "PARcau" ~ "Paramecium_caudatum",
      Species == "SPIter" ~ "Spirostomum_teres",
      Species == "STEvir" ~ "Stenostomum_virginianum")) %>% 
    rename_with(tolower) %>% 
    dplyr::select(id, frame, time_s, replicate, species, non_protist = nonpro, 
                  paramecium_caudatum = parcau, spirostomum_teres = spiter,
                  stenostomum_virginianum = stevir, length_um, width_um, 
                  area_sqrd_um, abundance_frame, deltax, deltay, velocity) %>% 
    drop_na() %>% 
    mutate(type = c_type)
  
}))

save(groundtruthed_experiment_videos, file = "data/groundtruthed_data/groundtruthed_experiment_videos.RData")

#_______________________________________________________________________________
#### 4. Single species videos ####

## Obtaining file names
allfiles_singlespecies <- list.files("data/groundtruthed_data/single_species/")
tcfiles_singlespecies <- allfiles_singlespecies[grep("TC[.]", allfiles_singlespecies)] 

groundtruthed_singlespecies_videos  <- bind_rows(lapply(tcfiles_singlespecies, function(x){
  
  # raw data with species probabilities
  c_raw = read_delim(paste0("data/groundtruthed_data/single_species/", x))
  
  # validated species names
  c_speciesnames = read_delim(paste0("data/groundtruthed_data/single_species/", gsub("TC", "labels", x))) %>% 
    dplyr::select(Frame, ID, Species = Label)
  
  # tracking duration to normalise per video
  tracking_duration = video_duration*(max(c_raw$Frame)-min(c_raw$Frame))/max(c_raw$Frame)
  
  # go through and wrangle
  c_raw %>% 
    left_join(x= ., y = c_speciesnames, by = c("ID", "Frame")) %>% 
    mutate(Replicate = as.numeric(unlist(strsplit(x, "_"))[2])) %>% 
    # getting rid of non-protist/mixed data for now
    filter(!(Species %in% c("MIXspp", "NONpro"))) %>% 
    # 1. false IDs
    group_by(ID) %>% 
    filter(n() > 3) %>% 
    ungroup() %>% 
    # 2. morphology
    mutate(time_s = ((Frame-min(Frame))/(((max(Frame)-min(Frame))/tracking_duration))), 
           CentroidX_mm = CentroidX/xscale, CentroidY_mm = CentroidY/yscale, 
           Length_um = (Length/xscale)*1000, Width_um = (Width/yscale)*1000,
           Area_sqrd_um = (Area/area_scale)*1000000) %>% 
    # 3. abundance
    group_by(Frame) %>% 
    mutate(abundance_frame = n()) %>% 
    ungroup() %>% 
    # 4. speed
    group_by(ID) %>% 
    mutate(deltaX = CentroidX_mm - shift(CentroidX_mm, 1L, type = "lag"),
           deltaY = CentroidY_mm - shift(CentroidY_mm, 1L, type = "lag"),
           deltaTime = time_s - shift(time_s, 1L, type = "lag")) %>% 
    ungroup() %>% 
    mutate(velocity = sqrt(deltaX^2 + deltaY^2)/deltaTime) %>% 
    mutate(Species = case_when(
      Species == "PARcau" ~ "Paramecium_caudatum",
      Species == "PARbur" ~ "Paramecium_bursaria",
      Species == "SPIter" ~ "Spirostomum_teres",
      Species == "STEvir" ~ "Stenostomum_virginianum",
      Species == "DIDnas" ~ "Didinium_nasutum")) %>% 
    rename_with(tolower) %>% 
    dplyr::select(id, frame, time_s, replicate, species, didinium_nasutum = didnas,
                  non_protist = nonpro, paramecium_bursaria = parbur,
                  paramecium_caudatum = parcau, spirostomum_teres = spiter,
                  stenostomum_virginianum = stevir, length_um, width_um, 
                  area_sqrd_um, abundance_frame, deltax, deltay, velocity) %>% 
    drop_na()
  
}))

save(groundtruthed_singlespecies_videos, file = "data/groundtruthed_data/groundtruthed_singlespecies_videos.RData")

