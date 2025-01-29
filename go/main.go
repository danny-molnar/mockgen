package main

import (
	"encoding/csv"
	"fmt"
	"log"
	"math/rand"
	"os"
	"strconv"
	"sync"
	"time"

	"github.com/brianvoe/gofakeit/v6"
)

// Configuration
const (
	inputFile       = "../focus-data-full.csv"
	outputFilePath  = "mock-custom-dates-opt.csv"
	startDateStr    = "2024-07-01"
	endDateStr      = "2024-12-31"
	rowsPerProvider = 300000
	numWorkers      = 16   // Number of Goroutines
	bufferSize      = 5000 // Number of rows to write per batch
)

// Providers list
var providers = []string{"AWS", "Google Cloud", "Oracle", "Microsoft"}

// Converts date string to time.Time
func parseDate(dateStr string) time.Time {
	layout := "2006-01-02"
	t, err := time.Parse(layout, dateStr)
	if err != nil {
		log.Fatalf("Error parsing date: %v", err)
	}
	return t
}

// Generates a random mock data row
func generateMockRow(provider string, currentDate time.Time, rowTemplate []string) []string {
	row := make([]string, len(rowTemplate))
	copy(row, rowTemplate)

	row[2] = provider                                                               // ProviderName
	row[5] = currentDate.Format("2006-01-02 15:04:05")                              // BillingPeriodStart
	row[6] = currentDate.AddDate(0, 1, 0).Format("2006-01-02 15:04:05")             // BillingPeriodEnd
	row[8] = strconv.FormatFloat(rand.Float64()*100, 'f', 2, 64)                    // BilledCost
	row[18] = strconv.FormatFloat(rand.Float64()*1000, 'f', 2, 64)                  // ConsumedQuantity
	row[20] = providers[rand.Intn(len(providers))]                                  // ServiceName
	row[21] = gofakeit.City()                                                       // RegionName
	row[22] = gofakeit.JobDescriptor()                                              // ChargeCategory
	row[23] = gofakeit.Sentence(6)                                                  // ChargeDescription
	row[24] = gofakeit.RandomString([]string{"Usage-Based", "Monthly", "One-Time"}) // ChargeFrequency
	row[25] = strconv.FormatFloat(rand.Float64()*100, 'f', 2, 64)                   // ContractedCost
	row[26] = strconv.FormatFloat(rand.Float64()*100, 'f', 2, 64)                   // EffectiveCost
	row[27] = provider                                                              // InvoiceIssuerName
	row[28] = strconv.FormatFloat(rand.Float64()*100, 'f', 2, 64)                   // ListCost
	row[29] = strconv.FormatFloat(rand.Float64()*100, 'f', 2, 64)                   // ListUnitPrice
	row[30] = gofakeit.RandomString([]string{"Standard", "Premium"})                // PricingCategory
	row[31] = strconv.FormatFloat(rand.Float64()*10, 'f', 2, 64)                    // PricingQuantity
	row[32] = gofakeit.RandomString([]string{"Requests", "GB", "Hours"})            // PricingUnit
	row[33] = provider                                                              // PublisherName

	return row
}

// Worker function to generate mock data
func worker(id int, wg *sync.WaitGroup, jobs <-chan []string, results chan<- []string, startDate time.Time, endDate time.Time) {
	defer wg.Done()
	currentDate := startDate

	for currentDate.Before(endDate) {
		for _, provider := range providers {
			for i := 0; i < rowsPerProvider/numWorkers; i++ {
				row, ok := <-jobs
				if !ok {
					return // Stop worker when jobs channel is closed
				}
				results <- generateMockRow(provider, currentDate, row)
			}
		}
		currentDate = currentDate.AddDate(0, 1, 0) // Move to next month
	}
}

// Main function
func main() {
	startDate := parseDate(startDateStr)
	endDate := parseDate(endDateStr)

	// Open input file
	file, err := os.Open(inputFile)
	if err != nil {
		log.Fatalf("Failed to open input file: %v", err)
	}
	defer file.Close()

	reader := csv.NewReader(file)
	header, err := reader.Read() // Read header
	if err != nil {
		log.Fatalf("Failed to read header: %v", err)
	}

	// Open output file
	outputFile, err := os.Create(outputFilePath)
	if err != nil {
		log.Fatalf("Failed to create output file: %v", err)
	}
	defer outputFile.Close()
	writer := csv.NewWriter(outputFile)

	// Write header to output
	writer.Write(header)
	writer.Flush()

	// Channels for processing
	jobs := make(chan []string, numWorkers)
	results := make(chan []string, bufferSize)

	// Worker pool
	var wg sync.WaitGroup
	for w := 0; w < numWorkers; w++ {
		wg.Add(1)
		go worker(w, &wg, jobs, results, startDate, endDate)
	}

	// Read the input file and send jobs
	go func() {
		for {
			row, err := reader.Read()
			if err != nil {
				break
			}
			jobs <- row
		}
		close(jobs) // ✅ Close jobs channel when all rows are read
	}()

	// Collect results and write to CSV in batches
	totalRows := 0
	buffer := [][]string{}

	go func() {
		for row := range results {
			buffer = append(buffer, row)
			totalRows++

			if len(buffer) >= bufferSize {
				writer.WriteAll(buffer)
				writer.Flush()
				buffer = buffer[:0] // Clear buffer
				fmt.Printf("Written %d rows so far...\n", totalRows)
			}
		}

		// Write remaining buffered rows
		if len(buffer) > 0 {
			writer.WriteAll(buffer)
			writer.Flush()
		}

		fmt.Printf("✅ Generated %d rows of mock data and saved to %s\n", totalRows, outputFilePath)
	}()

	wg.Wait()      // ✅ Ensure all workers complete before proceeding
	close(results) // ✅ Close results channel after workers are done
}
