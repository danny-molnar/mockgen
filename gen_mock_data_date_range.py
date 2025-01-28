"""
This script generates mock billing data with customizable date ranges. 
The date range can be adjusted directly in the script by setting the `start_date` and `end_date` variables.
The mock data includes realistic entries for cloud providers and is saved to a specified output CSV file.

Date Range:
- Specify the desired start and end dates for data generation.

Usage:
- Provide the input file path containing the original data and the output file path for the generated mock data.
- Adjust `start_date` and `end_date` variables for the desired date range.
- Adjust `rows_per_provider` variable for the number of rows per provider per month.
- Run the script to generate mock data for the defined date range.

"""

import pandas as pd
from faker import Faker
import random
from datetime import datetime, timedelta

# Initialize Faker
fake = Faker()

# Input and output file paths
input_file = 'focus-data-full.csv'
output_file = 'mock-custom-dates.csv'

# Define the date range and number of rows per provider
start_date = datetime(2024, 7, 1)
end_date = datetime(2024, 12, 31)
rows_per_provider = 40000

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
    row['ChargeCategory'] = 'Usage'
    row['ChargeDescription'] = fake.sentence(nb_words=6)
    row['ChargeFrequency'] = fake.random_element(elements=['Usage-Based', 'Monthly', 'One-Time'])
    row['ContractedCost'] = round(random.uniform(0, 100), 2)
    row['EffectiveCost'] = round(random.uniform(0, 100), 2)
    row['InvoiceIssuerName'] = provider
    row['ListCost'] = round(random.uniform(0, 100), 2)
    row['ListUnitPrice'] = round(random.uniform(0, 100), 2)
    row['PricingCategory'] = 'Standard'
    row['PricingQuantity'] = round(random.uniform(0, 10), 2)
    row['PricingUnit'] = fake.random_element(elements=['Requests', 'GB', 'Hours'])
    row['PublisherName'] = provider
    return row

# Function to generate mock data for the specified date range
def generate_mock_data(input_file, output_file, start_date, end_date, rows_per_provider):
    # Read the input file
    df = pd.read_csv(input_file, low_memory=False, dtype=str)
    
    # Initialize an empty list for the output
    output_data = []
    
    # Generate data for each provider and each month in the date range
    providers = ["AWS", "Google Cloud", "Oracle", "Microsoft"]
    current_date = start_date
    total_rows = 0
    while current_date <= end_date:
        for provider in providers:
            for _ in range(rows_per_provider):
                try:
                    row = df.sample(n=1).iloc[0].to_dict()
                    mock_row = generate_mock_row(row, provider, current_date)
                    output_data.append(mock_row)
                    total_rows += 1
                    if total_rows % 1000 == 0:
                        print(f"Generated {total_rows} rows so far...")
                except Exception as e:
                    print(f"Error generating row: {e}")
        current_date += timedelta(days=30)
    
    # Convert the list to a DataFrame and save the generated data to the output file
    output_df = pd.DataFrame(output_data)
    output_df.to_csv(output_file, index=False)
    print(f"Generated {total_rows} rows of mock data and saved to {output_file}")

# Run the script
generate_mock_data(input_file, output_file, start_date, end_date, rows_per_provider)
