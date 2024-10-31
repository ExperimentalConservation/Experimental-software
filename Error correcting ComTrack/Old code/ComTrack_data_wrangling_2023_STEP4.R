rm(list=ls())
##################################################################################################
####################### Extracting data from ComTrack video output ###############################
##------------------------- F. Cerini 14/03/2023 ---------------------------------------------####
##################################################################################################

#################### USING DATASHEETS CREATED WITH STEP4 OF ComTrack: "Track and Classify" ######
# These data for the code will contain the columns with probability of each ID to be species x or Y ##

# ---- 1. File directory ----

# put the Code (.R) file where data sheets of the videos ".txt" are; there will be the working directory
setwd(dirname(rstudioapi::getActiveDocumentContext()$path))

# or set the wd in the classic way
setwd("C:\\Users\\mr21762\\Dropbox\\Bristol\\Research\\Laboratory ad protists\\ComTrack_Method_Paper\\Exp_2_ComTrack_data\\Testing_model_output")

# ---- 2. Packages ----
require(ggplot2) 
require(ggdist)
require(ggpubr)
require(ggrepel)
require(dplyr) 
require(vroom)
require(data.table)
require(ggh4x)
require(plotrix)
library(gridExtra)

# ---- 3. Data import and handling----

### set the video resolution to re-scale from pixels to mm and um 

#pixels resolution
camera_resolution = c(5440, 3060)

#field of view of the camera in millilmeters (THIS IS AT MAGNIFICATION 2x)
field_of_view = c(24, 13.5)

# calculate scales on the horizontal and vertical axes of the videos
xscale<-camera_resolution[1]/field_of_view[1]

yscale<-camera_resolution[2]/field_of_view[2]

# and for the area calulated in pixels

area_scale<-(camera_resolution[1]*camera_resolution[2])/(field_of_view[1]*field_of_view[2])

# specify the video duration in seconds
video_duration<-12

#first and last name of the species in your model in alphabetic order (Check in the ComTrack output file)
first_sp<-"DIDnas"
last_sp<-"STEvir"

### create a list with all the file names (each object that ends in ".txt" in your folder, that is all the data of the processed videos)
files <- fs::dir_ls(glob = "*.txt")

#with rbindlist() we will paste together the resulting data frame that the following code (the "function(x)") creates for each ".txt" file (x)

