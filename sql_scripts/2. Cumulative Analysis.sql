-- =============================================================================
-- 2. Cumulative Analysis
-- =============================================================================
-- Aggregate data progressively over time; total cumulative measure by date dimension.

-- Step 1: Monthly sales aggregation (base for running total)
/*
SELECT
	DATETRUNC(MONTH, order_date) AS order_date,
	SUM(sales_amount) AS total_sales
FROM gold.fact_sales
WHERE order_date IS NOT NULL
GROUP BY DATETRUNC(MONTH, order_date)
ORDER BY DATETRUNC(MONTH, order_date);
*/

-- Step 2: Running total via window function over monthly data
/*
SELECT
	order_date,
	total_sales,
	SUM(total_sales) OVER (ORDER BY order_date) AS running_total_sales
FROM (
	SELECT
		DATETRUNC(MONTH, order_date) AS order_date,
		SUM(sales_amount) AS total_sales
	FROM gold.fact_sales
	WHERE order_date IS NOT NULL
	GROUP BY DATETRUNC(MONTH, order_date)
) t;
*/

-- Partition by order_date: no effect here since each row has unique order_date
/*
SELECT
	order_date,
	total_sales,
	SUM(total_sales) OVER (PARTITION BY YEAR(order_date) ORDER BY order_date) AS running_total_sales
FROM (
	SELECT
		DATETRUNC(MONTH, order_date) AS order_date,
		SUM(sales_amount) AS total_sales
	FROM gold.fact_sales
	WHERE order_date IS NOT NULL
	GROUP BY DATETRUNC(MONTH, order_date)
) t;
*/

-- Yearly granularity: running total and moving average
/*
SELECT
	order_date,
	total_sales,
	SUM(total_sales) OVER (ORDER BY order_date) AS running_total_sales
FROM (
	SELECT
		DATETRUNC(YEAR, order_date) AS order_date,
		SUM(sales_amount) AS total_sales
	FROM gold.fact_sales
	WHERE order_date IS NOT NULL
	GROUP BY DATETRUNC(YEAR, order_date)
) t;
*/

-- Active query: yearly running total + moving average price
SELECT
	order_date,
	total_sales,
	SUM(total_sales) OVER (ORDER BY order_date) AS running_total_sales,
	AVG(avg_price) OVER (ORDER BY order_date) AS moving_avg_price
FROM (
	SELECT
		DATETRUNC(YEAR, order_date) AS order_date,
		SUM(sales_amount) AS total_sales,
		AVG(price) AS avg_price
	FROM gold.fact_sales
	WHERE order_date IS NOT NULL
	GROUP BY DATETRUNC(YEAR, order_date)
) t
ORDER BY order_date;