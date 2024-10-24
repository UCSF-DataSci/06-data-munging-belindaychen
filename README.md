# Data Cleaning Project: Population Dataset

## 1. Initial State Analysis

### Dataset Overview
- **Name**: messy_population_data.csv
- **Rows**: 125719
- **Columns**: 5

### Column Details
| Column Name   | Data Type | Non-Null Count | Unique Values | 
|-------------  |-----------|----------------|---------------|
| [income_groups]  | [string]    | [119412]        | [8]      | 
| [age]  | [float]       | [119495]            | [101]           | 
| [gender]  | [float]       | [119811]            | [3]           | 
| [year]  | [int]       | [119516]            | [169]           | 
| [population]  | [float]       | [119378]            | [113698]           | 


### Identified Issues

1. **[Missing values]**
   - Description: [Missing values in columns]
   - Affected Column(s): [population, age, gender, income_groups]
   - Example: [NaN values in 'population' column]
   - Potential Impact: [Missing data will be calculated in the cleaning script and may lead to biased results]

2. **[Invalid Categories]**
     - Description: [Out-of-range values and incorrect formulas]
   - Affected Column(s): [age, gender]
   - Example: ['-5, '150+', 'unknown' in age column]
   - Potential Impact: [age-based and gender-based analysis errors, may lead to over/underrepresentation of certain demographics]

3. **[Inconsistent Group Labeling]**
   - Description: [Mixed case, typos, and inconsistent naming]
   - Affected Column(s): [income_groups]
   - Example: ['high income' vs 'HighIncome' vs 'High_Income']
   - Potential Impact: [Grouping and aggregation errors, particularly in finding mode, unique values]
  
4. **[Invalid values]**
   - Description: [Negative numbers or extremely large outliers]
   - Affected Column(s): [population]
   - Example: [-1000, 999999]
   - Potential Impact: [incorrect population statistics]

## 2. Data Cleaning Process

### Issue 1: [Missing values]
- **Cleaning Method**: [Fill in missing values with the mean or mode of the entire column; see population column example below]
- **Implementation**:
  ```python
  df['population'] = df['population'].fillna(df['population'].median())
  ```
- **Justification**: [By imputing missing values in the dataset, we can ensure reasonable reliability and keep the dataset large.]
- **Impact**: [Missing values were successfully filled. ]

### Issue 2: [Income Group Standardization]
- **Cleaning Method**: [Covnert to a consistent form (lowercase, underscore separated)]
- **Implementation**:
  ```python
  income_group_corrections = {
            'low_income_typo': 'low_income',
            'lower_middle_income_typo': 'lower_middle_income',
            'high_income_typo': 'high_income',
            'upper_middle_income_typo': 'upper_middle_income'
        }
        df['income_groups'] = df['income_groups'].replace(income_group_corrections)

        # stripping whitespace from income groups
        df['income_groups'] = df['income_groups'].str.strip()
  ```
- **Justification**: [By removing special characters and mapping to standard categories, we can have consistent categorization for analysis.]
- **Impact**: [Consistent values were filled and we can obtain accurate numbers of unique values.]


### Issue 1: [Duplicate Handling]
- **Cleaning Method**: [Remove exact duplicates]
- **Implementation**:
  ```python
  initial_rows = len(df)
        df = df.drop_duplicates()
        duplicates_removed = initial_rows - len(df)
  ```
- **Justification**: [Removing exact duplicates prevents overrepresentation of certain demographics.]
- **Impact**: [Prevented skewing of data.]


## 3. Final State Analysis

### Dataset Overview
- **Name**: cleaned_population_data.csv 
- **Rows**: [122769]
- **Columns**: [5]

### Column Details
| Column Name | Data Type | Non-Null Count | #Unique Values |  
|-------------|-----------|----------------|----------------|
| [population]  | [int]    | [122769]        | [113689]      | 
| [age]         | [int]       | [122769]            | [101]            | 
| [gender]         | [object]       | [122769]            | [3]            | 
| [income_groups]         | [object]       | [122769]            | [4]            | 
| [year]         | [int]       | [122769]            | [169]            | 

### Summary of Changes
- removed missing rows 
- standardized income groups by removing special characters and implemented consistent formatting 
- age and population value correction to standardize formatting 
- exact duplicates removed 
- removed outliers in population and age according to the IQR method 
- converted population, age, and year columns to integers
