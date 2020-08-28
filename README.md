
# __Masters Capstone Project__

## __University of Minnesota__<br><sup>__Bioinformatics and Computational Biology Program__</sup>
---
### __About the Project__

#### __Title__
__Group and Dataset Comparisons for Optimization and Simulation-Based Approaches to Warfarin Treatment Protocols__

#### __Background__
Warfarin is an inexpensive and frequently used anticoagulant medication to treat and prevent blood clot disorders. Management of its important treatment measurements such as the International Normalized Ratio and Time in Therapeutic Range are constantly monitored due to the powerful two-sided adverse effects. Patients that are not within the therapeutic ranges are at risk of over-anticoagulation (i.e. causing bleeding), or under-anticoagulation (i.e. increased risk for strokes). The narrow therapeutic windows coupled with high variability in dosage have been linked to clinical and genetic factors of an individual.

The primary study under consideration generated a study population of 1,478,930 simulated patients referred to as “clinical avatars”. The study population was based on a ten-year period of real-world atrial fibrillation patients, which were de-identified, and institutional review board approved before the necessary medical information was extracted from the Aurora Health Care system’s electronic medical records (EMRs).  Each clinical avatar underwent five simulated warfarin protocol treatments for a 30-day or a 90-day period. The five protocols were distinct and based on either clinical, pharmacogenomic, or a combination of clinical and pharmacogenomic approaches. To do a suitable representation of clinical avatar's genetic characteristics, an extensive literature review and expert domain knowledge were necessary due to the limited amount of real-world genetic tests and limited storage of patient’s genotypes. A Bayesian network model and Stochastic models were utilized to match the patterns of the clinical information extracted from the EMRs to create a viable study population.  The simulated treatment values for each clinical avatar were predicted by developing a machine learning technique for a warfarin Pharmacokinetic/Pharmacodynamic model.  The results of the simulated framework were compared to a real-world warfarin clinical trial to validate the accuracy of the clinical avatars and their corresponding simulations. A decision tree algorithm derived sub-populations to identify the factors that the clinical avatars could optimize by treatment protocols. The objective of the study was to find a cost-effective and realistic means for designing and evaluating precision-driven warfarin treatment protocols. A secondary analysis used a small random sample of 800 clinical avatars to investigate the effectiveness of warfarin treatment plans concerning important clinical characteristics (age and BMI). Furthermore, how genetics and genomics are used in the Nursing environment.

#### __Description__
I developed Python scripts to visualize and perform logistic regression analysis to compare the study population dataset to the sample size dataset to generate summary reports for my findings. The study population clinical avatars were stored in a pipe-delimited text file (\~3.14 Gigabytes). It stored thirty attributes about the clinical avatars. The attributes contained the avatar’s clinical characteristics, genetic characteristics, primary identifications, and simulated warfarin treatment outcomes. The sample size contained a smaller list of attributes that were appropriate for the secondary analysis. The sample size avatars were stored in an excel file (\~554 Kilobytes). These files were shared with me as a part of my capstone experience to gain hands-on experience with informatics and data analysis. I do not have the authority to provide these files. I will use discretion by not sharing them publicly and maintaining the privacy of the primary studies data. The study population is referred as *Dataset 1* and the sample size is referred as *Dataset 2* in the capstone report and results.

---
#### __Repository__

The repository contains the scripts, and results of the Masters Capstone Experience.

###### [DesciptStats_CountsPercents_Script](https://github.com/fermpeter/BICB_Capstone/blob/master/DescriptStats_CountsPercent_Script.py)

- Descriptive statistics from the study population are explored and visualized in tables.
-Results in *Desc_Stats_Results.pdf*

###### [DesciptStats_StudyPopVisual_Script](https://github.com/fermpeter/BICB_Capstone/blob/master/DesciptStats_StudyPopVisual_Script.py)

- Relevant attributes and their corresponding sub-categories from the study population are wrangled and displayed in count plots
-Results in *Figure_1_Capstone.pdf*

