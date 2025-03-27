import os
import pandas as pd

# Define input and output directories
input_dir = os.path.join(os.path.dirname(__file__), '../data/dirty/government-policies')
output_dir = os.path.join(os.path.dirname(__file__), '../data/clean/government-policies')
os.makedirs(output_dir, exist_ok=True)

# Function to preprocess each DataFrame
def preprocess_df(df, source_name):
    # Drop completely empty rows and columns
    df.dropna(how='all', inplace=True)
    df.dropna(axis=1, how='all', inplace=True)

    # Standardize column names: strip whitespace and replace spaces with underscores
    df.columns = [col.strip().lower().replace(' ', '_') for col in df.columns]

    # Example: Convert date columns to datetime format
    for col in df.columns:
        if 'date' in col:
            df[col] = pd.to_datetime(df[col], errors='coerce')

    # Example: Fill missing values in categorical columns with 'Unknown'
    categorical_cols = df.select_dtypes(include=['object']).columns
    df[categorical_cols] = df[categorical_cols].fillna('Unknown')

    # Add source information
    df['source'] = source_name

    return df

# Process each file in the input directory
for filename in os.listdir(input_dir):
    file_path = os.path.join(input_dir, filename)

    if filename.endswith('.csv'):
        df = pd.read_csv(file_path)
    elif filename.endswith('.xlsx'):
        df = pd.read_excel(file_path)
    else:
        print(f"Unsupported file format: {filename}. Skipping.")
        continue

    source_name = filename.rsplit('.', 1)[0]
    cleaned_df = preprocess_df(df, source_name)
    output_file_path = os.path.join(output_dir, f'{source_name}_cleaned.csv')
    cleaned_df.to_csv(output_file_path, index=False)
    print(f"Processed and saved: {output_file_path}")

print("✅ Immigration policies data preprocessing complete.")
