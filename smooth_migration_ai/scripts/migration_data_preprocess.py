import os
import pandas as pd
import re

# Define input and output directories
input_dir = os.path.join(os.path.dirname(__file__), '../data/dirty/migration')
output_dir = os.path.join(os.path.dirname(__file__), '../data/clean/migration')
os.makedirs(output_dir, exist_ok=True)

def clean_column_names(df):
    """
    Standardize column names: strip whitespace, convert to lowercase, and replace spaces with underscores.
    """
    df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_')
    return df

def clean_numeric_column(df, column_name):
    """
    Clean and convert a column to numeric, handling common issues like currency symbols and commas.
    """
    if column_name in df.columns:
        df[column_name] = df[column_name].astype(str).apply(lambda x: re.sub(r'[^\d.]', '', x))
        df[column_name] = pd.to_numeric(df[column_name], errors='coerce')
    return df

def preprocess_migration_data(df):
    """
    Perform specific preprocessing steps for migration data.
    """
    df = clean_column_names(df)
    
    # Example: Standardize country names if a 'country' column exists
    if 'country' in df.columns:
        df['country'] = df['country'].str.strip().str.title()
    
    # Example: Clean numeric columns
    numeric_columns = ['population', 'net_migration']
    for col in numeric_columns:
        df = clean_numeric_column(df, col)
    
    # Handle missing values
    df.fillna(method='ffill', inplace=True)  # Forward fill as an example; adjust as needed
    
    return df

# Process each file in the input directory
for filename in os.listdir(input_dir):
    file_path = os.path.join(input_dir, filename)
    try:
        if filename.endswith('.csv'):
            df = pd.read_csv(file_path)
        elif filename.endswith('.tsv'):
            df = pd.read_csv(file_path, sep='\t')
        elif filename.endswith('.xlsx'):
            df = pd.read_excel(file_path)
        else:
            print(f"Unsupported file format: {filename}. Skipping.")
            continue

        df = preprocess_migration_data(df)

        output_file_path = os.path.join(output_dir, f'cleaned_{filename}')
        df.to_csv(output_file_path, index=False)
        print(f"Processed and saved: {output_file_path}")
    except Exception as e:
        print(f"Error processing {filename}: {e}")

print("✅ Migration data preprocessing complete.")
