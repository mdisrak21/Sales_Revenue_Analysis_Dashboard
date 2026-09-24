
```markdown
<!-- docs/Dashboard_Guide.md -->

# Dashboard Guide

## 1. Dashboard Purpose

The Sales & Revenue Analysis Dashboard provides an interactive view of transaction-level retail sales data.

The main goal is to convert raw transaction records into understandable KPIs, trends, product analysis, geographic analysis, and business insights.

## 2. Using the Dashboard

### Data Upload

Use the left sidebar to upload a CSV or Excel file.

The uploaded file must contain:

- InvoiceNo
- StockCode
- Description
- Quantity
- InvoiceDate
- UnitPrice
- CustomerID
- Country

If no file is uploaded, the dashboard attempts to load:

`data/processed/online_retail_clean.csv`

## 3. Filters

### Date Range

Select the period to include in the analysis.

### Country

Select one or more countries.

### Product Contains

Enter text to find products whose descriptions contain the entered text.

All KPI values and charts update according to the active filters.

## 4. KPI Interpretation

### Total Revenue

The sum of calculated transaction revenue.

### Total Orders

Unique invoice count.

### Total Quantity

Total units sold.

### Average Order Value

Revenue divided by the number of unique orders.

### Unique Customers

Unique non-missing customer IDs.

## 5. Business Insights

The Key Business Insights section identifies:

- Highest revenue month
- Top revenue product
- Top revenue country
- Revenue per customer

Because these values are calculated from the filtered data, they change when filters change.

## 6. Charts

### Revenue & Order Trend

The first chart shows how revenue changes by month.

The second chart shows monthly order volume.

### Product Performance

The product section compares the top products using:

- Revenue
- Quantity sold

### Geographic Revenue Analysis

The geographic section compares revenue by country and shows the revenue share of the leading countries.

## 7. Transaction Data

The transaction section is expandable.

It provides a detailed view of up to 1,000 filtered transactions, including:

- Invoice number
- Product code
- Product description
- Quantity
- Invoice date
- Unit price
- Revenue
- Customer ID
- Country

## 8. Export

The `Download Filtered Data` button exports the currently filtered transaction dataset as a CSV file.

## 9. Presentation Tips

For a project demonstration:

1. Start with the KPI cards.
2. Explain the date, country, and product filters.
3. Show the revenue trend.
4. Explain product performance.
5. Explain geographic performance.
6. Demonstrate the business insights.
7. Open the transaction section.
8. Export the filtered data.

## 10. Suggested Demo Scenario

Select a shorter date range and one country, then demonstrate how:

- Revenue changes
- Orders change
- Quantity changes
- Top products change
- Geographic results change
- Business insights update

This demonstrates the interactive nature of the dashboard.