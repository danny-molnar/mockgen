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

### 5. `gen_6_month_mock_data.py`
**Purpose**:  
Generates a mock dataset for billing and usage data spanning 6 months. The script ensures balanced representation of major cloud providers (AWS, Google Cloud, Oracle, Microsoft) and realistic data distribution.

**Key Features**:
- Reads data from a one-month source file.
- Expands the data across 6 months, maintaining provider balance.
- Utilizes multiprocessing for efficient processing of large datasets.

**Input**:
- A single-month dataset in CSV format.

**Output**:
- A 6-month dataset in CSV format.

---

### 6. `validate_new.py`
**Purpose**:  
Validates the content of a large CSV file to ensure it meets expected standards.

**Key Features**:
- Randomly samples rows for validation.
- Checks for the presence of all required columns.
- Validates date ranges for a 6-month period.
- Ensures all major cloud providers are represented.

---

## Sample Dataset
All scripts are based on the FOCUS Sample Dataset for FinOps cost and usage data.  
The dataset can be found [here](https://github.com/FinOps-Open-Cost-and-Usage-Spec/FOCUS-Sample-Data/tree/main/FOCUS-1.0).

---

## Notes

- Ensure the input CSV file paths are correctly updated in each script.
- All scripts are designed for use with Python 3.7+ and require the `pandas` and `faker` libraries.
