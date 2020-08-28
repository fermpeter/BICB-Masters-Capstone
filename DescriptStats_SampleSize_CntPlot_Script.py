# -*- coding: utf-8 -*-
"""
Created on Fri Nov  1 10:48:10 2019

@author: fermx014

"""

# Install packages on Anoconda Prompt -- pip install package
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import seaborn as sns
import math as m



#                       --SAMPLE SIZE--

#                         --Reminder--
# Sample size referred to Dataset 2 in report.

#                       --IMPORT DATASET--

# Read-in sample size (used for Miki's analysis) into a dataframe
df_sampleSize_clinicalChars = pd.read_excel('SampleSize_Miki.xlsx', sheet_name = 'supervisedData')

# Store sample size clinical avatar total count
cnt_sampleSize_clinicalChars = len(df_sampleSize_clinicalChars)


#------------------------------------------------------------------------------

#                       --DATA PROCESSING--

# Convert numerical values representing categories to qualitatvie str values to stay consistent with Population size dataset 
# Change binary numeric values to str values stored in new columns of df
df_sampleSize_clinicalChars['Gender'] = np.where(df_sampleSize_clinicalChars['GENDER'] == 1, '"M"', '"F"')
df_sampleSize_clinicalChars['Amiodorane_status'] = np.where(df_sampleSize_clinicalChars['AMI'] == 1, '"Y"', '"N"')
df_sampleSize_clinicalChars['Smoker_status'] = np.where(df_sampleSize_clinicalChars['SMOKER'] == 1, '"Y"', '"N"')
 
# Set different age categories 
cutOff_points_age = [0,64.99,103]
# Set different ttrIn categories 
cutOff_points_ttrIn = [-1,74.99,101]

# Age category element values
label_names_age = ['18-64', '65+'] 
# ttrIn category element values
label_names_ttrIn = ['<75', '>=75'] 

# Use pandas cut method to set age categories
df_sampleSize_clinicalChars['Age_categories'] = pd.cut(df_sampleSize_clinicalChars['AGE'], cutOff_points_age, labels = label_names_age)
# Use pandas cut method to set ttrIn categories
df_sampleSize_clinicalChars['TTR'] = pd.cut(df_sampleSize_clinicalChars['ttrIn'], cutOff_points_ttrIn, labels = label_names_ttrIn)




# Creating new column to store BMI categories
df_sampleSize_clinicalChars['BMI_categories'] = ''
# Iterate through BMI continous column to code different BMI categories 
for i,v in df_sampleSize_clinicalChars['BMI'].items():
    if (v < 18.5):
        df_sampleSize_clinicalChars['BMI_categories'].values[i] = 'Underweight'
    elif (v >= 18.5 and v <=25):
        df_sampleSize_clinicalChars['BMI_categories'].values[i] = 'Normal'
    elif (v > 25 and v <= 30):
            df_sampleSize_clinicalChars['BMI_categories'].values[i] = 'Overweight'
    elif (v > 30):
        df_sampleSize_clinicalChars['BMI_categories'].values[i] = 'Obese'
        

# Creating new column to store Race categories
df_sampleSize_clinicalChars['Race'] = ''
# Iterate through RACE numeric column to code different Race categories 
for i,v in df_sampleSize_clinicalChars['RACE'].items():
    if (v == 1):
       df_sampleSize_clinicalChars['Race'].values[i] = '"Asian"'
    elif (v == 2):
       df_sampleSize_clinicalChars['Race'].values[i] = '"American Indian or Alaskan Native"'  
    elif (v == 3):
        df_sampleSize_clinicalChars['Race'].values[i] = '"White"'
    elif (v == 4):
        df_sampleSize_clinicalChars['Race'].values[i] = '"Black or African American"'
        

# Creating new column to store CYP2C9_variants categories
df_sampleSize_clinicalChars['CYP2C9_variants'] = ''
# Iterate through CYP2C9 numeric column to code different Race categories 
for i,v in df_sampleSize_clinicalChars['CYP2C9'].items():
    if (v == 1):
       df_sampleSize_clinicalChars['CYP2C9_variants'].values[i] = '"*2/*3"'
    elif (v == 2):
       df_sampleSize_clinicalChars['CYP2C9_variants'].values[i] = '"*2/*2"'
    elif (v == 3):
        df_sampleSize_clinicalChars['CYP2C9_variants'].values[i] = '"*1/*3"'
    elif (v == 4):
        df_sampleSize_clinicalChars['CYP2C9_variants'].values[i] = '"*1/*2"'
    elif (v == 5):
        df_sampleSize_clinicalChars['CYP2C9_variants'].values[i] = '"*1/*1"'
        

# Creating new column to store VKORC1G_variants categories
df_sampleSize_clinicalChars['VKORC1G_variants'] = ''
# Iterate through VKORC1G numeric column to code different Race categories 
for i,v in df_sampleSize_clinicalChars['VKORC1G'].items(): 
    if (v == 1):
       df_sampleSize_clinicalChars['VKORC1G_variants'].values[i] = '"A/A"'
    elif (v == 2):
       df_sampleSize_clinicalChars['VKORC1G_variants'].values[i] = '"G/A"'
    elif (v == 3):
        df_sampleSize_clinicalChars['VKORC1G_variants'].values[i] = '"G/G"'

#------------------------------------------------------------------------------

