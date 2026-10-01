# Sales & Revenue Analysis Dashboard

An interactive sales and revenue analytics dashboard built with Python, Pandas, Plotly, and Streamlit for the Thiranex Data Analytics internship project.

## 🚀 Live Demo

[Open Live Dashboard](https://salesrevenueanalysisdashboard.streamlit.app/)

## Project Overview

This project analyzes the UCI Online Retail transaction dataset and presents the results through an interactive dashboard.

The dashboard supports:

- Sales and revenue KPI tracking
- Monthly revenue and order analysis
- Top-performing product analysis
- Geographic revenue analysis
- Interactive filtering
- Transaction-level exploration
- Filtered data export
- Business insight generation

## Internship Task

**Task:** Sales & Revenue Analysis Dashboard

**Objective:** Build a dashboard to analyze sales and revenue data.

### Expected Features

- Import data from Excel, CSV, or database
- Visualize KPIs such as total sales/revenue
- Analyze revenue trends
- Identify top-performing products
- Use charts and interactive filters
- Generate business insights

## Dataset

The project uses the **Online Retail** dataset from the UCI Machine Learning Repository.

The dataset contains transaction-level records for a UK-based online retailer.

The dashboard uses the following fields:

- `InvoiceNo` — Invoice number
- `StockCode` — Product code
- `Description` — Product description
- `Quantity` — Quantity purchased
- `InvoiceDate` — Transaction date and time
- `UnitPrice` — Price per unit
- `CustomerID` — Customer identifier
- `Country` — Customer country

Dataset source:

https://archive.ics.uci.edu/dataset/352/online+retail

## Data Preparation

The dashboard applies the following cleaning and preparation steps:

1. Standardizes column names.
2. Converts `InvoiceDate` to datetime.
3. Converts `Quantity` and `UnitPrice` to numeric values.
4. Fills missing product descriptions with `Unknown Product`.
5. Fills missing countries with `Unknown`.
6. Identifies cancelled invoices using invoice numbers beginning with `C`.
7. Excludes cancelled transactions from the main sales analysis.
8. Excludes rows with missing dates.
9. Excludes transactions with non-positive quantities.
10. Excludes transactions with non-positive unit prices.
11. Calculates revenue using:

`Revenue = Quantity * UnitPrice`

12. Creates a monthly analysis field named `YearMonth`.

## Dashboard KPIs

The dashboard provides five primary KPIs.

### Total Revenue

Total calculated sales revenue after applying the selected filters.

### Total Orders

Number of unique invoice numbers in the filtered dataset.

### Total Quantity

Total number of units sold.

### Average Order Value

Calculated as:

`Average Order Value = Total Revenue / Total Orders`

### Unique Customers

Number of unique non-missing customer IDs.

## Key Business Insights

The dashboard automatically identifies:

- Highest revenue month
- Top revenue-generating product
- Top revenue-generating country
- Revenue per customer

These insights update when dashboard filters are changed.

## Dashboard Features

### 1. Data Upload

Users can upload:

- CSV
- XLSX
- XLS

The application validates the required columns before processing the uploaded file.

### 2. Date Filter

Users can select a date range to analyze a specific period.

### 3. Country Filter

Users can select one or multiple countries.

### 4. Product Search

Users can search products using partial text.

### 5. Revenue & Order Trend

The dashboard displays:

- Monthly revenue trend
- Monthly order trend

### 6. Product Performance

Two charts show:

- Top 10 products by revenue
- Top 10 products by quantity sold

### 7. Geographic Revenue Analysis

The dashboard provides:

- Revenue by country
- Revenue share for the top countries

### 8. Transaction Data

Users can expand the transaction section and inspect filtered transaction-level records.

### 9. Data Export

Filtered transaction data can be downloaded as a CSV file.

## Technologies Used

- Python
- Pandas
- Plotly
- Streamlit
- OpenPyXL
- UCI Machine Learning Repository dataset

## Project Structure

```text
Sales_Revenue_Analysis_Dashboard/
│
├── app.py
├── README.md
├── requirements.txt
├── LICENSE
│
├── data/
│   ├── raw/
│   └── processed/
│
├── src/
│   ├── download_data.py
│   └── prepare_data.py
│
├── sql/
│   └── analysis_queries.sql
│
├── notebooks/
│   └── Sales_Revenue_Analysis.ipynb
│
├── docs/
│   ├── Dashboard_Guide.md
│   └── Project_Documentation.md
│
└── screenshots/

```

## Installation

### 1. Clone the repository

`git clone YOUR_GITHUB_REPOSITORY_URL`

`cd Sales_Revenue_Analysis_Dashboard`

### 2. Install dependencies

`pip install -r requirements.txt`

### 3. Prepare the dataset

If the processed dataset is already included, the dashboard can use it directly.

Alternatively, place the UCI Online Retail Excel file in:

`data/raw/Online Retail.xlsx`

Then run:

`python src/prepare_data.py`

### 4. Run the dashboard

`python -m streamlit run app.py`

The application will open in the browser at the local Streamlit address shown in the terminal.

## Dashboard Workflow

Raw Online Retail Data  
↓  
Data Cleaning  
↓  
Validation  
↓  
Revenue Calculation  
↓  
Monthly / Product / Country Aggregation  
↓  
Interactive Filters  
↓  
KPIs + Charts + Business Insights  
↓  
Filtered Data Export

## Example Business Questions

The dashboard can be used to answer questions such as:

1. How much revenue was generated during the selected period?
2. How many orders were placed?
3. How many units were sold?
4. What was the average order value?
5. Which month generated the highest revenue?
6. Which products generated the most revenue?
7. Which products had the highest sales quantity?
8. Which countries generated the most revenue?
9. How does revenue change when filtering by country?
10. How does product performance change over a selected period?

## Limitations

- Revenue is calculated from `Quantity * UnitPrice`.
- Cancelled invoices are excluded from the main sales analysis.
- Rows with invalid dates, non-positive quantities, or non-positive unit prices are excluded.
- Customer-based metrics use available `CustomerID` values.
- The dashboard is an analytical implementation and does not represent accounting or audited financial statements.

## Author

**Md. Israk Ahmmed**

Data Analytics Intern

Thiranex

## License

This project is prepared for educational and internship project purposes.

The dataset remains subject to the licensing terms of the UCI Machine Learning Repository.
