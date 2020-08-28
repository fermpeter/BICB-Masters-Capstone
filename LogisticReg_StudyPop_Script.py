# -*- coding: utf-8 -*-
"""
Created on Tue Mar 31 08:49:36 2020

@author: Peter
"""


# Install packages on Anoconda Prompt -- pip install package
import regex as re
import numpy as np
import pandas as pd
import statsmodels.api as sm

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

#               --DATA PROCESSING--


#                 --Reminders--
# Study Population referred to Dataset 1 in report.

# Copy lists and covert to needed data types
protocol_copy_list = protocol_col.copy()
BMI_list_copy_float = [float(i) for i in BMI_col]
age_list_copy_float = [float(i) for i in age_col]
ttrIn_list_copy_float = [float(i) for i in ttrIN_col]


# Logistic regression function to implement model by protocol
def logit_reg_pro(df, protocol_str, x=None, y=None):   
    # Get the rows datafarame of passed in protocol string
    df_protocol = df[df['protocol'] == protocol_str]
    
    # Get column names that are your predictor variables and baseline 
    train_col = df_protocol.columns[x:y]
    
    # Logit formula
    LogitEq = sm.Logit(df_protocol['ttrIn'], df_protocol[train_col])
    
    # Fit the model
    results = LogitEq.fit()
    
    # Return the results 
    return results


# Function to create df and convert log odds and log confidence interval to odds and confidence interval
def conf_int_OR(Logit_Results):
    # Gather log Odds ratio of results
    parmas = Logit_Results.params
    
    # Get log confidence interval
    confidence_int = Logit_Results.conf_int()
    
    # Set odds ratio to OR column in df
    confidence_int['OR'] = parmas
    
    #Set df columns of confidence interval range and OR
    confidence_int.columns = ['2.5%', '97.5%', 'OR']
    
    # Conver and return df 
    return np.exp(confidence_int)


# Function to find predictor variable odds
def predictor_odds(Logit_Results, x, y):
    # Retrive OR from indexed position
    OR = np.exp(Logit_Results.params[x])
    
    # Retrive baseline odds of indexed postion
    baselineOdds = np.exp(Logit_Results.params[y])
    
    # Compute odds of predictor sub-group 
    predictorOdds = OR * baselineOdds
    
    # Return odds of predictor sub-groups
    return predictorOdds


#             --Age Binary Logistic Regression--
#             Baseline age group is 65+ category  
   
# Create combined dataframe from imported lists
df_protocol_ttrIn_age = pd.DataFrame(list(zip(protocol_copy_list, ttrIn_list_copy_float, age_list_copy_float)), columns = ['protocol', 'ttrIn', 'age']) 


# Find the rows in merged dataframe where ttrIn >= 75,
# Create binary outcome variable (ttrIn) for modelling, where
# Y = 1 for ttrIn >= 75
# Y = 0 for ttrIn < 75
df_protocol_ttrIn_age['ttrIn'] = np.where(df_protocol_ttrIn_age['ttrIn'] >= 75 , 1, 0)


# Find the rows in merged dataframe where age < 65,
# Create binary predictor dummy variable (age), where
# X = 1 for ages 18-64
# X = 0 for ages 65+
df_protocol_ttrIn_age['age'] = np.where(df_protocol_ttrIn_age['age'] < 65, 1, 0) 

# Add column for the baseline group (age: 65+)
df_protocol_ttrIn_age.insert(3, 'Baseline(65+)', 1)


#        --DATA VISUALIZATION AND EXPLORATION--

#                --AAA Protocol--

# Binary Logistic regression results for protocol AAA, ttrIn (outcome), Age catergories(predictor) 
Logit_age_AAA_result = logit_reg_pro(df_protocol_ttrIn_age,'"AAA"', 2)

# Summary of results
print(Logit_age_AAA_result.summary())

# Function call of Odds Ratio and confidence interval 

# Function call of predictor odds 
print(predictor_odds(Logit_age_AAA_result, 0, 1))

 
#                --CAA Protocol--

# Binary Logistic regression results for protocol CAA, ttrIn (outcome), Age catergories(predictor) 
Logit_age_CAA_result = logit_reg_pro(df_protocol_ttrIn_age,'"CAA"', 2)

# Summary of results
print(Logit_age_CAA_result.summary())

# Function call of Odds Ratio and confidence interval
print(conf_int_OR(Logit_age_CAA_result)) 

# Function call of predictor odds 
print(predictor_odds(Logit_age_CAA_result, 0, 1))


#                --PGAA Protocol--

# Binary Logistic regression results for protocol PGAA, ttrIn (outcome), Age catergories(predictor) 
Logit_age_PGAA_result = logit_reg_pro(df_protocol_ttrIn_age,'"PGAA"', 2)

# Summary of results
print(Logit_age_PGAA_result.summary())

# Function call of Odds Ratio and confidence interval 
print(conf_int_OR(Logit_age_PGAA_result)) 

# Function call of predictor odds 
print(predictor_odds(Logit_age_PGAA_result, 0, 1))


