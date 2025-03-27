import os
import pandas as pd
import requests

# Get the absolute path of the directory containing the script
script_dir = os.path.dirname(os.path.abspath(__file__))

# Construct absolute paths
input_dir = os.path.join(script_dir, '../data/dirty/cost-of-living-indexes')
output_dir = os.path.join(script_dir, '../data/clean/cost-of-living-indexes')
os.makedirs(output_dir, exist_ok=True)

# Function to fetch current exchange rates
def get_exchange_rate(from_currency, to_currency='USD'):
    # Example using a placeholder for exchange rate retrieval
    # Replace with actual API call and parsing as needed
    exchange_rates = {
        'USD': 1.0,
        'GBP': 1.27,  # Example: 1 GBP = 1.27 USD
        'CAD': 0.74,  # Example: 1 CAD = 0.74 USD
        'EUR': 1.09,  # Example: 1 EUR = 1.09 USD
    }
    return exchange_rates.get(from_currency.upper(), None)

# Function to normalize currency values
def normalize_currency(value, currency):
    try:
        exchange_rate = get_exchange_rate(currency)
        if exchange_rate is None:
            print(f"Warning: Exchange rate for {currency} not found. Skipping normalization.")
            return None
        return float(value) * exchange_rate
    except Exception as e:
        print(f"Error normalizing currency: {e}")
        return None

# Function to preprocess each DataFrame
def preprocess_df(df, source_name):
    # Drop completely empty rows and columns
    df.dropna(how='all', inplace=True)
    df.dropna(axis=1, how='all', inplace=True)

    # Standardize column names
    df.columns = [col.strip().lower().replace(' ', '_') for col in df.columns]

    # Normalize currency columns
    for col in df.columns:
        if 'cost' in col or 'price' in col or 'rent' in col:
            # Assuming there's a 'currency' column indicating the currency type
            if 'currency' in df.columns:
                df[col] = df.apply(lambda row: normalize_currency(row[col], row['currency']), axis=1)
            else:
                # If no currency column, assume values are already in USD or handle accordingly
                pass

    # Add source and phase tags
    df['source'] = source_name
    df['phase'] = 'pre_departure'

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

print("✅ Cost-of-living data preprocessing complete.")