summary_data_final<-rbindlist(lapply(as.list(files), function(x){
  
  #x <- as.list(files)[[4]]   ## here you can just check if the loading is working by calling the first name of the list
  
  # we read the ComTrack data file x
  data<-fread(x) 

  #create variables of how many seconds the tracking lasted (to use later to calculate speed)
  tracking_duration<-video_duration*(max(data$Frame)-min(data$Frame))/max(data$Frame)
  
  #### THE FOLLOWING PART OF THE CODE DEPENDS ON HOW YOU NAME THE FILES OF THE DATA OF YOUR VIDEOS, is based on theour standard method of having a "_"#
  # separating the date components (e.g. years, month, day), the treatment (e.g. 3seeds or 2seeds) and the replicate of that treatment. And in case you have 
  #differet species, the name of the species
  
  #we split the name of the file (x) to obtain the treatment name, the replicate number, etc (make sure that the elements are separated by "_")
  split_name <- unlist(strsplit(x, split=c("_", "."))) 
  
  replicate<-gsub(".txt", "", split_name[[2]]) #take the xth element separated by the "_" and drop the ".txt"
  
  ##if we want to add date to have a singular dataframe with the time series we label like this:
  #species_name<- split_name[[6]] #take the second element before the "_"
  # treatment_name <- split_name[[8]]
  # date<-paste(split_name[3],split_name[2], split_name[1], sep = "/") 
  # hour<-paste(split_name[4],split_name[5], sep = ":")
  species_tested<-split_name[[1]]
  
  
  
  ## now we remove false detection (i.e. objects that were detected in less than 3 frames throughout the video, we discard them)
  filter_threshold_frames <- 3 #the threshold of detection across the video (e.g. 3 frames in this case, you can change it)
  
  #remove false detection
  sorted_data <- data %>% group_by(ID) %>% filter(n()> filter_threshold_frames) %>% ungroup()
  
  # if condition to continue the loop
  if (nrow(sorted_data) <= 2) { #we want more than two rows in the data frame

    print(paste(x,"no individuals tracked", sep = " ")) #let us know that no protists were traked in this video


    sorted_data<-sorted_data %>% add_row() %>% mutate_all(~replace(., is.na(.), 0)) # therefore create an empty dataframe for that date/video

    data_final<-sorted_data %>% mutate(
      # treatment = treatment_name,
      replicate = replicate,
      # date = date,
      # hour = hour,
      species_tested = species_tested
    )

    return(data_final)

  } else { #if protists are actually tracked in the videos...
    print(paste(x,"has individuals", sep = " ")) #let us know that
    
    ## the following bit of the code identifies the gap in the ID detection (i.e. the flickering of the ID assignment through the video) 
    # and takes it into account creating a new ID variable everytime an ID is not sub sequentially tracked in adjacent frames
    
    # #create a list with each sub dataframe for each ID and apply the function
    # gap_ID <- rbindlist(lapply(split(sorted_data, sorted_data$ID), function(y){
    #   #y<- split(sorted_data, sorted_data$ID)[[1]]
    #   counter <- 0
    #   y$Diff <- 0 #add a "Diff" column to the sub-dataframe
    #   for(i in 2:nrow(y)){
    #     if(y$Frame[i]-y$Frame[i-1] == 1){ #check if the difference between subsequent frame number in the rows is 1
    #       y$Diff[i] = counter}else{ #if is not add 1 to the counter
    #         counter<-counter+1
    #         y$Diff[i] = counter
    #       }
    #   }
    #   return(y)
    # }))
    
    # #create a new dataframe that has new ID based on if a particle has disappeared and then reappeared in the video (what we did right before)
    # filtered_gap_ID <- gap_ID %>% group_by(ID, Diff) %>% mutate(ID = cur_group_id()) %>% ungroup
    
    ##if you don't want to adjust for the flickering using the new ID we created above, you simply run the following line instead of the gap_ID 
    
    filtered_gap_ID<-sorted_data
    
    #from now on this "dataz" will be out data frame to go on
    dataz<-filtered_gap_ID
    
    #manipulate data to obtain a column with species name and a ID_probability column (easiest for analysis)
    dataz<-sorted_data %>% group_by(Frame,ID) %>% #group the data
      tidyr::pivot_longer(all_of(first_sp):all_of(last_sp), names_to = "Species",values_to = "Prob")  #pivot the data
    
    ### this is the data handling to obtain ABUNDANCE and morphological estimates 
    
    data_ab<- dataz %>%  ungroup() %>% #is good practice to ungroup before regrouping for new variables!
      mutate(time_s = ((Frame-min(Frame))/(((max(Frame)-min(Frame))/tracking_duration))),  ##create time column with "seconds" as a unit instead of frames
             CentroidX_mm = CentroidX/xscale, CentroidY_mm = CentroidY/yscale, ###scale  values of the particles centroids to mm instead of pixels
             Length_um = (Length/xscale)*1000, Width_um = (Width/yscale)*1000,  ##scale protists size to micro meters 
             Area_sqrd_um = (Area/area_scale)*1000000
      ) %>%  
      ungroup() %>% 
      group_by(ID, Species) %>% #now for each ID and each Species...
      mutate(average_p = mean(Prob), median_p = median(Prob)) %>% #create average p and median p column calculated across all frames of the video
      ungroup() %>% 
      group_by(Frame, ID) %>% #for each frame and ID
      filter(average_p == max(average_p)) %>% #we take only the highest average ID probs, we may also use max(median)
      #filter(median_p == max(median_p))
      group_by(Frame, Species) %>% #for each frame and each species... 
      mutate(abundance_frame = n()) %>% #create a column with the count of rows per Frame per species (i.e. how many ID of those species we have per frame)
      ungroup() %>% group_by(Species) %>% 
      #create a column with the max , mean and median abundance per species throughout the video + the same for body size measures
      mutate(max_abundance = max(abundance_frame), mean_abundance = mean(abundance_frame), median_abundance = median(abundance_frame)) %>% 
      ungroup() %>% 
      group_by(ID) %>%#for each ID tracked we want measures of the body size
      mutate( mean_width_um = mean(Width_um), median_width_um = median(Width_um),
              mean_length_um = mean(Length_um), median_length_um = median(Length_um),
              max_length_um = max(Length_um), max_width_um = max(Width_um),
              mean_area_sqrd_um = mean(Area_sqrd_um), median_area_sqrd_um = median(Area_sqrd_um))
    
    ## Now let's calculate speed of the protists using data.table
    ##turn data_ab into a data.table format
    data_ab.dt = as.data.table(data_ab)
    setorderv(data_ab.dt, c("ID","time_s")) # order by ID and time_s (formerly Frame)
    
    #operation to calculate speed
    data_ab.dt[      ##use all the dataframe
      , `:=`(        #create new columns, in particular...
        #colum deltaY with the difference between the horizontal position of each ID between two time steps
        deltaX = CentroidX_mm - shift(CentroidX_mm, 1L, type = "lag")
        #colum deltaY with the difference between the vertical position of each ID between two time steps
        , deltaY = CentroidY_mm - shift(CentroidY_mm, 1L, type = "lag")
        #diffence in time between two rows
        , deltaTime = time_s - shift(time_s, 1L, type = "lag")
      )
      , ID #do this for each ID
    ][
      , velocity := sqrt(deltaX^2 + deltaY^2)/deltaTime #calculate velocity
    ]
    
    data_ab_velocity<-data_ab.dt %>%ungroup() %>% group_by(ID) %>% #for each ID
      mutate(median_speed = median(velocity, na.rm =T),mean_speed = mean(velocity,na.rm =T)) #create column with mean and median speed throughout the video
    
    #finally, add all the information of the video to this dataframe 
    data_final<-data_ab_velocity %>% mutate(
      # treatment = treatment_name,
      replicate = replicate,
      # date = date,
      # hour = hour,
      species_tested = species_tested
    )
    
    return(data_final)
    
  }
  
}),fill = T)



