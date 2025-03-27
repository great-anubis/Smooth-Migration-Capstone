import os
import pandas as pd
import re

# Define input and output directories
input_dir = os.path.join(os.path.dirname(__file__), '../data/dirty/job-housing')
output_dir = os.path.join(os.path.dirname(__file__), '../data/clean/job-housing')
os.makedirs(output_dir, exist_ok=True)

def clean_currency(value):
    """
    Remove currency symbols and commas, and convert to float.
    """
    if isinstance(value, str):
        value = re.sub(r'[^\d.]', '', value)
        try:
            return float(value)
        except ValueError:
            return None
    return value

def preprocess_job_data(df):
    df.drop_duplicates(inplace=True)
    if 'salary' in df.columns:
        df['salary'] = df['salary'].apply(clean_currency)
        df['salary'].fillna(df['salary'].median(), inplace=True)
    # Additional job data preprocessing steps
    return df

def preprocess_housing_data(df):
    df.drop_duplicates(inplace=True)
    if 'price' in df.columns:
        df['price'] = df['price'].apply(clean_currency)
        df['price'].fillna(df['price'].median(), inplace=True)
    # Additional housing data preprocessing steps
    return df

for filename in os.listdir(input_dir):
    file_path = os.path.join(input_dir, filename)
    try:
        if filename.endswith('.csv'):
            df = pd.read_csv(file_path)
        elif filename.endswith('.tsv') or filename.endswith('.tsv000'):
            df = pd.read_csv(file_path, sep='\t')
        elif filename.endswith('.xlsx'):
            df = pd.read_excel(file_path)
        else:
            print(f"Unsupported file format: {filename}. Skipping.")
            continue

        # Standardize column names
        df.columns = df.columns.str.lower().str.replace(' ', '_')

        # Determine dataset type based on column presence
        if 'job_title' in df.columns:
            df = preprocess_job_data(df)
        elif 'property_type' in df.columns:
            df = preprocess_housing_data(df)
        else:
            print(f"Unrecognized data structure in {filename}. Skipping.")
            continue

        output_file_path = os.path.join(output_dir, f'cleaned_{filename}')
        df.to_csv(output_file_path, index=False)
        print(f"Processed and saved: {output_file_path}")
    except Exception as e:
        print(f"Error processing {filename}: {e}")

print("✅ Job and housing data preprocessing complete.")
