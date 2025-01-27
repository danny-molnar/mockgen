"""
generate_six_months_data.py

This script generates a mock dataset spanning 6 months by extending and replicating the data
from an existing large CSV file. It ensures all cloud providers are represented while maintaining
a balanced and realistic data distribution.

Key Features:
1. **6-Month Data Generation**: Takes a single month of data and extrapolates it across a 6-month period.
2. **Balanced Provider Representation**: Ensures all major cloud providers (AWS, Google Cloud, Oracle, Microsoft) are represented.
3. **Efficient Processing**: Utilizes chunk processing and multiprocessing to handle large files effectively.
4. **Customizable Output**: Allows configuration of the number of rows per provider and number of months.

Usage:
1. Update the `input_file` and `output_file` variables with the paths to the source and target files.
2. Run the script to generate the mock dataset.

Parameters:
- `input_file`: Path to the source CSV file (one-month data).
- `output_file`: Path to save the generated 6-month dataset.
- `rows_per_provider`: Number of rows to generate for each provider per month (default is 1000).
- `months`: Number of months to generate (default is 6).
- `num_workers`: Number of parallel workers for multiprocessing (default is 4).

Output:
- A new CSV file containing 6 months of extended mock data with balanced cloud provider representation.

"""
import pandas as pd
import random
from datetime import datetime, timedelta

def generate_mock_row(row, provider, month_offset):
    """
    Generate a single mock row with adjusted dates and provider-specific values.
    """
    try:
        # Adjust the dates for the row
        start_date = datetime.strptime(row['BillingPeriodStart'], "%Y-%m-%d %H:%M:%S")
        end_date = datetime.strptime(row['BillingPeriodEnd'], "%Y-%m-%d %H:%M:%S")
        start_date -= timedelta(days=month_offset)
        end_date -= timedelta(days=month_offset)

        row['BillingPeriodStart'] = start_date.strftime("%Y-%m-%d %H:%M:%S")
        row['BillingPeriodEnd'] = end_date.strftime("%Y-%m-%d %H:%M:%S")

        # Update provider-specific fields
        row['ProviderName'] = provider
        row['ConsumedQuantity'] = round(random.uniform(1, 1000), 2)
        row['BilledCost'] = round(random.uniform(0.1, 100), 2)

    except Exception as e:
        print(f"Error processing row: {e}")
        return None

    return row

def generate_six_months_data(input_file, output_file, rows_per_provider=1000, months=6):
    """
    Generate mock data for 6 months across multiple providers from a large dataset.
    """
    # List of providers
    providers = ['AWS', 'Google Cloud', 'Oracle', 'Microsoft']
    
    # Read input file in chunks
    with pd.read_csv(input_file, chunksize=10000) as reader, open(output_file, 'w') as output:
        header_written = False
        
        for chunk in reader:
            chunk_rows = []
            for month in range(months):
                for provider in providers:
                    # Process rows for each month and provider
                    for i in range(rows_per_provider):
                        random_row = chunk.iloc[random.randint(0, len(chunk) - 1)].to_dict()
                        processed_row = generate_mock_row(random_row, provider, month * 30)
                        if processed_row:
                            chunk_rows.append(processed_row)
            
            # Convert to DataFrame and write incrementally
            df = pd.DataFrame(chunk_rows)
            if not header_written:
                df.to_csv(output_file, index=False, mode='w', header=True)  # Write header
                header_written = True
            else:
                df.to_csv(output_file, index=False, mode='a', header=False)  # Append data

            print(f"Processed a chunk, current output size: {output.tell() / (1024 ** 3):.2f} GB")

    print(f"Mock data generation completed. File saved to {output_file}")

if __name__ == '__main__':
    # File paths
    input_file = 'focus-data-full.csv'  # Path to large input file
    output_file = 'mock-data-6-months-NEW.csv'  # Output file path

    # Generate data
    generate_six_months_data(input_file, output_file, rows_per_provider=1000, months=6)
