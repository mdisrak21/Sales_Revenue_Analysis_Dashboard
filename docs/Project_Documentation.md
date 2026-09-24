# Project Documentation

## Project Title

Sales & Revenue Analysis Dashboard

## Business Objective

The objective is to transform retail transaction data into an interactive analytical dashboard that supports sales monitoring and business insight generation.

## Analytical Approach

The project follows these stages:

### Stage 1 — Data Input

The application accepts CSV and Excel files and can also use a prepared local dataset.

### Stage 2 — Data Cleaning

The application validates required fields, converts data types, handles missing descriptive values, identifies cancellations, and removes invalid sales records.

### Stage 3 — Revenue Calculation

Revenue is calculated at transaction level:

`Revenue = Quantity × UnitPrice`

### Stage 4 — Aggregation

The cleaned data is aggregated by:

- Month
- Product
- Country
- Order

### Stage 5 — Visualization

Plotly charts are used to communicate trends and comparisons.

### Stage 6 — Interactive Analysis

Streamlit filters allow the user to dynamically change the analysis.

### Stage 7 — Business Insights

The dashboard identifies leading revenue periods, products, countries, and revenue per customer.

## KPI Definitions

| KPI | Definition |
|---|---|
| Total Revenue | Sum of transaction revenue |
| Total Orders | Unique invoice count |
| Total Quantity | Sum of positive quantities |
| Average Order Value | Revenue divided by unique orders |
| Unique Customers | Unique available CustomerID values |
| Revenue per Customer | Revenue divided by unique customers |

## Data Quality Rules

The main dashboard excludes:

- Cancelled invoices
- Missing transaction dates
- Non-positive quantities
- Non-positive unit prices

## Analytical Outputs

The dashboard produces:

- KPI cards
- Monthly revenue trend
- Monthly order trend
- Top products by revenue
- Top products by quantity
- Revenue by country
- Revenue share by country
- Country summary table
- Filtered transaction table
- CSV export

## Reproducibility

The project can be run locally using:

`python -m streamlit run app.py`

The same dashboard logic is applied whether the data is loaded from the prepared local dataset or uploaded as a supported CSV/Excel file.

## Project Outcome

The completed project demonstrates practical skills in:

- Data cleaning
- Data transformation
- KPI development
- Exploratory data analysis
- Data visualization
- Interactive dashboard development
- Business insight generation
- Data export