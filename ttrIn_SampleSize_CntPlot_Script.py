# -*- coding: utf-8 -*-
"""
Created on Tue Mar 31 16:25:28 2020

@author: Peter
"""


# Install packages on Anoconda Prompt -- pip install package
import pandas as pd
import seaborn as sns

#                       --SAMPLE SIZE--

#                       --IMPORT DATASET--

# Read-in Sample size (used for Miki's analysis) into a dataframe 
df_sampleSize = pd.read_excel('SampleSize_Miki.xlsx', sheet_name = 'EntireData') #EntireData sheet where all 5 protocols are represented for each avatar (800X5 =4000)


# Store sample size clinical avatar total count
cnt_sampleSize = len(df_sampleSize)
# Store sample size clinical avatar total count per protocol
cnt_sampleSize_perProtocol = len(df_sampleSize)/5

#------------------------------------------------------------------------------


#                       --DATA PROCESSING--

# Convert numerical values representing categories to qualitatvie str values to stay consistent with Population size dataset
# Change binary numeric values to str values stored in new columns of df

# Set different age categories 
cutOff_points_age = [0,64.99,103]
# Set different ttrIn categories 
cutOff_points_ttrIn = [-1,74.99,101]

# Age category element values
label_names_age = ['18-64', '65+'] 
# ttrIn category element values
label_names_ttrIn = ['<75', '>=75'] 

# Use pandas cut method to set age categories
df_sampleSize['Age_categories'] = pd.cut(df_sampleSize['AGE'], cutOff_points_age, labels = label_names_age)
# Use pandas cut method to set ttrIn categories
df_sampleSize['TTR'] = pd.cut(df_sampleSize['ttrIn'], cutOff_points_ttrIn, labels = label_names_ttrIn)

# Create new column Protocol to change column name
df_sampleSize['Protocol'] = df_sampleSize['OPTIMAL PROTOCOL'] 

#Creating new column to store BMI categories
df_sampleSize['BMI_categories'] = ''
# Iterate through BMI continous column to code different BMI categories 
for i,v in df_sampleSize['BMI'].items():
    if (v < 18.5):
        df_sampleSize['BMI_categories'].values[i] = 'Underweight'
    elif (v >= 18.5 and v <=25):
        df_sampleSize['BMI_categories'].values[i] = 'Normal'
    elif (v > 25 and v <= 30):
            df_sampleSize['BMI_categories'].values[i] = 'Overweight'
    elif (v > 30):
        df_sampleSize['BMI_categories'].values[i] = 'Obese'
        

#------------------------------------------------------------------------------
        
#           --DATA VISUALIZATION AND EXPLORATION--
#                   --SAMPLE SIZE--
        

# Sample size df columns to be used for count plots
df_sampleSize_visual = df_sampleSize[['Protocol','Age_categories', 'BMI_categories', 'TTR']]
# Plot settings
sns.set_style('darkgrid')
sns.set(font_scale=1.5)
order = ['PGPGA','CAA','PGAA', 'PGPGI', 'AAA']



# Count plots by protocol where age sub-groups are in or out of theraputic range 
cat_sampleSize_ttrAgePro = sns.catplot(x='Age_categories', hue='TTR', col ='Protocol', data=df_sampleSize_visual, kind='count', height=5, aspect=.8, palette = 'deep')

# Count plots by protocol where BMI sub-groups are in or out of theraputic range 
cat_sampleSize_ttrBmiPro = sns.catplot(x='BMI_categories', hue='TTR', col='Protocol', row_order = order, data=df_sampleSize_visual, kind='count', height=5, aspect=.8, palette = 'deep')
# Set xlabel font size
cat_sampleSize_ttrBmiPro.set_xticklabels(rotation=65, horizontalalignment='right')

# Count plots by protocol where that are in or out of theraputic range 
cat_sampleSize_ttrPro = sns.catplot(x='TTR', col='Protocol', data=df_sampleSize_visual, kind='count', height=5, aspect=.8, palette = 'deep')



