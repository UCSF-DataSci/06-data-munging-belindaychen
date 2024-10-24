import pandas as pd
import numpy as np
import logging
import argparse

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def clean_population_data(input, output):
    try:
        # Load the dataset
        df = pd.read_csv(input)
        logging.info(f"Dataset loaded successfully with shape {df.shape}")

        # Display non-null counts and unique values before cleaning
        for column in df.columns:
            non_null_count = df[column].notnull().sum()
            unique_count = df[column].nunique()
            logging.info(f"{column}: Non-null count = {non_null_count}, Unique count = {unique_count}")

    except FileNotFoundError:
        logging.error(f"Error: File {input} not found.")
        return
    except Exception as e:
        logging.error(f"An error occurred while loading the file: {e}")
        return

    try:
        # Remove duplicate data
        initial_rows = len(df)
        df = df.drop_duplicates()
        duplicates_removed = initial_rows - len(df)
        logging.info(f"Removed {duplicates_removed} duplicate rows")

        # Impute missing values using median for numerical columns and mode for categorical columns or other for gender
        df['population'] = df['population'].fillna(df['population'].median())
        df['age'] = df['age'].fillna(df['age'].median())
        df['gender'] = df['gender'].fillna(3)  #filling in missing values 
        df['income_groups'] = df['income_groups'].fillna(df['income_groups'].mode()[0]) #filling in with mode
        logging.info("Missing values completed")

        # Standardize gender representation
        gender_mapping = {1: 'Male', 2: 'Female', 3: 'Other'}
        df['gender'] = df['gender'].map(gender_mapping)

        # Correct income group names
        income_group_corrections = {
            'low_income_typo': 'low_income',
            'lower_middle_income_typo': 'lower_middle_income',
            'high_income_typo': 'high_income',
            'upper_middle_income_typo': 'upper_middle_income'
        }
        df['income_groups'] = df['income_groups'].replace(income_group_corrections)

        # stripping whitespace from income groups
        df['income_groups'] = df['income_groups'].str.strip()

        # Addressing outliers in population and age using IQR method
        population_outlier = df['population'].quantile(0.99)
        df['population'] = np.where(df['population'] > population_outlier, population_outlier, df['population'])

        df['age'] = np.where(df['age'] > 120, 120, df['age'])  # Capping age at 120

        # Convert population to integers to remove 
        df['population'] = df['population'].astype(int)

        # Convert year column to integer type
        df['year'] = df['year'].fillna(df['year'].mode()[0])
        df['year'] = df['year'].astype(int)

        # Validate data ranges
        df['population'] = df['population'].apply(lambda x: x if x >= 0 else np.nan)
        df = df.dropna(subset=['population'])  # Remove any remaining invalid population values

        # Check for any remaining missing values
        missing_after_cleaning = df.isnull().sum()
        logging.info(f"Remaining missing values:\n{missing_after_cleaning}")

        # Convert population and age columns to integers 
        df['age'] = df['age'].apply(lambda x: int(x) if x.is_integer() else x)

        # Show non-null and missing values post cleaning
        for column in df.columns:
            non_null_count = df[column].notnull().sum()
            unique_count = df[column].nunique()
            logging.info(f"{column}: Non-null count = {non_null_count}, Unique count = {unique_count}")

        # Save the cleaned dataset
        df.to_csv(output, index=False)
        logging.info("Cleaned dataset saved successfully")

    except Exception as e:
        logging.error(f"An error occurred during the cleaning process: {e}")
        return



if __name__ == "__main__":
    try:
        clean_population_data(input = 'messy_population_data.csv', output = 'cleaned_population_data.csv')
    except Exception as e: 
        logging.error(f"An error occured: {e}")