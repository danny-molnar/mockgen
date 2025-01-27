"""
Use this to extract a random sample of rows from the input CSV file 
and save it to a new CSV file. You can adjust the number of rows to extract
"""

import csv
import random

def extract_random_rows(input_file, output_file, num_rows=1000):
    """
    Extract a random selection of rows (excluding the header) from a large CSV file.
    """
    with open(input_file, 'r') as infile:
        reader = list(csv.reader(infile))
        header, rows = reader[0], reader[1:]
        
        # Randomly sample rows
        sampled_rows = random.sample(rows, num_rows)
        
        # Write to a new CSV file
        with open(output_file, 'w', newline='') as outfile:
            writer = csv.writer(outfile)
            writer.writerow(header)  # Write the header
            writer.writerows(sampled_rows)  # Write the sampled rows

    print(f"Extracted {num_rows} random rows to {output_file}.")

input_csv = "focus-data-full.csv"
output_csv = "random_sample.csv"

# Extract 1000 random rows
extract_random_rows(input_csv, output_csv, num_rows=1000)
