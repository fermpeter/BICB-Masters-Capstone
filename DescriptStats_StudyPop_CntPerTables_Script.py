 # -*- coding: utf-8 -*-
"""
Created on Fri Nov  1 10:48:10 2019

@author: fermx014

"""

# Install packages on Anoconda Prompt -- pip install package
import regex as re
import numpy as np
import tabulate as tb


#                       --STUDY POPULATION--


#                       --IMPORT DATASET--

# Open input file -- "AHC_RESULTS.txt"
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

 
# Close input file -- "AHC_RESULTS.txt"
inFile.close()

#------------------------------------------------------------------------------

#                       --DATA PROCESSING--

#                          --Reminders--
# Study Population referred to Dataset 1 in report.
# Send a copy of lists to preserve original data b/c a list is a mutable data structure.
# Divide counts by 5 to account for the each clinical avatar i.e. 1,478,930 of them represented in the 5 different warfarin protocols
# Divide percentages by total of clinical avatars i.e. 1,478,930 of them

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


#                       --DATA VISUALIZATION AND EXPLORATION--


# Function to aggregate counts and compute frequencies
def thirtyDay_lists_counts_percents(list_name, element_str):
    # Count number of passed in element string and divide by 5 to account for the 5 different warfarin protocols
    element_count = int(list_name.count(element_str)/5)
    
    # Find percentage, round to tenth decimal place and divide by the number of clinical avatars in each protocol
    element_percent = np.round(element_count/clinical_avatar_count*100, 1)
    
    # Return element counts and percentages
    return [element_count, element_percent]


# Function call of results for the counts and percentages of the clinical avatars demographics and genetics columns
  
# Gender list element counts and percentages
male_results = thirtyDay_lists_counts_percents(gender_copy_list, '"M"') 
female_results = thirtyDay_lists_counts_percents(gender_copy_list, '"F"')  

# Smoker list element counts and percentages
smoker_yes_results = thirtyDay_lists_counts_percents(smoker_copy_list, '"Y"') 
smoker_no_results = thirtyDay_lists_counts_percents(smoker_copy_list, '"N"')

# AMI list element counts and percentages
AMI_yes_results = thirtyDay_lists_counts_percents(AMI_copy_list, '"Y"')
AMI_no_results = thirtyDay_lists_counts_percents(AMI_copy_list, '"N"')

# Race list element counts and percentages
Asian_results = thirtyDay_lists_counts_percents(race_copy_list, '"Asian"')
AmericanIndian_AlaskaNative_results = thirtyDay_lists_counts_percents(race_copy_list, '"American Indian or Alaskan Native"')
White_results = thirtyDay_lists_counts_percents(race_copy_list, '"White"')
Black_results = thirtyDay_lists_counts_percents(race_copy_list, '"Black or African American"')
Native_Hawaii_results = thirtyDay_lists_counts_percents(race_copy_list, '"Native Hawaiian/Other Pacific Islander"')

# CYP2C9 variations list counts and percentages
one_one_results = thirtyDay_lists_counts_percents(CYP2C9_copy_list, '"*1/*1"')
one_two_results = thirtyDay_lists_counts_percents(CYP2C9_copy_list, '"*1/*2"')
one_three_results = thirtyDay_lists_counts_percents(CYP2C9_copy_list, '"*1/*3"')
two_two_results = thirtyDay_lists_counts_percents(CYP2C9_copy_list, '"*2/*2"')
two_three_results = thirtyDay_lists_counts_percents(CYP2C9_copy_list, '"*2/*3"')

# VKORC1 variations list element counts and percentages 
AA_results = thirtyDay_lists_counts_percents(VKORC1G_copy_list, '"A/A"')
GA_results = thirtyDay_lists_counts_percents(VKORC1G_copy_list, '"G/A"')
GG_results = thirtyDay_lists_counts_percents(VKORC1G_copy_list, '"G/G"')

#------------------------------------------------------------------------------

# Forming BMI list into categories

