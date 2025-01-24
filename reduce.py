"""
This script reduces the size of a large CSV file to a target size (e.g., 1.5 GB) 
by iteratively sampling rows. It reads the input file in chunks, samples rows 
based on an adjustable fraction, and writes the reduced dataset to an output file.

Key Features:
- Handles large files efficiently using chunked processing.
- Iteratively adjusts the sampling fraction to approximate the target file size.
- Outputs the reduced dataset as a new CSV file.

Usage:
1. Place the large CSV file in the same directory as the script and update the 
   `input_file` variable with its name.
2. Run the script to generate a reduced dataset (`mock-data-reduced.csv`).
3. Adjust the `target_size_bytes` variable to specify the desired output file size.

Dependencies:
- pandas
- os
"""

import pandas as pd
import os

# Input and output file paths
input_file = 'focus-data-full.csv'
output_file = 'mock-data-reduced.csv'

# Target file size in bytes (1.5 GB = 1.5 * 1024^3 bytes)
target_size_bytes = 1.5 * (1024 ** 3)

# Initial sampling size percentage (start with 10%)
sampling_fraction = 0.1

# Function to estimate file size iteratively
def downsize_file(input_file, output_file, target_size_bytes, initial_fraction=0.1):
    df_iter = pd.read_csv(input_file, chunksize=10**6)  # Process in chunks
    sampled_rows = []

    print("Sampling initial rows...")
    for chunk in df_iter:
        # Sample rows from each chunk based on the sampling fraction
        sampled_rows.append(chunk.sample(frac=initial_fraction))

    # Combine sampled rows into a single DataFrame
    sampled_df = pd.concat(sampled_rows)
    
    print("Saving sampled rows to temporary file for size estimation...")
    temp_file = 'temp_sample.csv'
    sampled_df.to_csv(temp_file, index=False)

    # Calculate the size of the sampled file
    temp_file_size = os.path.getsize(temp_file)
    print(f"Temporary file size: {temp_file_size / (1024 ** 3):.2f} GB")

    # Adjust the sampling fraction
    scaling_factor = target_size_bytes / temp_file_size
    final_fraction = initial_fraction * scaling_factor
    print(f"Adjusted sampling fraction: {final_fraction:.4f}")

    # Resample based on the adjusted fraction
    sampled_rows = []
    df_iter = pd.read_csv(input_file, chunksize=10**6)  # Reiterate through chunks
    for chunk in df_iter:
        sampled_rows.append(chunk.sample(frac=min(final_fraction, 1.0)))  # Cap at 1.0

    # Combine and save the final reduced DataFrame
    print("Saving final reduced file...")
    final_df = pd.concat(sampled_rows)
    final_df.to_csv(output_file, index=False)

    # Clean up the temporary file
    os.remove(temp_file)

    print(f"Reduced file saved to {output_file}")
    final_size = os.path.getsize(output_file) / (1024 ** 3)
    print(f"Final file size: {final_size:.2f} GB")

# Run the downsizing process
downsize_file(input_file, output_file, target_size_bytes)
