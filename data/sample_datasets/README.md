# Sample Datasets for DS-Tutor

This directory contains real sample datasets used in DS-Tutor lessons. These files help students learn to work with actual data files rather than simulated in-memory data.

## Available Datasets

### CSV Files (Comma-Separated)

1. **employees.csv** - Employee information
   - Columns: Name, Age, City, Salary, Department
   - 10 records
   - Use cases: Basic data loading, filtering, grouping

2. **sales.csv** - Sales transactions
   - Columns: Date, Product, Quantity, Price, Region
   - 10 records
   - Use cases: Date handling, aggregations, revenue calculations

3. **products.csv** - Product catalog
   - Columns: ProductID, ProductName, Category, Price, InStock
   - 8 records
   - Use cases: Filtering, categorical data, lookups

4. **students.csv** - Student records
   - Columns: StudentID, Name, Major, GPA, Year
   - 8 records
   - Use cases: Sorting, filtering, statistical analysis

5. **weather.csv** - Weather data
   - Columns: Date, City, Temperature, Humidity, Precipitation
   - 9 records
   - Use cases: Time series, multi-index, pivoting

6. **survey_data.csv** - Survey responses
   - Columns: RespondentID, Age, Gender, Satisfaction, City, Income
   - 8 records
   - Use cases: Missing data, demographic analysis

### TSV Files (Tab-Separated)

7. **employees.tsv** - Employee data (tab-delimited)
   - Same structure as employees.csv but tab-separated
   - 5 records
   - Use cases: Learning different delimiters

### Pipe-Delimited Files

8. **inventory.txt** - Inventory data (pipe-delimited)
   - Columns: Item, Quantity, Price, Supplier
   - 6 records
   - Use cases: Custom delimiters

### JSON Files

9. **products.json** - Product data in JSON format
   - 3 records with nested specifications
   - Use cases: JSON reading, nested data structures

## File Locations

All files are located in: `E:\dstutor\data\sample_datasets\`

For portable path handling in lessons, use:
```python
import os
from pathlib import Path

# Get the data directory
data_dir = Path(__file__).parent.parent.parent / 'data' / 'sample_datasets'

# Or use relative path from notebooks directory
data_dir = Path('../data/sample_datasets')
```

## Usage in Lessons

These datasets are referenced in:
- pandas_04: Loading and Saving Data
- pandas_05: GroupBy operations
- pandas_09: Merging DataFrames
- And other intermediate/advanced lessons

## Data Quality

All datasets:
- Are clean and ready to use (unless specifically designed to teach data cleaning)
- Have realistic but fictional data
- Are small enough for quick loading and iteration
- Demonstrate common data patterns and structures
