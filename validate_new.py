import pandas as pd
from datetime import datetime

# File path of the generated data
file_path = "mock-data-6-months-NEW.csv"

def validate_file(file_path, sample_size=2000):
    print(f"Validating file: {file_path}\n")

    # Load a sample of the data
    print("Loading sample rows...")
    try:
        data = pd.read_csv(file_path, nrows=sample_size)
        print(f"Sample data:\n{data}\n")
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
    print("Checking columns...")
    if not all(col in data.columns for col in expected_columns):
        print(f"Missing columns in the file. Expected columns: {expected_columns}")
        return False
    print("All columns are present.")

    # Check date ranges
    print("Validating date ranges for 6 months...")
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
    print("Validating provider representation...")
    unique_providers = data["ProviderName"].unique()
    print(f"Unique providers in the file: {unique_providers}")
    expected_providers = ["AWS", "Google Cloud", "Oracle", "Microsoft"]
    if not all(provider in unique_providers for provider in expected_providers):
        print(f"Some providers are missing. Expected providers: {expected_providers}")
        return False
    print("All providers are represented.")

    # Check for non-zero rows
    print("Checking for non-zero rows...")
    if len(data) == 0:
        print("The file contains no rows.")
        return False
    print(f"The file contains {len(data)} rows.")

    print("\nValidation completed successfully. The file passed all checks.")
    return True


# Run validation
if __name__ == "__main__":
    validation_result = validate_file(file_path)
    if validation_result:
        print("File is valid!")
    else:
        print("File validation failed.")
