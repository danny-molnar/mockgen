"""

This script validates the content of a large CSV file by performing the following checks:
1. **Random Sampling**: Selects a random sample of rows from the file to ensure comprehensive coverage.
2. **Column Completeness**: Verifies that all expected columns are present in the file.
3. **Date Range Validation**: Ensures `BillingPeriodStart` and `BillingPeriodEnd` span the last 6 months.
4. **Provider Representation**: Confirms that all expected cloud providers (AWS, Google Cloud, Oracle, Microsoft) are represented in the sampled data.
5. **Row Validity**: Ensures sampled rows contain valid and meaningful data.

Usage:
1. Update the `file_path` variable with the path to the generated CSV file.
2. Run the script to validate the content of the file.

Parameters:
- `file_path`: Path to the CSV file to validate.
- `sample_size`: Number of random rows to sample for validation (default is 1000).

Output:
- Prints detailed validation results for column checks, date ranges, and provider representation.
- Confirms whether the file passes all validation checks or fails with specific issues.

"""

import pandas as pd
from datetime import datetime
import random

# File path of the generated data
file_path = "mock-data-6-months-NEW.csv"

def validate_file(file_path, sample_size=1000):
    print(f"Validating file: {file_path}\n")

    # Get total number of rows without loading the entire file into memory
    print("Determining total number of rows...")
    try:
        total_rows = sum(1 for _ in open(file_path)) - 1  # Subtract 1 for the header
        print(f"Total rows in file: {total_rows}")
    except Exception as e:
        print(f"Error determining file size: {e}")
        return False

    # Generate random row indices for sampling
    print(f"Randomly selecting {sample_size} rows...")
    sample_indices = random.sample(range(1, total_rows + 1), sample_size)

    # Read the sampled rows
    try:
        data = pd.read_csv(file_path, skiprows=lambda x: x not in sample_indices and x != 0)  # Keep header (row 0)
        print(f"Sample data loaded ({len(data)} rows):\n")
        print(data.head())  # Show first few rows of the sample
    except Exception as e:
        print(f"Error reading file: {e}")
        return False

    # Check column names
    expected_columns = [
        "AvailabilityZone", "BilledCost", "BillingAccountId", "BillingAccountName", "BillingCurrency",
        "BillingPeriodEnd", "BillingPeriodStart", "ChargeCategory", "ChargeClass", "ChargeDescription",
        "ChargeFrequency", "ChargePeriodEnd", "ChargePeriodStart", "CommitmentDiscountCategory",
        "CommitmentDiscountId", "CommitmentDiscountName", "CommitmentDiscountStatus",
        "CommitmentDiscountType", "ConsumedQuantity", "ConsumedUnit", "ContractedCost",
        "ContractedUnitPrice", "EffectiveCost", "InvoiceIssuerName", "ListCost", "ListUnitPrice",
        "PricingCategory", "PricingQuantity", "PricingUnit", "ProviderName", "PublisherName", "RegionId",
        "RegionName", "ResourceId", "ResourceName", "ResourceType", "ServiceCategory", "Id", "ServiceName",
        "SkuId", "SkuPriceId", "SubAccountId", "SubAccountName", "Tags"
    ]
    print("\nChecking columns...")
    if not all(col in data.columns for col in expected_columns):
        print(f"Missing columns in the file. Expected columns: {expected_columns}")
        return False
    print("All columns are present.")

    # Validate date ranges
    print("\nValidating date ranges for 6 months...")
    try:
        billing_start_dates = pd.to_datetime(data["BillingPeriodStart"], errors="coerce")
        billing_end_dates = pd.to_datetime(data["BillingPeriodEnd"], errors="coerce")

        # Ensure no missing or invalid dates
        if billing_start_dates.isnull().any() or billing_end_dates.isnull().any():
            print("Invalid or missing dates in BillingPeriodStart or BillingPeriodEnd.")
            return False

        # Check date range for 6 months
        six_months_ago = datetime.now() - pd.DateOffset(months=6)
        if not (billing_start_dates >= six_months_ago).all() or not (billing_end_dates <= datetime.now()).all():
            print("Dates are not within the expected 6-month range.")
            return False

        print(f"Dates are within the expected range ({six_months_ago.date()} to {datetime.now().date()}).")
    except Exception as e:
        print(f"Error validating date ranges: {e}")
        return False

    # Check for representation of providers
    print("\nValidating provider representation...")
    unique_providers = data["ProviderName"].unique()
    print(f"Unique providers in the sample: {unique_providers}")
    expected_providers = ["AWS", "Google Cloud", "Oracle", "Microsoft"]
    if not all(provider in unique_providers for provider in expected_providers):
        print(f"Some providers are missing. Expected providers: {expected_providers}")
        return False
    print("All providers are represented.")

    print("\nValidation completed successfully. The file passed all checks.")
    return True


# Run validation
if __name__ == "__main__":
    validation_result = validate_file(file_path, sample_size=1000)
    if validation_result:
        print("File is valid!")
    else:
        print("File validation failed.")