#                 --PGPGI Protocol--

# Binary Logistic regression results for protocol PGPGI, ttrIn (outcome), Age catergories(predictor) 
Logit_age_PGPGI_result = logit_reg_pro(df_protocol_ttrIn_age,'"PGPGI"', 2)

# Summary of results
print(Logit_age_PGPGI_result.summary())

# Function call of Odds Ratio and confidence interval
print(conf_int_OR(Logit_age_PGPGI_result)) 

# Function call of predictor odds 
print(predictor_odds(Logit_age_PGPGI_result, 0, 1))


#                 --PGPGA Protocol--

# Binary Logistic regression results for protocol PGPGA, ttrIn (outcome), Age catergories (predictor) 
Logit_age_PGPGA_result = logit_reg_pro(df_protocol_ttrIn_age,'"PGPGA"', 2)

# Summary of results
print(Logit_age_PGPGA_result.summary())

# Function call of Odds Ratio and confidence interval 
print(conf_int_OR(Logit_age_PGPGA_result)) 

# Function call of predictor odds 
print(predictor_odds(Logit_age_PGPGA_result, 0, 1))

#-----------------------------------------------------------------------------

#                       --DATA PROCESSING--

#                --BMI Multi Logistic Regression--
#                Baseline BMI group is Obese category  

# Create combined dataframe
df_protocol_ttrIn = pd.DataFrame(list(zip(protocol_copy_list, ttrIn_list_copy_float)), columns = ['protocol', 'ttrIn']) 


# Find the rows in merged dataframes where ttrIn >= 75,
# Create binary dependent (ttrIn) k-1 dummy variables, where
# Y = 1 for ttrIn >= 75
# Y = 0 for ttrIn < 75
df_protocol_ttrIn['ttrIn'] = np.where(df_protocol_ttrIn['ttrIn'] >= 75 , 1, 0)

# Find the rows in merged dataframes and set to BMI categories,
# under -- 1
# BMI < 18.5
# normal -- 2
# BMI >= 18.5 and BMI <=25       
# over -- 3
# BMI > 25 and BMI <= 30
# obese -- 4
# BMI > 30

# Initialize container
logit_BMI_Categories = []
# Iterate through BMI list to code different BMI categories 
for i in BMI_list_copy_float:
    # under -- 1
    if (i < 18.5):
        logit_BMI_Categories.append(1)
    # normal -- 2
    elif (i >= 18.5 and i <=25):
        logit_BMI_Categories.append(2)
    # over -- 3
    elif (i > 25 and i <= 30):
        logit_BMI_Categories.append(3)
    # obese -- 4
    elif (i > 30):
        logit_BMI_Categories.append(4)

# Dummify BMI categories to new dataframe with binary indicator variables
dummy_logit_BMI = pd.get_dummies(logit_BMI_Categories)

# Merge protocol/ttrIn dataframe with dummify BMI categories
merged_df_BMIdummy_proTTR = df_protocol_ttrIn.join(dummy_logit_BMI)

# Rename columns to BMI names
merged_df_BMIdummy_proTTR.columns = ['protocol', 'ttrIn', 'under', 'normal', 'over', 'obese']

# Add intercept
merged_df_BMIdummy_proTTR.insert(2, 'Baseline(obese)', 1)



#             --DATA VISUALIZATION AND EXPLORATION--

#                     --AAA--

# Multi Logistic regression results for AAA, ttrIn (outcome), BMI catergories (predictors) 
Logit_BMI_AAA_result = logit_reg_pro(merged_df_BMIdummy_proTTR,'"AAA"', 2, 6)

# Summary of results
print(Logit_BMI_AAA_result.summary())

# Function call of Odds Ratio and confidence interval 
print(conf_int_OR(Logit_BMI_AAA_result)) 

# under -- predictor odds
print('under', predictor_odds(Logit_BMI_AAA_result, 1, 0))

# normal -- predictor odds
print('normal',predictor_odds(Logit_BMI_AAA_result, 2, 0))

# over -- predictor odds
print('over', predictor_odds(Logit_BMI_AAA_result, 3, 0))


#                     --CAA--

# Multi Logistic regression results for CAA, ttrIn (outcome), BMI catergories (predictors) 
Logit_BMI_CAA_result = logit_reg_pro(merged_df_BMIdummy_proTTR,'"CAA"', 2, 6)

# Summary of results
print(Logit_BMI_CAA_result.summary())

# Function call of Odds Ratio and confidence interval 
print(conf_int_OR(Logit_BMI_CAA_result)) 

# under -- predictor odds
print('under', predictor_odds(Logit_BMI_CAA_result, 1, 0))

# normal -- predictor odds
print('normal',predictor_odds(Logit_BMI_CAA_result, 2, 0))

# over -- predictor odds
print('over', predictor_odds(Logit_BMI_CAA_result, 3, 0))


#                    --PGAA--

# Multi Logistic regression results for PGAA, ttrIn (outcome), BMI catergories (predictor) 
Logit_BMI_PGAA_result = logit_reg_pro(merged_df_BMIdummy_proTTR,'"PGAA"', 2, 6)