###### [DesciptStats_SampSizeVisual_Script](https://github.com/fermpeter/BICB_Capstone/blob/master/DescriptStats_SampSizeVisual_Script.py)

- Relevant attributes and their corresponding sub-categories from the sample size are wrangled and displayed in count plots
- Results in *Figure_2_Capstone.pdf*

###### [ttrIn_StudyPopVisual_Script.py](https://github.com/fermpeter/BICB_Capstone/blob/master/DesciptStats_StudyPopVisual_Script.py)

- Clinical avatar’s from the study population dataset are processed by selecting clinical characteristics and their sub-categories being in or out of therapeutic range for each treatment protocol.
- Visualized as count plots
- AGE
  - Sub-categories: 18-64 and 65+
  - Results in *Figure_3_Capstone.pdf*

- BMI
  - Sub-categories: Underweight, Normal, Overweight, Obese
  - Results in *Figure_5_Capstone.pdf*

- Protocol
  - Sub-categories: AAA, CAA, PGAA, PGPGI, PGPGA
  - Results in *Figure_7_Capstone.pdf*


###### [ttrIn_SampleSizeVisual_Script.py](https://github.com/fermpeter/BICB_Capstone/blob/master/ttrIn_SampleSizeVisual_Script.py)

- Clinical avatar’s from the sample size dataset are processed by capturing clinical characteristics and their sub-categories being in or out of therapeutic range for each treatment protocol.
- Visualized as count plots
- AGE
  - Sub-categories: 18-64 and 65+
  - Results in *Figure_4_Capstone.pdf*

- BMI
  - Sub-categories: Underweight, Normal, Overweight, Obese
  - Results in *Figure_6_Capstone.pdf*

- Protocol
  - Sub-categories: AAA, CAA, PGAA, PGPGI, PGPGA
  - Results in *Figure_8_Capstone.pdf*

###### [LogisticReg_Script](https://github.com/fermpeter/BICB_Capstone/blob/master/LogisticReg_Script.py)
- A goal of the capstone project was to compute inferential statistics using a logistic regression approach to compare to specific aims and results from secondary analysis. In the secondary analysis a chi-square test of homogeneity was performed to interpret the impact of patient characteristics (age and BMI), on the effectiveness of clinical versus pharmacogenomic treatment protocols, measured by the TTR, for the 30-day treatment-simulation data.

-  Results from the logistic regression were printed to Ipython console and then imported to a table of results.

- Protocol Outputs
![Table_7_Capstone](https://user-images.githubusercontent.com/69829891/91520524-1d84eb00-e8bb-11ea-81cc-bbac1407db6a.JPG)

- Age Outputs

![Table_9_Capstone](https://user-images.githubusercontent.com/69829891/91520638-6177f000-e8bb-11ea-8fc0-49d4cf9b6ca4.JPG)


- BMI Outputs
![Table_11_Capstone](https://user-images.githubusercontent.com/69829891/91520675-7ce2fb00-e8bb-11ea-8766-2e3a17810bcc.JPG)

---
#### __Collaborative Team__  
Chih-Lin Chi, Ph.D., M.B.A.  
Graduate Advisor  
Principal Investigator  
Institute of Health Informatics  
School of Nursing, Center for Nursing Informatics

Michelle A. Mathiason Moore, M.S.   
Biostatistician  
School of Nursing  

Miki Dahlin, BSN

---






#### __Links__

##### Primary Study's Journal Links

[Personalized Anticoagulation: Optimizing Warfarin Management Using Genetics and Simulated Clinical Trials](https://pubmed.ncbi.nlm.nih.gov/29237680)

[Optimal decision support rules improve personalize warfarin treatment outcomes](https://pubmed.ncbi.nlm.nih.gov/28268853/)

[Using simulation and optimization approach to improve outcome through warfarin precision treatment](https://pubmed.ncbi.nlm.nih.gov/29218901/)            
