"""
This script generates 1,000,000 rows of mock billing data for AWS services
using a sample dataset and the Faker library. It modifies key columns 
with random and realistic values such as costs, quantities, dates, and 
AWS-specific metadata. The generated data is saved to a CSV file 
(focus-mock-data-1M.csv) and can be used for testing, simulations, 
or performance evaluation of data processing workflows.

Usage:
1. Ensure the sample dataset file (focus_sample-data-new.csv) exists.
2. Run the script to generate a new CSV file with mock data.

Adjust the `num_rows` variable to control the size of the output dataset.
"""

import pandas as pd
from faker import Faker
import random

# Initialize Faker
fake = Faker()

# Read the sample data
input_file = 'focus_sample-data-new.csv'
df = pd.read_csv(input_file)

# Function to generate mock data
def generate_mock_data(row):
    row['AvailabilityZone'] = fake.random_element(elements=('us-east-1', 'us-west-2', 'eu-central-1'))
    row['BilledCost'] = round(random.uniform(0, 1), 10)
    row['BillingAccountId'] = fake.random_number(digits=13, fix_len=True)
    row['BillingAccountName'] = fake.company()
    row['BillingCurrency'] = 'USD'
    row['BillingPeriodEnd'] = fake.date_time_this_year()
    row['BillingPeriodStart'] = fake.date_time_this_year()
    row['ChargeCategory'] = 'Usage'
    row['ChargeDescription'] = fake.sentence(nb_words=6)
    row['ChargeFrequency'] = 'Usage-Based'
    row['ChargePeriodEnd'] = fake.date_time_this_year()
    row['ChargePeriodStart'] = fake.date_time_this_year()
    row['ConsumedQuantity'] = round(random.uniform(0, 10), 10)
    row['ConsumedUnit'] = fake.random_element(elements=('Requests', 'GB', 'Hours'))
    row['ContractedCost'] = round(random.uniform(0, 1), 10)
    row['EffectiveCost'] = round(random.uniform(0, 1), 10)
    row['InvoiceIssuerName'] = 'Amazon Web Services, Inc.'
    row['ListCost'] = round(random.uniform(0, 1), 10)
    row['ListUnitPrice'] = round(random.uniform(0, 1), 10)
    row['PricingCategory'] = 'Standard'
    row['PricingQuantity'] = round(random.uniform(0, 10), 10)
    row['PricingUnit'] = fake.random_element(elements=('Requests', 'GB', 'Hours'))
    row['ProviderName'] = 'AWS'
    row['PublisherName'] = 'Amazon Web Services, Inc.'
    row['RegionId'] = fake.random_element(elements=('us-west-2', 'us-east-1', 'eu-central-1'))
    row['RegionName'] = fake.random_element(elements=('US West (Oregon)', 'US East (N. Virginia)', 'EU (Frankfurt)'))
    row['ResourceId'] = fake.uuid4()
    row['ResourceName'] = fake.word()
    row['ResourceType'] = fake.random_element(elements=('Compute', 'Storage', 'Networking'))
    row['ServiceCategory'] = fake.random_element(elements=('Integration', 'Compute', 'Storage'))
    row['ServiceName'] = fake.random_element(elements=('Amazon Simple Queue Service', 'Elastic Load Balancing', 'Amazon Elastic Compute Cloud'))
    row['SkuId'] = fake.uuid4()
    row['SkuPriceId'] = fake.uuid4()
    row['SubAccountId'] = fake.random_number(digits=11, fix_len=True)
    row['SubAccountName'] = fake.company()
    row['Tags'] = fake.json()
    return row

# Generate 1,000,000 rows of data
num_rows = 1000000

# Create new DataFrame with generated data
new_data = pd.DataFrame([generate_mock_data(df.iloc[random.randint(0, len(df) - 1)].copy()) for _ in range(num_rows)])

# Save to new CSV file
output_file = 'focus-mock-data-1M.csv'
new_data.to_csv(output_file, index=False)

print(f"Generated {num_rows} rows of mock data and saved to {output_file}")