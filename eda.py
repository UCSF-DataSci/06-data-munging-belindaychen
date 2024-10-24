import pandas as pd
import numpy as np
from numpy.random import default_rng
import argparse
from tqdm import tqdm

dirty = pd.read_csv('messy_population_data.csv')

dirty.info()
dirty.describe()
missing = dirty.isnull().sum()#about 6k null for each of the columns -> missing population counts
print(f"Number of missing values: {missing}")
duplicates = dirty.duplicated().sum() #duplicated sum = 2950
print(f"Number of duplicate rows: {duplicates}")
dirty.value_counts() #95425 total 

#visible problems 
#null values and outliers in population columns, inconsistent income group labels (hyphens, caps, etc), invalid age categories, duplicated records,