##### CODE TO CHECK HOW THE PROBABLITIES ARE DOING THROUGHOUT THE VIDEO FOR EACH ID####

###Plot which species are the in the "data_ab" dataset, it will give us a quick look on how the model is doing (if we are processing 
# videos with just one species in it)

ggplot(data = data_ab, aes(x = Species, y = max_abundance, col = Species))+
  geom_point(size = 5)+
  theme_bw()


###plots to check probability of tracked objects and print list (we have to use the "pivoted longer" "dataz" data.frame (after LINE 146)
# before we do the selection of the max average probability)#####
IDs<-unique(dataz$ID)
myplots <- vector('list', length(IDs))

for (i in IDs) {
  message(i)
  myplots[[i+1]] <- local({
    i <- i
    p1<-ggplot(dataz %>% filter(ID == i), aes(y = Prob, x =  Frame, col = Species))+
      geom_point()+
      ggtitle(i)+
      theme_bw()
    p2<-ggplot(dataz %>% filter(ID == i), aes(y = Prob, x =  Species, col = Species))+
      geom_boxplot()+
      stat_summary(fun=mean, geom="point", 
                   size=2, show.legend=FALSE) + 
      theme_bw()
    
    p3<-ggarrange(p1,p2,  common.legend = T)
    
    
  })
}

pdf("probability_plots_ID_no_flickering_BS_Comm_5spp.pdf", onefile = TRUE, width = 12, height = 7)
print(myplots)  
dev.off()




#### At this point, you will have your "summary_data_final" dataframe, that should contain all the replicates and treatments ####
# with ID information for each video in a single big dataset
# we can put this dataframe in tibble version (more ggplot friendly) and do some final tweaks
summary_data_final<-as_tibble(summary_data_final) %>%
  mutate(date = lubridate::dmy(summary_data_final$date)) %>% #put the date in a readable format for R
  tidyr::unite(time_date, c(date,hour), sep = " ", remove = T) %>% 
  ungroup %>% 
  # add time column representing "time points of experiment, at the scale we want. In this case: hours
  mutate(time_point = as.numeric(difftime(time_date, min(time_date), units = "hours"))) 



######### Plotting to check species abundances, body size and speed extracted from video ############################
#put dataframe in tibble version (more ggplot friendly)
summary_data_final<-as_tibble(summary_data_final) %>%
  group_by(time_point,
           treatment,
           replicate,
           Species) %>% 
  mutate(time_point = as.numeric(time_point)) %>% #time point to be treated as a number
  filter(Species != 'NONpro',
  ) %>% #remove non protist particles 
  ungroup () # %>%


#### Now let's clean that dataset from potential outliers using quantile distributions of body size and speed measurements for each species ####

summary_data_percentiles <- summary_data_final %>%
  group_by(treatment, Species) %>% 
  #remove the most extreme values (below 1% and above 99%)
  #only doing this for the variables I'm interested in, and recalculate the mean values
  filter(velocity > quantile(velocity, c(0.01), na.rm = T) & velocity < quantile(velocity, c(0.99), na.rm = T),
         Width_um > quantile(Width_um, c(0.01), na.rm = T) & Width_um < quantile(Width_um, c(0.99), na.rm = T),
         max_length_um > quantile(max_length_um, c(0.01), na.rm = T) & max_length_um < quantile(max_length_um, c(0.99), na.rm = T),
         Area_sqrd_um > quantile(Area_sqrd_um, c(0.01), na.rm = T) & Area_sqrd_um < quantile(Area_sqrd_um, c(0.99), na.rm = T)) %>% 
  ungroup() %>% group_by(treatment,replicate, time_point, Species, ID) %>% 
  mutate(mean_speed = mean(velocity),median_speed = median(velocity),
         mean_width_um = mean(Width_um), median_width_um = median(Width_um),
         mean_length_um = mean(Length_um), median_length_um = median(Length_um),
         max_length_um = max(Length_um), max_width_um = max(Width_um),
         mean_area_sqrd_um = mean(Area_sqrd_um), median_area_sqrd_um = median(Area_sqrd_um)) %>% 
  group_by(treatment,replicate, time_point, Species, Frame) %>% 
  mutate(abundance_frame = n()) %>% group_by(treatment,replicate, time_point, Species) %>% 
  mutate(max_abundance = max(abundance_frame)) 

# let's call the final dataset to work with...
data_comtrack<-summary_data_percentiles


