-- =============================================================================
-- 1. Change over time analysis
-- =============================================================================
-- Data set is analyzed first by looking at the change-over-time analysis; this is valid for aggregate values.
-- That's why we first analyze the fact tables.
/*
SELECT 
	YEAR(order_date) as order_year
	,SUM(sales_amount) as total_sales
	,COUNT(DISTINCT customer_key) as total_customer
	,SUM(quantity) as total_quantity
from gold.fact_sales 
where order_date is not null
group by YEAR(order_date)
order by YEAR(order_date);
*/
-- Yearly rollup: high-level long-term view for strategic decisions

-- Seasonality: monthly aggregation to identify business cycles
/*
SELECT 
	MONTH(order_date) as order_month
	,SUM(sales_amount) as total_sales
	,COUNT(DISTINCT customer_key) as total_customer
	,SUM(quantity) as total_quantity
from gold.fact_sales 
where order_date is not null
group by MONTH(order_date)
order by MONTH(order_date);
*/
/*
SELECT
	YEAR(order_date) as order_year
	,MONTH(order_date) as order_month
	,SUM(sales_amount) as total_sales
	,COUNT(DISTINCT customer_key) as total_customer
	,SUM(quantity) as total_quantity
from gold.fact_sales 
where order_date is not null
group by YEAR(order_date), MONTH(order_date) 
ORDER BY YEAR(order_date), MONTH(order_date);
*/
-- Active query: monthly time series with DATETRUNC for cleaner date bucketing
SELECT
	DATETRUNC(MONTH, order_date) as order_date
	,SUM(sales_amount) as total_sales
	,COUNT(DISTINCT customer_key) as total_customer
	,SUM(quantity) as total_quantity
FROM gold.fact_sales
WHERE order_date IS NOT NULL
GROUP BY DATETRUNC(MONTH, order_date)
ORDER BY DATETRUNC(MONTH, order_date);