# Summary of results
print(Logit_BMI_PGAA_result.summary())

# Function call of Odds Ratio and confidence interval 
print(conf_int_OR(Logit_BMI_PGAA_result)) 

# under -- predictor odds
print('under', predictor_odds(Logit_BMI_PGAA_result, 1, 0))

# normal -- predictor odds
print('normal',predictor_odds(Logit_BMI_PGAA_result, 2, 0))

# over -- predictor odds
print('over', predictor_odds(Logit_BMI_PGAA_result, 3, 0))



#                   --PGPGI--

# Multi Logistic regression results for PGPGI, ttrIn (outcome), BMI categories (predictors) 
Logit_BMI_PGPGI_result = logit_reg_pro(merged_df_BMIdummy_proTTR,'"PGPGI"', 2, 6)

# Summary of results
print(Logit_BMI_PGPGI_result.summary())

# Function call of Odds Ratio and confidence interval 
print(conf_int_OR(Logit_BMI_PGPGI_result)) 

# under -- predictor odds
print('under', predictor_odds(Logit_BMI_PGPGI_result, 1, 0))

# normal -- predictor odds
print('normal',predictor_odds(Logit_BMI_PGPGI_result, 2, 0))

# over -- predictor odds
print('over', predictor_odds(Logit_BMI_PGPGI_result, 3, 0))


#                   --PGPGA--

# Multi Logistic regression results for PGPGA, ttrIn (outcome), BMI catergories (predictors) 
Logit_BMI_PGPGA_result = logit_reg_pro(merged_df_BMIdummy_proTTR,'"PGPGA"', 2, 6)

# Summary of results
print(Logit_BMI_PGPGA_result.summary())

# Function call of Odds Ratio and confidence interval 
print(conf_int_OR(Logit_BMI_PGPGA_result)) 

# under -- predictor odds
print('under', predictor_odds(Logit_BMI_PGPGA_result, 1, 0))

# normal -- predictor odds
print('normal',predictor_odds(Logit_BMI_PGPGA_result, 2, 0))

# over -- predictor odds
print('over', predictor_odds(Logit_BMI_PGPGA_result, 3, 0))


#------------------------------------------------------------------------------

#                       --DATA PROCESSING--

#             --Protocol Multi Logistic Regression
#              Baseline PGAA group is Obese category  


# Create combined dataframe
df_protocol_ttrIn = pd.DataFrame(list(zip(protocol_copy_list, ttrIn_list_copy_float)), columns = ['protocol', 'ttrIn']) 

# Find the rows in merged dataframes where ttrIn >= 75,
# Create binary dependent (ttrIn) k-1 dummy variables, where
# Y = 1 for ttrIn >= 75
# Y = 0 for ttrIn < 75
df_protocol_ttrIn['ttrIn'] = np.where(df_protocol_ttrIn['ttrIn'] >= 75 , 1, 0)

# Intialize container
logit_pro_Categories = []
# Iterate through protocol list to code different Protocol categories 
for i in protocol_copy_list:
    if (i == '"AAA"'):
        logit_pro_Categories.append(1)
    elif (i == '"CAA"'):
        logit_pro_Categories.append(2)
    elif (i == '"PGPGI"'):
        logit_pro_Categories.append(3)
    elif (i == '"PGPGA"'):
        logit_pro_Categories.append(4)
    elif (i == '"PGAA"'):
        logit_pro_Categories.append(5)


# Dummify BMI categories to new dataframe with binary indicator variables
dummy_logit_pro = pd.get_dummies(logit_pro_Categories)

# Merge protocol/ttrIn dataframe with dummify protocol categories
merged_df_prodummy_proTTR = df_protocol_ttrIn.join(dummy_logit_pro)

# Rename columns to protocol names
merged_df_prodummy_proTTR.columns = ['protocol', 'ttrIn', 'AAA', 'CAA', 'PGPGI', 'PGPGA', 'PGAA']

# Add intercept
merged_df_prodummy_proTTR.insert(6, 'Baseline(PGAA)', 1)

# Get column names that are your predictor variables and baseline 
train_col = merged_df_prodummy_proTTR.columns[2:7]

# Logit formula
LogitEq = sm.Logit(merged_df_prodummy_proTTR['ttrIn'], merged_df_prodummy_proTTR[train_col])

# Fit the model
results = LogitEq.fit()


#              --DATA VISUALIZATION AND EXPLORATION--


# Summary of Protocol results
print(results.summary())

# Function call of Odds Ratio and confidnece interval 
print(conf_int_OR(results)) 

# AAA -- predictor odds
print('AAA', predictor_odds(results, 0, 4))

# CAA -- predictor odds
print('CAA',predictor_odds(results, 1, 4))

# PGPGI -- predictor odds
print('PGPGI', predictor_odds(results, 2, 4))

# PGPGA -- predictor odds
print('PGPGA', predictor_odds(results, 3, 4))


