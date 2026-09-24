-- Sales & Revenue Analysis queries
-- Table expected: online_retail
-- Columns: InvoiceNo, StockCode, Description, Quantity, InvoiceDate,
--          UnitPrice, CustomerID, Country

-- 1. Total revenue from valid non-cancelled sales
SELECT ROUND(SUM(Quantity * UnitPrice), 2) AS total_revenue
FROM online_retail
WHERE UPPER(InvoiceNo) NOT LIKE 'C%'
  AND Quantity > 0
  AND UnitPrice > 0;

-- 2. Total orders
SELECT COUNT(DISTINCT InvoiceNo) AS total_orders
FROM online_retail
WHERE UPPER(InvoiceNo) NOT LIKE 'C%'
  AND Quantity > 0
  AND UnitPrice > 0;

-- 3. Monthly revenue
SELECT
    strftime('%Y-%m', InvoiceDate) AS year_month,
    ROUND(SUM(Quantity * UnitPrice), 2) AS revenue
FROM online_retail
WHERE UPPER(InvoiceNo) NOT LIKE 'C%'
  AND Quantity > 0
  AND UnitPrice > 0
GROUP BY strftime('%Y-%m', InvoiceDate)
ORDER BY year_month;

-- 4. Top 10 products by revenue
SELECT
    Description,
    ROUND(SUM(Quantity * UnitPrice), 2) AS revenue
FROM online_retail
WHERE UPPER(InvoiceNo) NOT LIKE 'C%'
  AND Quantity > 0
  AND UnitPrice > 0
GROUP BY Description
ORDER BY revenue DESC
LIMIT 10;

-- 5. Country revenue
SELECT
    Country,
    ROUND(SUM(Quantity * UnitPrice), 2) AS revenue
FROM online_retail
WHERE UPPER(InvoiceNo) NOT LIKE 'C%'
  AND Quantity > 0
  AND UnitPrice > 0
GROUP BY Country
ORDER BY revenue DESC;

-- 6. Average order value
WITH orders AS (
    SELECT InvoiceNo, SUM(Quantity * UnitPrice) AS order_revenue
    FROM online_retail
    WHERE UPPER(InvoiceNo) NOT LIKE 'C%'
      AND Quantity > 0
      AND UnitPrice > 0
    GROUP BY InvoiceNo
)
SELECT ROUND(AVG(order_revenue), 2) AS average_order_value
FROM orders;