#          --DATA VISUALIZATION AND EXPLORATION--
#                   --SAMPLE SIZE--


# Function computes percentage of a number
def percent_of(number, percentage): 
    # Compute percentage of number
    p = number * percentage
    
    # Return percentage of number 
    return p

# Function to round a number half down
def round_half_up(n, decimals=0):
    multiplier = 10 ** decimals
    return m.floor(n*multiplier + 0.5) / multiplier

# Function to round half away from zero
def round_half_away_from_zero(n, decimals=0):
    rounded_abs = round_half_up(abs(n), decimals)
    return m.copysign(rounded_abs, n)


# Function to create twin axes for counts a percent for countplot 
def twin_axes(ax, df_len):   
    # Make twin axis
    ax2=ax.twinx()
    
    # Set ylabel names
    ax.set_ylabel('Count', fontsize = 24)
    ax2.set_ylabel('Percentage [%]', fontsize = 24)
    
    # Set xlabel font size
    ax.set_xticklabels(ax.get_xticklabels(), fontsize= 14, rotation = 15, ha = 'right')
    
    # Intitialize percentage of df for placing annotations
    ten_percent_of_df = percent_of(df_len, .10)
    eight_percent_of_df = percent_of(df_len, .80)
    ninety_percent_of_df = percent_of(df_len, .90)
    seventy_percent_of_df = percent_of(df_len, .70)
    
    # Get percent to label bars
    for p in ax.patches:
        x=p.get_bbox().get_points()[:,0]
        y=p.get_bbox().get_points()[1,1]
        # Annotations of counts and percent based on bar heights
        if(y < ten_percent_of_df):
            ax.annotate('{}%'.format(round_half_away_from_zero((100.*y/df_len), 3)), (x.mean(), y+ten_percent_of_df), weight = 'bold', 
                ha='center', va='bottom', fontsize = 10)
        elif(y > ninety_percent_of_df):
            ax.annotate('{}%'.format(round_half_away_from_zero((100.*y/df_len), 3)), (x.mean(), eight_percent_of_df), color = 'white', weight = 'bold', 
                ha='center', va='bottom', fontsize = 10)
        else:
            ax.annotate('{}%'.format(round_half_away_from_zero((100.*y/df_len), 3)), (x.mean(), y), weight = 'bold', 
                ha='center', va='bottom', fontsize = 10)
                        
    # Get counts to label bars        
    for p in ax.patches:
        x=p.get_bbox().get_points()[:,0]
        y=p.get_bbox().get_points()[1,1]
        # Annotations of counts and percentages based on bar heights
        if(y < ten_percent_of_df):
            ax.annotate('{}'.format(int(y)), (x.mean(), y), weight = 'bold',
                ha='center', va='bottom', fontsize = 10)
        elif(y > ninety_percent_of_df):
             ax.annotate('{}'.format(int(y)), (x.mean(), seventy_percent_of_df), color ='white', weight = 'bold', 
                ha='center', va='bottom', fontsize = 10)
        else:
            ax.annotate('{}'.format(int(y)), (x.mean(), y-ten_percent_of_df), color = 'white', weight = 'bold',
                ha='center', va='bottom', fontsize = 10)
                
    # Use a LinearLocator to ensure the correct number of ticks
    ax.yaxis.set_major_locator(ticker.LinearLocator(11))
    
    # Set the percent range to 0-100
    ax2.set_ylim(0,100)
    # Set the count range to dataset size
    ax.set_ylim(0,df_len)
    
    # Use a MultipleLocator to ensure a tick spacing of 10
    ax2.yaxis.set_major_locator(ticker.MultipleLocator(10))
    
    # Need to turn the grid on ax2 off, otherwise the gridlines end up on top of the bars
    ax2.grid(None)

# Sample size df columns to be used for subplots
df_sampleSize_clinicalCharsVisual = df_sampleSize_clinicalChars[['Gender', 'Smoker_status', 'Amiodorane_status', 'Race'
                                                                                      , 'Age_categories', 'BMI_categories', 
                                                                                      'CYP2C9_variants', 'VKORC1G_variants']]

# Intialize axes of subplots
rowCnt = len(df_sampleSize_clinicalCharsVisual.columns) 
colCnt = 4
subCnt = 1 # Initialize subplot counter

# Plot settings
fig = plt.figure(figsize=(30,60))
sns.set_style('darkgrid')
sns.set(font_scale = 1.7)
fig.subplots_adjust(hspace=0.5, wspace=0.5)

# Sample size subplots for loop
for i in df_sampleSize_clinicalCharsVisual.columns: 
    # Add first subplot in axis pos
    fig.add_subplot(rowCnt, colCnt, subCnt)
    
    # Create countplot sample size clinical characteristics
    ax_sampleSize_clinicalChars = sns.countplot(df_sampleSize_clinicalCharsVisual[i], palette = 'deep', order = df_sampleSize_clinicalCharsVisual[i].value_counts(ascending=True).index )
    
    # Plot xlabels
    plt.xlabel(i, fontsize = 22)
    
    # Function call to create twin axes for subplots
    twin_axes(ax_sampleSize_clinicalChars, cnt_sampleSize_clinicalChars)
    
    # Adjust subplots to fit into figure
    fig.tight_layout()

    # Increment subplot counter
    subCnt = subCnt + 1

