# BMI category list comprehensions to create lists of BMI categories
# Under
BMI_under = [BMI_measure for BMI_measure in BMI_list_copy_float if BMI_measure < 18.5]
# Normal
BMI_normal = [BMI_measure for BMI_measure in BMI_list_copy_float if BMI_measure >= 18.5 and BMI_measure <= 25]
# Over
BMI_over = [BMI_measure for BMI_measure in BMI_list_copy_float if BMI_measure > 25 and BMI_measure <= 30]
# Obese
BMI_obese = [BMI_measure for BMI_measure in BMI_list_copy_float if BMI_measure > 30]


# Count the number of avatars in each BMI category

# Under
BMI_under_count = int(len(BMI_under)/5)
# Normal
BMI_normal_count = int(len(BMI_normal)/5)
# Over
BMI_over_count = int(len(BMI_over)/5)
# Obese
BMI_obese_count = int(len(BMI_obese)/5)


# Compute percentage of each BMI category

# Under
BMI_under_percent = np.round(BMI_under_count/clinical_avatar_count*100, 1)
# Normal
BMI_normal_percent = np.round(BMI_normal_count/clinical_avatar_count*100, 1)
# Over
BMI_over_percent = np.round(BMI_over_count/clinical_avatar_count*100, 1)
# Obese 
BMI_obese_percent = np.round(BMI_obese_count/clinical_avatar_count*100, 1)

# BMI list aggregation statistics

# Mean of BMI list 
BMI_mean = np.round(np.mean(BMI_list_copy_float),1)

# Standard deviation of BMI list
BMI_stdDev = np.round(np.std(BMI_list_copy_float),1)

# Median of age list
BMI_median= np.round(np.median(BMI_list_copy_float),1)

# Max value in age list
BMI_max = np.round(np.max(BMI_list_copy_float), 1)

# Min value in age list
BMI_min = np.round(np.min(BMI_list_copy_float), 1)

# 25th quantile in age list 
BMI_25_quantile = np.round(np.percentile(BMI_list_copy_float, 25), 1)

# 75th quantile in age list
BMI_75_quantile = np.round(np.percentile(BMI_list_copy_float, 75), 1)

#------------------------------------------------------------------------------

# Forming age list into categories

# Age list comprehensions 
# 18-64
age_eighteen_sixtyFour = [age for age in age_list_copy_float if age >= 18 and age < 65]
# 65+
age_sixtyFive_plus = [age for age in age_list_copy_float if age >= 65]


# Count the number of avatars in each age category
# 18-64
age_eighteen_sixtyFour_count = int(len(age_eighteen_sixtyFour)/5)
# 65+
age_sixtyFive_plus_count = int(len(age_sixtyFive_plus)/5)

# Compute percentage of each age category 
# 18-64
age_eighteen_sixtyFour_percent = np.round(age_eighteen_sixtyFour_count/clinical_avatar_count*100, 1)
# 65+ 
age_sixtyFive_plus_percent = np.round(age_sixtyFive_plus_count/clinical_avatar_count*100, 1)
    
# Age list aggregation statistics

# Mean of age list 
age_mean = np.round(np.mean(age_list_copy_float), 1)

# Standard deviation of age list
age_stdDev = np.round(np.std(age_list_copy_float), 1)

# Median of age list
age_median= np.median(age_list_copy_float)

# Max value in age list
age_max = np.max(age_list_copy_float) 

# Min value in age list
age_min = np.min(age_list_copy_float)

# 25th quantile in age list 
age_25_quantile = np.percentile(age_list_copy_float, 25)

# 75th quantile in age list
age_75_quantile = np.percentile(age_list_copy_float, 75)

#------------------------------------------------------------------------------

# Tables for descriptive statistics

# Open outFile to produce results from descriptive statistics
outFile = open("Desc_Stats_Results", "w")

# Print Gender headers and results
Gender_table_header = ["Gender", "[Count, %]"]
Gender_table = [["Male", male_results],["Female", female_results]]
print(tb.tabulate(Gender_table, Gender_table_header, tablefmt = "psql"),file = outFile)
print(file = outFile)

