

# -*- coding: utf-8 -*-
"""
Created on Tue Mar 31 16:25:28 2020

@author: Peter
"""


# Install packages on Anoconda Prompt -- pip install package
import regex as re
import pandas as pd
import seaborn as sns


#                       --STUDY POPULATION ANALYSIS--

#                       --IMPORT DATASET--

# Open input file 
inFile = open("AHC_RESULTS.txt", "r")

# Read-in first line (column header)
columnHeaders = inFile.readline()

# Read-in all the Clinical Avatar data
container = []
for line in inFile:
   container.append(line)
        
# Regex functions/pattern to match and capture 30day period results
# Regex for  90day period results -- r'"[A-Z]+"\|"90Day"\|.*'
pattern = re.compile(r'"[A-Z]+"\|"30Day"\|.*')

# Container to store lines with 30day periods
thirtyDay_container = list(filter(pattern.match, container))

# Intialize containers (lists) to hold 30day period results 
protocol_col = []
age_col = []
BMI_col = []
ttrIN_col = []

# 30day period
for lines in thirtyDay_container:  
    # Strip of new line chars
    lines = lines.rstrip("\n")
    
    # Seperate file by pipes to parse out columns
    pipe_lines = lines.split(sep = "|")
   
    # Append parsed columns to seperate lists 
    protocol_col.append(pipe_lines[0])
    age_col.append(pipe_lines[4])
    BMI_col.append(pipe_lines[16])
    ttrIN_col.append(pipe_lines[17]) 

 
# Close input file 
inFile.close()

#------------------------------------------------------------------------------

#                       --DATA PROCESSING--

#                         --Reminders:--
# Send a copy of lists to preserve original datq b/c a list is a mutable data structure.
# Divide counts by 5 to account for the each clinical avatar i.e. 1,478,930 of them represented in the 5 different warfarin protocols
# Divide percentages by total of clinical avatars i.e. 1,478,930 of them

# Copy lists and covert to needed data types
protocol_copy_list = protocol_col.copy()
BMI_list_copy_float = [float(i) for i in BMI_col]
age_list_copy_float = [float(i) for i in age_col]
ttrIn_list_copy_float = [float(i) for i in ttrIN_col]

# Store Study Population clinical avatar total count
clinical_avatar_count = len(protocol_copy_list)/5


# Empty container to store new BMI category str values
BMI_Categories = []
# Iterate through BMI list to code different BMI categories 
for i in BMI_list_copy_float:
    if (i < 18.5):
        BMI_Categories.append('Underweight')
    elif (i >= 18.5 and i <=25):
        BMI_Categories.append('Normal')
    elif (i > 25 and i <= 30):
        BMI_Categories.append('Overweight')
    elif (i > 30):
        BMI_Categories.append('Obese')
        

# Function to convert list to Series
def series_ttrInOut(list_name):
    # Create series of Study Population total number of clinical avatars (i.e. not all 5 protocol simulations)
    s = pd.Series(list_name)
    # Return the series
    return s
    
# Call of series function for Study Population 
s_protocol = series_ttrInOut(protocol_copy_list)
s_ttrIn =  series_ttrInOut(ttrIn_list_copy_float)
s_age = series_ttrInOut(age_list_copy_float)
s_BMI = series_ttrInOut(BMI_list_copy_float)
s_BMI_cat = series_ttrInOut(BMI_Categories)  


# Concatenate series to a dataframe
df_studyPop_ttrInOut = pd.concat([s_protocol, s_ttrIn, s_age, s_BMI, s_BMI_cat], axis = 1)

# Column names
df_studyPop_ttrInOut.columns = ['Protocol', 'ttrIn', 'Age', 'BMI', 'BMI_categories']

# Total count of clincal avatars
cnt_df_studyPop_ttrInOut = len(df_studyPop_ttrInOut)/5

# Set different age categories 
cutOff_points_age = [0,64.99,103]
# Set different ttrIn categories 
cutOff_points_ttrIn = [-1,74.99,101]

# Age category element values
label_names_age = ['18-64', '65+'] 
# ttrIn category element values
label_names_ttrIn = ['<75', '>=75'] 

# Use pandas cut method to set age categories
df_studyPop_ttrInOut['Age_categories'] = pd.cut(df_studyPop_ttrInOut['Age'], cutOff_points_age, labels = label_names_age)
# Use pandas cut method to set ttrIn categories
df_studyPop_ttrInOut['TTR'] = pd.cut(df_studyPop_ttrInOut['ttrIn'], cutOff_points_ttrIn, labels = label_names_ttrIn)

#------------------------------------------------------------------------------
           
#          --DATA VISUALIZATION AND EXPLORATION--
#                  --Study Population--  


# Study populatuon df columns to be used for count plots
df_studyPop_visual = df_studyPop_ttrInOut[['Protocol','Age_categories', 'BMI_categories', 'TTR']]
# Plot settings
sns.set_style('darkgrid')
sns.set(font_scale=1.5)

# Count plots by protocol where age sub-groups are in or out of theraputic range 
cat_studyPop_ttrAgePro = sns.catplot(x='Age_categories', hue='TTR', col='Protocol', data=df_studyPop_visual, kind='count', height=5, aspect=.8, palette = 'colorblind' )

# Count plots by protocol where BMI sub-groups are in or out of theraputic range 
cat_studyPop_ttrBmiPro = sns.catplot(x='BMI_categories', hue='TTR', col='Protocol', data=df_studyPop_visual, kind='count', height=5, aspect=.8, palette = 'colorblind')
# Set xlabel font size for BMI count plots 
cat_studyPop_ttrBmiPro.set_xticklabels(rotation=65, horizontalalignment='right')

# Count plots by protocol where that are in or out of theraputic range 
cat_studyPop_ttrPro = sns.catplot(x='TTR', col='Protocol', data=df_studyPop_visual, kind='count', height=5, aspect=.8, palette = 'colorblind')



