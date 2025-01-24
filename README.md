# Mock Data Generator and Processor

This repository contains Python scripts for generating, processing, and downsizing large datasets for mock data generation and analysis. Each script serves a specific purpose, enabling efficient handling of large CSV files.

## File Overview

### 1. `main.py`
**Purpose:**  
Generates 1,000,000 rows of mock billing data for AWS services using a sample dataset and the Faker library.  
Key features include randomized costs, quantities, dates, and AWS-specific metadata.
This script is ideal for testing, simulations, or evaluating data processing workflows.

---

### 2. `gen.py`
**Purpose:**  
Generates large mock datasets for multiple cloud providers, including AWS, Google Cloud, Oracle, and Microsoft.  
Produces six months of data with configurable row counts and realistic metadata for billing, resource usage, and service details.  

---

### 3. `reduce.py`
**Purpose:**  
Reduces the size of a large CSV file by iteratively sampling rows to meet a target file size.  
Ensures a representative subset of the original data is created for use in smaller-scale testing or analysis.  

---

### 4. `extract.py`
**Purpose:**  
Extracts a random sample of rows from a large CSV file and saves them to a new file.  
Useful for quick sampling or creating smaller datasets for testing and debugging.  

---

## Notes

- Ensure the input CSV file paths are correctly updated in each script.
- Avoid committing large CSV files to the repository; they should be excluded using `.gitignore`.
- All scripts are designed for use with Python 3.7+ and require the `pandas` and `faker` libraries.
