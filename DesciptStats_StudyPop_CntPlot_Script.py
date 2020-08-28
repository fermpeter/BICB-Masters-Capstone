 # -*- coding: utf-8 -*-
"""
Created on Fri Nov  1 10:48:10 2019

@author: fermx014

"""

# Install packages on Anoconda Prompt -- pip install package
import regex as re
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import seaborn as sns
import math as m


#                       --STUDY POPULATION--


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
# Regex for 90day period results -- r'"[A-Z]+"\|"90Day"\|.*'
pattern = re.compile(r'"[A-Z]+"\|"30Day"\|.*')

# Container to store lines with 30day periods
thirtyDay_container = list(filter(pattern.match, container))

# Intialize containers (lists) to hold 30day period results 
protocol_col = []
period_col = [] 
id_col = []
gender_col = []
age_col = []
race_col = []
smoker_col = []
AMI_col = []
CYP2C9_col = []
VKORC1G_col = []
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
    period_col.append(pipe_lines[1])
    id_col.append(pipe_lines[2])
    gender_col.append(pipe_lines[3])
    age_col.append(pipe_lines[4])
    race_col.append(pipe_lines[5])
    smoker_col.append(pipe_lines[8]) 
    AMI_col.append(pipe_lines[9]) 
    CYP2C9_col.append(pipe_lines[12]) 
    VKORC1G_col.append(pipe_lines[13]) 
    BMI_col.append(pipe_lines[16])
    ttrIN_col.append(pipe_lines[17]) 

 
# Close input file 
inFile.close()

#------------------------------------------------------------------------------

#                       --DATA PROCESSING--

#                         --Reminders--
# Study Population referred to Dataset 1 in report.
# Send a copy of lists to preserve original data b/c a list is a mutable data structure.

# Copy lists and covert to needed data types
protocol_copy_list = protocol_col.copy()
gender_copy_list = gender_col.copy()
smoker_copy_list = smoker_col.copy()
AMI_copy_list = AMI_col.copy()
race_copy_list = race_col.copy()
CYP2C9_copy_list = CYP2C9_col.copy()
VKORC1G_copy_list = VKORC1G_col.copy()

BMI_list_copy_float = [float(i) for i in BMI_col]
age_list_copy_float = [float(i) for i in age_col]
ttrIn_list_copy_float = [float(i) for i in ttrIN_col]

# Store Study Population clinical avatar total count
clinical_avatar_count = len(protocol_copy_list)/5


# Function to convert list to Series
def series_clinicalChars(list_name):
    # Create series of Study Population total number of clinical avatars (i.e. not all 5 protocol simulations)
    s = pd.Series(list_name[0:1478930])
    
    # Return the series
    return s
    
# Call of series function for Study Population 
s_protocol = series_clinicalChars(protocol_copy_list)
s_ttrIn =  series_clinicalChars(ttrIn_list_copy_float)
s_age = series_clinicalChars(age_list_copy_float)
s_BMI = series_clinicalChars(BMI_list_copy_float)   
s_gender = series_clinicalChars(gender_copy_list)  
s_smoker = series_clinicalChars(smoker_copy_list)
s_AMI = series_clinicalChars(AMI_copy_list)
s_race = series_clinicalChars(race_copy_list)
s_CYP2C9 = series_clinicalChars(CYP2C9_copy_list)
s_VKORC1G = series_clinicalChars(VKORC1G_copy_list)

# Concatenate series to a dataframe
df_studyPop_clinicalChars = pd.concat([s_protocol, s_ttrIn, s_age, s_BMI, s_gender, s_smoker, s_AMI, s_race, s_CYP2C9, s_VKORC1G], axis = 1)
# Column names
df_studyPop_clinicalChars.columns = ['Protocol', 'ttrIn', 'Age', 'BMI', 'Gender', 'Smoker_status', 'Amiodorane_status', 'Race', 'CYP2C9_variants', 'VKORC1G_variants']

# Total length of df i.e. total count of clinical avatars
cnt_studyPop_clinicalChars = len(df_studyPop_clinicalChars)

# Set different age categories 
cutOff_points_age = [0,64.99,103]
# Set different ttrIn categories 
cutOff_points_ttrIn = [-1,74.99,101]

# Age category element values
label_names_age = ['18-64', '65+'] 
# ttrIn category element values
label_names_ttrIn = ['<75', '>=75'] 

# Use pandas cut method to set age categories
df_studyPop_clinicalChars['Age_categories'] = pd.cut(df_studyPop_clinicalChars['Age'], cutOff_points_age, labels = label_names_age)
# Use pandas cut method to set ttrIn categories
df_studyPop_clinicalChars['TTR'] = pd.cut(df_studyPop_clinicalChars['ttrIn'], cutOff_points_ttrIn, labels = label_names_ttrIn)


# Creating new column to store BMI categories
df_studyPop_clinicalChars['BMI_categories'] = ''
# Iterate through BMI continuous columns to code different BMI categories 
for i,v in df_studyPop_clinicalChars['BMI'].items():
    if (v < 18.5):
        df_studyPop_clinicalChars['BMI_categories'].values[i] = 'Underweight'
    elif (v >= 18.5 and v <=25):
        df_studyPop_clinicalChars['BMI_categories'].values[i] = 'Normal'
    elif (v > 25 and v <= 30):
        df_studyPop_clinicalChars['BMI_categories'].values[i] = 'Overweight'
    elif (v > 30):
        df_studyPop_clinicalChars['BMI_categories'].values[i] = 'Obese'

#------------------------------------------------------------------------------

#         --DATA VISUALIZATION AND EXPLORATION--
#                --STUDY POPULATION--


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


# Function to create twin axes for counts and percents for countplot 
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


# Study Population df columns to be used for subplots
df_studyPop_clinicalCharsVisual = df_studyPop_clinicalChars[['Gender', 'Smoker_status', 'Amiodorane_status', 'Race', 'Age_categories', 'BMI_categories', 'CYP2C9_variants', 'VKORC1G_variants']]


# Intialize axes of subplots
rowCnt = len(df_studyPop_clinicalCharsVisual.columns) 
colCnt = 4
subCnt = 1 # Initialize subplot counter

# Plot settings
fig = plt.figure(figsize=(30,60))
sns.set_style('darkgrid')
sns.set(font_scale = 1.7)
fig.subplots_adjust(hspace=0.5, wspace=0.5)



# Study Population subplots for loop
for i in df_studyPop_clinicalCharsVisual.columns: 
    # Add first subplot in axis positions  
    fig.add_subplot(rowCnt, colCnt, subCnt)
    
    # Create countplot Study Population clinical characteristics
    ax_studyPop_clinicalChars = sns.countplot(df_studyPop_clinicalCharsVisual[i], palette = 'colorblind', order = df_studyPop_clinicalCharsVisual[i].value_counts(ascending=True).index)
    
    # Plot xlabels
    plt.xlabel(i, fontsize = 25)
    
    # Function call to create twin axes for subplots
    twin_axes(ax_studyPop_clinicalChars, cnt_studyPop_clinicalChars)
    
    # Adjust subplots to fit into figure
    fig.tight_layout()
    
    # Increment subplot counter
    subCnt = subCnt + 1


