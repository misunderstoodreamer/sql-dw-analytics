-- =============================================================================
-- 6. Customer Report
-- =============================================================================
-- Key customer metrics and behaviours.
-- 1. Essential fields: customer info, age
-- 2. Aggregates: total orders, sales, quantity, products, lifespan
-- 3. KPIs: recency, average order value (AOV), average monthly spend

-- Base query: order-level with customer and age
/*
WITH base_query AS (
	SELECT
		f.order_number,
		f.product_key,
		f.order_date,
		f.sales_amount,
		f.quantity,
		c.customer_key,
		c.customer_number,
		CONCAT(c.first_name, ' ', c.last_name) AS fullname,
		DATEDIFF(YEAR, c.birthdate, GETDATE()) AS age
	FROM gold.fact_sales f
	LEFT JOIN gold.dim_customers c ON c.customer_key = f.customer_key
	WHERE order_date IS NOT NULL
)
SELECT
	customer_key,
	customer_number,
	fullname,
	age,
	COUNT(DISTINCT order_number) AS total_orders,
	SUM(quantity) AS total_sales,
	COUNT(DISTINCT product_key) AS total_products,
	MAX(order_date) AS last_order_date,
	DATEDIFF(MONTH, MIN(order_date), MAX(order_date)) AS life_span
FROM base_query
GROUP BY customer_key, customer_number, fullname, age;
*/
/*
WITH base_query AS (
	SELECT
		f.order_number,
		f.product_key,
		f.order_date,
		f.sales_amount,
		f.quantity,
		c.customer_key,
		c.customer_number,
		CONCAT(c.first_name, ' ', c.last_name) AS fullname,
		DATEDIFF(YEAR, c.birthdate, GETDATE()) AS age
	FROM gold.fact_sales f
	LEFT JOIN gold.dim_customers c ON c.customer_key = f.customer_key
	WHERE order_date IS NOT NULL
), customer_aggregation AS (
	SELECT
		customer_key,
		customer_number,
		fullname,
		age,
		COUNT(DISTINCT order_number) AS total_orders,
		SUM(quantity) AS total_sales,
		COUNT(DISTINCT product_key) AS total_products,
		MAX(order_date) AS last_order_date,
		DATEDIFF(MONTH, MIN(order_date), MAX(order_date)) AS life_span
	FROM base_query
	GROUP BY customer_key, customer_number, fullname, age
)
SELECT
	customer_key,
	customer_number,
	fullname,
	age,
	CASE WHEN age < 20 THEN 'Under 20'
		 WHEN age BETWEEN 20 AND 29 THEN 'Under 20-29'
		 WHEN age BETWEEN 30 AND 39 THEN 'Under 30-39'
		 WHEN age BETWEEN 40 AND 49 THEN 'Under 40-49'
		 ELSE '50 and Above'
	END AS age_group,
	CASE WHEN life_span >= 12 AND total_sales > 5000 THEN 'VIP'
		 WHEN life_span >= 12 AND total_sales <= 5000 THEN 'REGULAR'
		 ELSE 'NEW'
	END AS customer_segment,
	total_orders,
	total_sales,
	total_products,
	last_order_date,
	life_span
FROM customer_aggregation;
*/

-- View: customer report with age groups, segment (from script 5), recency, AOV, avg monthly spend
CREATE VIEW gold.customer_reports AS
WITH base_query AS (
	SELECT
		f.order_number,
		f.product_key,
		f.order_date,
		f.sales_amount,
		f.quantity,
		c.customer_key,
		c.customer_number,
		CONCAT(c.first_name, ' ', c.last_name) AS customer_name,
		DATEDIFF(YEAR, c.birthdate, GETDATE()) AS age
	FROM gold.fact_sales f
	LEFT JOIN gold.dim_customers c ON c.customer_key = f.customer_key
	WHERE order_date IS NOT NULL
), customer_aggregation AS (
	SELECT
		customer_key,
		customer_number,
		customer_name,
		age,
		COUNT(DISTINCT order_number) AS total_orders,
		SUM(sales_amount) AS total_sales,
		SUM(quantity) AS total_quantity,
		COUNT(DISTINCT product_key) AS total_products,
		MAX(order_date) AS last_order_date,
		DATEDIFF(MONTH, MIN(order_date), MAX(order_date)) AS life_span
	FROM base_query
	GROUP BY customer_key, customer_number, customer_name, age
)
SELECT
	customer_key,
	customer_number,
	customer_name,
	age,
	CASE WHEN age < 20 THEN 'Under 20'
		 WHEN age BETWEEN 20 AND 29 THEN 'Under 20-29'
		 WHEN age BETWEEN 30 AND 39 THEN 'Under 30-39'
		 WHEN age BETWEEN 40 AND 49 THEN 'Under 40-49'
		 ELSE '50 and Above'
	END AS age_group,
	CASE WHEN life_span >= 12 AND total_sales > 5000 THEN 'VIP'
		 WHEN life_span >= 12 AND total_sales <= 5000 THEN 'REGULAR'
		 ELSE 'NEW'
	END AS customer_segment,
	last_order_date,
	DATEDIFF(MONTH, last_order_date, GETDATE()) AS recency,
	total_orders,
	total_sales,
	total_quantity,
	total_products,
	life_span,
	CASE WHEN total_sales = 0 THEN 0
		 ELSE total_sales / total_orders
	END AS avg_order_value,
	CASE WHEN life_span = 0 THEN total_sales
		 ELSE total_sales / life_span
	END AS avg_monthly_spend
FROM customer_aggregation;
