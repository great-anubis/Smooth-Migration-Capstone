import os
import pandas as pd
import re

# Define base directory
base_dir = os.path.dirname(os.path.abspath(__file__))

# Define dataset directories
datasets = {
    'cost_of_living': {
        'input': os.path.join(base_dir, '../data/dirty/cost-of-living-indexes'),
        'output': os.path.join(base_dir, '../data/clean/cost-of-living-indexes')
    },
    'government_policies': {
        'input': os.path.join(base_dir, '../data/dirty/government-policies'),
        'output': os.path.join(base_dir, '../data/clean/government-policies')
    },
    'job_housing': {
        'input': os.path.join(base_dir, '../data/dirty/job-housing'),
        'output': os.path.join(base_dir, '../data/clean/job-housing')
    },
    'migration': {
        'input': os.path.join(base_dir, '../data/dirty/migration'),
        'output': os.path.join(base_dir, '../data/clean/migration')
    },
    'travel_logistics': {
        'input': os.path.join(base_dir, '../data/dirty/travel-logistics'),
        'output': os.path.join(base_dir, '../data/clean/travel-logistics')
    }
}

# Ensure output directories exist
for dataset in datasets.values():
    os.makedirs(dataset['output'], exist_ok=True)

# Utility function to clean column names
def clean_column_names(df):
    df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_')
    return df

# Utility function to clean numeric columns
def clean_numeric_column(df, column_name):
    if column_name in df.columns:
        df[column_name] = df[column_name].astype(str).apply(lambda x: re.sub(r'[^\d.]', '', x))
        df[column_name] = pd.to_numeric(df[column_name], errors='coerce')
    return df

# Preprocessing functions for each dataset
def preprocess_cost_of_living(df):
    # Implement cost of living data preprocessing steps
    return df

def preprocess_government_policies(df):
    # Implement government policies data preprocessing steps
    return df

def preprocess_job_housing(df):
    # Implement job and housing data preprocessing steps
    return df

def preprocess_migration(df):
    # Implement migration data preprocessing steps
    return df

def preprocess_travel_logistics(df):
    # Implement travel logistics data preprocessing steps
    return df

# Mapping of dataset types to their preprocessing functions
preprocessing_functions = {
    'cost_of_living': preprocess_cost_of_living,
    'government_policies': preprocess_government_policies,
    'job_housing': preprocess_job_housing,
    'migration': preprocess_migration,
    'travel_logistics': preprocess_travel_logistics
}

# Function to process files in a directory
def process_files(dataset_name, input_dir, output_dir):
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

            # Clean column names
            df = clean_column_names(df)

            # Apply dataset-specific preprocessing
            preprocess_func = preprocessing_functions.get(dataset_name)
            if preprocess_func:
                df = preprocess_func(df)
            else:
                print(f"No preprocessing function found for {dataset_name}. Skipping.")
                continue

            # Save the processed file
            output_file_path = os.path.join(output_dir, f'cleaned_{filename}')
            df.to_csv(output_file_path, index=False)
            print(f"Processed and saved: {output_file_path}")
        except Exception as e:
            print(f"Error processing {filename}: {e}")

# Main execution
def main():
    for dataset_name, paths in datasets.items():
        print(f"Processing dataset: {dataset_name}")
        process_files(dataset_name, paths['input'], paths['output'])
    print("✅ Data preprocessing complete.")

if __name__ == "__main__":
    main()
