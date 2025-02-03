# Mock CSV Data Generator

This tool reads an input CSV file and generates a new CSV file with mock data. It leverages concurrency (via Go goroutines) to speed up the data generation process. The generated CSV contains modified data based on a template row from the input CSV file, with fields such as dates, provider names, random numeric values, and fake location/job information.

## Features

- **Concurrent Processing:** Uses multiple goroutines to generate data in parallel.
- **Batch Writing:** Writes rows in batches to improve performance.
- **Customizable Configuration:** Easily adjust date ranges, rows per provider, and the number of workers.
- **Randomized Data:** Uses the `gofakeit` library to generate realistic fake data.

## How It Works

1. **Input CSV Reading:**
   The program reads a CSV file (default path: `../focus-data-full.csv`) that contains a header and data rows.

2. **Mock Data Generation:**
   For each row, the program generates mock data by:
   - Changing the provider information.
   - Assigning new billing start and end dates.
   - Generating random numeric values and fake data (like city names and job descriptors).

3. **Concurrent Workers:**
   A pool of worker goroutines processes rows concurrently. Each worker receives rows from a job channel, processes them, and sends the results to a results channel.

4. **Batch CSV Writing:**
   The main routine collects generated rows and writes them in batches to an output file (`mock-custom-dates-opt.csv`).

## Prerequisites

### Option 1: Using `go run` (No Go Installation Required via Binary)

For macOS users who may not have Go installed, you can run the code using [Go Playground](https://play.golang.org/) or use a precompiled binary. However, if you choose to run the code directly, follow Option 2 below.

### Option 2: Running with Go Installed

1. **Install Go:**
   - Download and install Go from the [official website](https://golang.org/dl/).

2. **Download the Source Code:**
   - Clone the repository or download the source files containing `main.go`.

3. **Fetch Dependencies:**
   - Open Terminal and navigate to the project directory.
   - Run:
     ```bash
     go mod tidy
     ```
     This command downloads the necessary dependencies (including `github.com/brianvoe/gofakeit/v6`).

4. **Run the Program:**
   - Ensure the input CSV file is available at the expected path (`../focus-data-full.csv` by default).
     *Tip:* You can modify the `inputFile` constant in the source code if you wish to use a different path.
   - Execute the program by running:
     ```bash
     go run main.go
     ```
   - The output file `mock-custom-dates-opt.csv` will be generated in the same directory as the binary.

## Configuration

Inside the source code, you can adjust the following constants to suit your needs:

- `inputFile`: Path to the input CSV file.
- `outputFilePath`: Path for the output CSV file.
- `startDateStr` & `endDateStr`: Date range for generating billing periods.
- `rowsPerProvider`: Total rows to generate per provider.
- `numWorkers`: Number of concurrent goroutines.
- `bufferSize`: Number of rows to write per batch.

Feel free to modify these values before running the program.

## Troubleshooting

- **Input File Not Found:**
  Ensure the input CSV file exists at the specified location (`../focus-data-full.csv` by default). Modify the `inputFile` constant if necessary.

- **Dependency Issues:**
  If you encounter missing dependencies when running the code, run `go mod tidy` to fetch them.

- **Permission Errors:**
  If you are using a precompiled binary, make sure it has execute permissions:
  ```bash
  chmod +x mock-data-generator