# Print Smoker headers and results
Smoker_table_header = ["Smoker", "[Count, %]"]
Smoker_table = [["Yes", smoker_yes_results],["No", smoker_no_results]]
print(tb.tabulate(Smoker_table, Smoker_table_header, tablefmt = "psql"), file = outFile)
print(file = outFile)

# Print AMI headers and results
AMI_table_header = ["AMI", "[Count, %]"]
AMI_table = [["Yes", AMI_yes_results],["No", AMI_no_results]]
print(tb.tabulate(AMI_table, AMI_table_header, tablefmt = "psql"), file = outFile)
print(file = outFile)

# Print Race headers and results
Race_table_header = ["Race", "[Count, %]"]
Race_table = [["Asian", Asian_results],["American Indian or Alaskan Native", AmericanIndian_AlaskaNative_results], ["White", White_results], ["Black or African American", Black_results], ["Native Hawaiian/Other Pacific Islander", Native_Hawaii_results]]
print(tb.tabulate(Race_table, Race_table_header, tablefmt = "psql"), file = outFile)
print(file = outFile)

# Print CYP2C9 headers and results
CYP2C9_table_header = ["CYP2C9 Variation", "[Count, %]"]
CYP2C9_table = [["*1/*1", one_one_results], ["*1/*2", one_two_results], ["*1/*3", one_three_results], ["*2/*2", two_two_results], ["*2/*3", two_three_results]]
print(tb.tabulate(CYP2C9_table, CYP2C9_table_header, tablefmt = "psql"), file = outFile)
print(file = outFile)

# Print VKORC1 headers and results
VKORC1_table_header = ["VKORC1 Variation", "[Count, %]"]
VKORC1_table = [["A/A", AA_results], ["G/A", GA_results], ["G/G", GG_results]]
print(tb.tabulate(VKORC1_table, VKORC1_table_header, tablefmt = "psql"), file = outFile)
print(file = outFile)

# Print BMI headers and results
BMI_table_header = ["BMI","Count", "%"]
BMI_table = [["Underweight", BMI_under_count, BMI_under_percent], ["Normal", BMI_normal_count, BMI_normal_percent], ["Overweight", BMI_over_count, BMI_over_percent], ["Obese", BMI_obese_count, BMI_obese_percent]]
print(tb.tabulate(BMI_table, BMI_table_header, numalign= "left", tablefmt = "psql"), file = outFile)
print(file = outFile)

# Print Age headers and results
Age_table_header = ["Age", "Count", "%"]
Age_table = [["18-64", age_eighteen_sixtyFour_count, age_eighteen_sixtyFour_percent], ["65+", age_sixtyFive_plus_count, age_sixtyFive_plus_percent]]
print(tb.tabulate(Age_table, Age_table_header, numalign= "left", tablefmt = "psql"), file = outFile)
print(file = outFile)

# Age descriptive statistics
Age_desc_table_header = ["Age Descriptive Statistics", "Years"]
Age_desc_table = [["Mean", age_mean], ["Standard Deviation", age_stdDev], ["Max", age_max], ["Min", age_min], ['Median', age_median], ["25th quantile", age_25_quantile], ["75th quantile", age_75_quantile]]
print(tb.tabulate(Age_desc_table, Age_desc_table_header, numalign= "left", tablefmt = "psql"), file = outFile)
print(file = outFile)

# BMI descriptive statistics
BMI_desc_table_header = ["BMI Descriptive Statistics", "lbs/in^2"]
BMI_desc_table = [["Mean", BMI_mean], ["Standard Deviation", BMI_stdDev], ["Max", BMI_max], ["Min", BMI_min], ['Median', BMI_median], ["25th quantile", BMI_25_quantile], ["75th quantile", BMI_75_quantile]]
print(tb.tabulate(BMI_desc_table, BMI_desc_table_header, numalign= "left", tablefmt = "psql"), file = outFile)
print(file = outFile)

# Close outFile
outFile.close()


