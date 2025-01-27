"""
This script generates mock billing data with customizable date ranges. 
The date range can be adjusted directly in the script by setting the `start_date` and `end_date` variables.
The mock data includes realistic entries for cloud providers and is saved to a specified output CSV file.

Date Range:
- Specify the desired start and end dates for data generation.

Usage:
- Adjust `start_date` and `end_date` variables for the desired date range.
- Run the script to generate mock data for the defined date range.

Output:
- The generated data is saved in `mock_data_with_custom_date_range.csv`.
"""

import pandas as pd
from faker import Faker
import random
from datetime import datetime, timedelta

# Initialize Faker
fake = Faker()

# Input and output file paths
input_file = 'focus_sample_data.csv'
output_file = 'mock_data_with_custom_date_range.csv'

# Set the fixed date range
start_date = datetime(2023, 7, 1)  # Start of the date range
end_date = datetime(2023, 12, 31)  # End of the date range

# Number of rows per provider per month
rows_per_provider = 5000
providers = ["AWS", "Google Cloud", "Oracle", "Microsoft"]

# Function to generate a single mock row
def generate_mock_row(row, provider, current_date):
    row['ProviderName'] = provider
    row['BillingPeriodStart'] = current_date.strftime("%Y-%m-%d %H:%M:%S")
    row['BillingPeriodEnd'] = (current_date + timedelta(days=30)).strftime("%Y-%m-%d %H:%M:%S")
    row['BilledCost'] = round(random.uniform(0.01, 100), 2)
    row['ConsumedQuantity'] = round(random.uniform(0.1, 1000), 2)
    row['ServiceName'] = fake.random_element(elements=[
        'Amazon EC2', 'Google Cloud Storage', 'Oracle Database', 'Microsoft Azure Functions'
    ])
    row['RegionName'] = fake.random_element(elements=[
        'US East (N. Virginia)', 'EU (Frankfurt)', 'Asia Pacific (Singapore)', 'US West (Oregon)'
    ])
    return row

# Generate data for the specified date range
def generate_mock_data(input_file, output_file, start_date, end_date, rows_per_provider):
    # Read the input sample file
    df = pd.read_csv(input_file)

    # Calculate the number of months in the range
    all_rows = []
    current_date = start_date

    while current_date <= end_date:
        for provider in providers:
            for _ in range(rows_per_provider):
                random_row = df.iloc[random.randint(0, len(df) - 1)].copy()
                all_rows.append(generate_mock_row(random_row, provider, current_date))
        current_date += timedelta(days=30)  # Increment by one month

    # Create a new DataFrame and save to the output file
    output_df = pd.DataFrame(all_rows)
    output_df.to_csv(output_file, index=False)
    print(f"Mock data generated and saved to {output_file}")

# Run the script
generate_mock_data(input_file, output_file, start_date, end_date, rows_per_provider)
