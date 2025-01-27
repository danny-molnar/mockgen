"""
This script generates mock data for various cloud providers (AWS, Google Cloud, Oracle, and Microsoft) using a sample dataset. 
It creates six months of billing data, including information such as billing periods, resource types, costs, and other metadata. 
The script is designed to produce realistic data by leveraging the Faker library and the input sample dataset.
"""

import pandas as pd
from faker import Faker
import random
from datetime import datetime, timedelta

# Initialize Faker
fake = Faker()

# Read the sample data
input_file = 'focus-data-full.csv'
df = pd.read_csv(input_file)

# Function to generate mock data for various providers
def generate_mock_data(row, provider, month_start, month_end):
    row['AvailabilityZone'] = fake.random_element(elements=('us-east-1', 'us-west-2', 'eu-central-1', 'europe-west3', 'asia-southeast1'))
    row['BilledCost'] = round(random.uniform(0, 100), 10)
    row['BillingAccountId'] = fake.random_number(digits=13, fix_len=True)
    row['BillingAccountName'] = fake.company()
    row['BillingCurrency'] = 'USD'

    # Use the specified month range for BillingPeriod and ChargePeriod
    billing_start = month_start
    billing_end = month_end
    row['BillingPeriodStart'] = billing_start.strftime("%Y-%m-%d %H:%M:%S")
    row['BillingPeriodEnd'] = billing_end.strftime("%Y-%m-%d %H:%M:%S")
    row['ChargePeriodStart'] = billing_start.strftime("%Y-%m-%d %H:%M:%S")
    row['ChargePeriodEnd'] = billing_end.strftime("%Y-%m-%d %H:%M:%S")

    row['ChargeCategory'] = 'Usage'
    row['ChargeDescription'] = fake.sentence(nb_words=6)
    row['ChargeFrequency'] = 'Usage-Based'
    row['ConsumedQuantity'] = round(random.uniform(0, 1000), 10)
    row['ConsumedUnit'] = fake.random_element(elements=('Requests', 'GB', 'Hours'))
    row['ContractedCost'] = round(random.uniform(0, 100), 10)
    row['EffectiveCost'] = round(random.uniform(0, 100), 10)

    # Add provider-specific details
    if provider == "AWS":
        row['InvoiceIssuerName'] = 'Amazon Web Services, Inc.'
        row['ProviderName'] = 'AWS'
        row['PublisherName'] = 'Amazon Web Services, Inc.'
    elif provider == "Google Cloud":
        row['InvoiceIssuerName'] = 'Google Cloud'
        row['ProviderName'] = 'Google Cloud'
        row['PublisherName'] = 'Google Cloud'
    elif provider == "Oracle":
        row['InvoiceIssuerName'] = 'Oracle'
        row['ProviderName'] = 'Oracle'
        row['PublisherName'] = 'Oracle'
    elif provider == "Microsoft":
        row['InvoiceIssuerName'] = 'Microsoft'
        row['ProviderName'] = 'Microsoft'
        row['PublisherName'] = 'Microsoft'

    row['RegionId'] = fake.random_element(elements=('us-west-2', 'us-east-1', 'eu-central-1', 'asia-east1'))
    row['RegionName'] = fake.random_element(elements=('US West (Oregon)', 'US East (N. Virginia)', 'EU (Frankfurt)', 'Asia East'))
    row['ResourceId'] = fake.uuid4()
    row['ResourceName'] = fake.word()
    row['ResourceType'] = fake.random_element(elements=('Compute', 'Storage', 'Networking'))
    row['ServiceCategory'] = fake.random_element(elements=('Integration', 'Compute', 'Storage'))
    row['ServiceName'] = fake.random_element(elements=(
        'Amazon Simple Queue Service',
        'Elastic Load Balancing',
        'Amazon Elastic Compute Cloud',
        'Google Cloud Storage',
        'Microsoft Azure Data Lake',
        'Oracle Autonomous Database'
    ))
    row['SkuId'] = fake.uuid4()
    row['SkuPriceId'] = fake.uuid4()
    row['SubAccountId'] = fake.random_number(digits=11, fix_len=True)
    row['SubAccountName'] = fake.company()
    row['Tags'] = fake.json()
    return row

# Generate six months of data with multiple providers
def generate_six_months_data(output_file, rows_per_month=100000, months=6, preview=False):
    providers = ["AWS", "Google Cloud", "Oracle", "Microsoft"]
    all_data = []

    # Calculate the start and end dates for the last six months
    today = datetime.now()
    for month in range(months):
        month_end = today - timedelta(days=month * 30)
        month_start = month_end - timedelta(days=29)  # Assume 30-day months for simplicity

        if not preview:
            print(f"Generating data for period {month_start.strftime('%Y-%m-%d')} to {month_end.strftime('%Y-%m-%d')}...")

        for _ in range(rows_per_month):
            provider = random.choice(providers)
            # Pick a random row from the sample dataset to base the new row on
            sample_row = df.iloc[random.randint(0, len(df) - 1)].copy()
            new_row = generate_mock_data(sample_row, provider, month_start, month_end)
            all_data.append(new_row)

        # If in preview mode, stop after the first month and show a few rows
        if preview:
            break

    # Convert the data into a DataFrame
    new_data = pd.DataFrame(all_data)

    if preview:
        print("\n*** Preview of Mock Data ***")
        print(new_data.head(10))  # Display the first 10 rows
        print("\nRun the script in full mode to generate the entire dataset.")
        return

    # Save to CSV
    new_data.to_csv(output_file, index=False)
    print(f"Generated six months of data ({len(new_data)} rows) and saved to {output_file}")

# Run the script
output_file = 'mock-data-6-months.csv'

# Set preview to True to see sample rows
generate_six_months_data(output_file, rows_per_month=100000, months=6, preview=False)
