Suicide Rate of Countries Based on Age and Sex (1986-2015)

Contributors: 
Delos Santos, Arviel 
Mecico, Cherry Grace
Ursabia, Carl Gian

Project Description
The primary goal of this project is to conduct an in-depth analysis of global suicide rates from 1986 to 2015, with a specific focus on age and sex distribution. It aims to unravel how age and sex distribution may influence and interact with population dynamics and economic conditions, ultimately impacting suicide rates across different countries. The primary objectives are to visualize and analyze how age and sex demographics relate to population distribution, yearly GDP, and GDP per capita, with a focus on their potential connections to variations in suicide rates.

The dataset is provided in both CSV and DBF file formats, and the analysis involves loading and processing this data to derive meaningful insights. Both files contain identical information regarding suicide rates across various countries, differentiated by age and sex. Python serves as the primary programming language for this project, with essential libraries such as pandas, plotly, and dash utilized for data manipulation and visualization. 

Implemented Features
1. Data Cleaning and Preprocessing: The dataset undergoes thorough cleaning and preprocessing activities before being loaded into the analysis environment. This step includes handling missing values, correcting data types, and ensuring data consistency.

2. Data Loading: Cleaned and preprocessed data from both CSV and DBF files are loaded into pandas dataframes to facilitate subsequent analysis.

3. Descriptive Analysis: 
 - Number of Suicides per Country based on Age and Sex:
    This section explores the number of suicides per country, considering the breakdown by age and sex. The goal is to understand how suicide rates vary across different demographics.

    Analysis Steps:    
    1. Group the data by country, age, and sex.
    2. Calculate the total number of suicides for each group.
    3. Visualize the trends using a line graph.

 - Population by Country based on Age and Sex:
    Similar to the previous section, this analysis focuses on the population, considering the breakdown by age and sex.

    Analysis Steps:
    1. Group the data by country, age, and sex.
    2. Calculate the total population for each group.
    3. Visualize the trends using a line graph.    

 - Yearly Gross Domestic Product (GDP) of a Country based on Age and Sex:
    This analysis focuses on the yearly Gross Domestic Product (GDP) of a country, considering the breakdown by age and sex.

    Analysis Steps:
    1. Group the data by country, age, and sex.
    2. Calculate the total GDP for each group for each year.
    3. Visualize the trends using a line graph.


 - Yearly Gross Domestic Product (GDP) per Capita based on Age and Sex:
    Similar to the previous section, this analysis focuses on the yearly Gross Domestic Product (GDP) per capita of a country, considering the breakdown by age and sex.

    Analysis Steps:
    1. Group the data by country, age, and sex.
    2. Calculate the GDP per capita for each group for each year.
    3. Visualize the trends using a line graph.


4. Predictive Modeling: 
- Predicted Projection on Suicides based on Age and Sex
    This analysis involves building a predictive model to project future suicides based on age and sex. The goal is to visualize the projected suicide rates against the actual rates.      

    Analysis Steps:
    1. Select relevant features for prediction (e.g., age, sex).
    2. Split the dataset into training and testing sets.
    3. Choose a predictive model (e.g., linear regression, time series model).
    4. Train the model using the training set.
    5. Predict future suicide rates.
    6. Visualize projected vs. actual suicide rates.



Dataset Information--
    Dataset Name: Suicide Rate Dataset
    Time Range: 1986 to 2015
    File Formats: CSV and DBF   

Attributes--
1. country
Description: The name of the country.
Data Type: String

2. country_iso
Description: The ISO code of the country.
Data Type: String

3. year
Description: The year in which the data was recorded.
Data Type: Integer

4. sex
Description: The gender for which the suicide rates are recorded (male or female).
Data Type: String

5. age
Description: The age group for which the suicide rates are recorded.
Data Type: String

6. suicides_no
Description: The number of suicides reported.
Data Type: Integer

7. population
Description: The population of the specified demographic group.
Data Type: Integer

8. suicides/100k pop
Description: Suicide rate per 100,000 population.
Data Type: Float

9. gdp_for_year($)
Description: Gross Domestic Product (GDP) for the specified year.
Data Type: Integer

10. gdp_per_capita($)
Description: Gross Domestic Product (GDP) per capita for the specified year.
Data Type: Integer


Programming Language and Libraries
    Programming Language: 
        Python
    Libraries:
        pandas: Used for data manipulation and analysis.
        plotly: Employed for interactive and dynamic data visualizations.
        dash: Utilized for creating an interactive web-based platform for presenting the analysis.

Deployment Instructions
