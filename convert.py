import pandas as pd

# Define file paths
csv_file = "go/mock-custom-dates-opt.csv"  # Output CSV from your Go script
parquet_file = "go/mock-custom-dates-opt.parquet"

# Load CSV into Pandas
df = pd.read_csv(csv_file, dtype=str)  # Read as strings to prevent dtype issues

# Save as Parquet
df.to_parquet(parquet_file, engine='pyarrow', index=False)

print(f"✅ Converted {csv_file} to {parquet_file}")
