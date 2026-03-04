-- =============================================================================
-- 5. Data Segmentation
-- =============================================================================
-- Group data by specific ranges to understand correlation between measures.
-- Examples: total products by cost range; total customers by age or spending.

-- Segment products into cost ranges and count how many fall into each
/*
SELECT
	product_key,
	product_name,
	cost,
	CASE WHEN cost < 100 THEN 'Below 100'
		 WHEN cost BETWEEN 100 AND 500 THEN '100-500'
		 WHEN cost BETWEEN 500 AND 1000 THEN '500-1000'
		 ELSE 'Above 1000'
	END AS cost_range
FROM gold.dim_products;
*/
/*
WITH product_segment AS (
	SELECT
		product_key,
		product_name,
		cost,
		CASE WHEN cost < 100 THEN 'Below 100'
			 WHEN cost BETWEEN 100 AND 500 THEN '100-500'
			 WHEN cost BETWEEN 500 AND 1000 THEN '500-1000'
			 ELSE 'Above 1000'
		END AS cost_range
	FROM gold.dim_products
)
SELECT
	cost_range,
	COUNT(product_key) AS total_products
FROM product_segment
GROUP BY cost_range
ORDER BY total_products DESC;
*/

-- Customer segments by spending behaviour:
-- VIP: at least 12 months history, spending > 5000
-- REG: at least 12 months history, spending <= 5000
-- NEW: history < 12 months
/*
SELECT
	c.customer_key,
	SUM(f.sales_amount) AS total_spending,
	MIN(order_date) AS first_order,
	MAX(order_date) AS last_order,
	DATEDIFF(MONTH, MIN(order_date), MAX(order_date)) AS life_span
FROM gold.fact_sales f
LEFT JOIN gold.dim_customers c ON c.customer_key = f.customer_key
GROUP BY c.customer_key;
*/
/*
WITH customer_spending AS (
	SELECT
		c.customer_key,
		SUM(f.sales_amount) AS total_spending,
		MIN(order_date) AS first_order,
		MAX(order_date) AS last_order,
		DATEDIFF(MONTH, MIN(order_date), MAX(order_date)) AS life_span
	FROM gold.fact_sales f
	LEFT JOIN gold.dim_customers c ON c.customer_key = f.customer_key
	GROUP BY c.customer_key
)
SELECT
	customer_key,
	total_spending,
	life_span,
	CASE WHEN life_span >= 12 AND total_spending > 5000 THEN 'VIP'
		 WHEN life_span >= 12 AND total_spending <= 5000 THEN 'REGULAR'
		 ELSE 'NEW'
	END AS customer_segment
FROM customer_spending;
*/

-- Active query: customer count per segment
WITH customer_spending AS (
	SELECT
		c.customer_key,
		SUM(f.sales_amount) AS total_spending,
		MIN(order_date) AS first_order,
		MAX(order_date) AS last_order,
		DATEDIFF(MONTH, MIN(order_date), MAX(order_date)) AS life_span
	FROM gold.fact_sales f
	LEFT JOIN gold.dim_customers c ON c.customer_key = f.customer_key
	GROUP BY c.customer_key
)
SELECT
	customer_segment,
	COUNT(customer_key) AS total_customers
FROM (
	SELECT
		customer_key,
		CASE WHEN life_span >= 12 AND total_spending > 5000 THEN 'VIP'
			 WHEN life_span >= 12 AND total_spending <= 5000 THEN 'REGULAR'
			 ELSE 'NEW'
		END AS customer_segment
	FROM customer_spending
) t
GROUP BY customer_segment
ORDER BY total_customers DESC;