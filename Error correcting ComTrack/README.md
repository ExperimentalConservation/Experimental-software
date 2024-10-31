# ComTrack Secondary Classifier predictions

#### 2024-10-16
#### Repository created by John Jackson

---

This repository is to enable species predictions to be made from the ComTrack pipeline, particularly for protist community experiments. 
The goal of the secondary classifier is to take species percentages from the ComTrack output, as well as morphological and behavioural features estimated
at the frame level, and consolidate this information to get a best guess of the species when taking all information together.

For this, we use a **random forest classification model**.

### Step 1. Adding your ComTrack data to the `data/data_to_predict/` folder

The first step for new predictions is to create yourself a new folder in the `data/data_to_predict/` folder, which describes the use case for your 
particular experiment. The data in here should be the raw text file outputs from Comtrack. There should be some form of replicate level information from
the file names, from which we can extract and specify in the final prediction data (which gets combined with `rbind`).

### Step 2. Work through the `random_forest_classifier_prediction.R` script

The main workhorse here is the `random_forest_classifier_prediction.R` script, which takes the ground-truthed data annotated by Francesco, and runs the Random Forest classifier on this data.
Then, using parameters that you set that are specific to your use case (your data folder and species included etc), the last step is to make predictions for your videos. 

The script is an annotated template to tell you what to do. Please modify the script with your specific information and save it in the `scripts/` folder, to keep the template unchanged.

### Step 3. Access your predictions in `output/`

Run the script through with your parameters and save the output of this, which will be in the `output/` folder, making sure that you create an empty folder (with same name as in the `data_to_predict/` folder)
