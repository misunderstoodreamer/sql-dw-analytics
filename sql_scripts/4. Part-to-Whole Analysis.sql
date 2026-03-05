-- =============================================================================
-- 4. Part-to-Whole Analysis
-- =============================================================================
-- (measure / total amount) * 100 by dimension
-- Examples: (sales / total sales) * 100 by category; (quantity / total quantity) * 100 by country

-- Which category contributes most to overall sales
/*
SELECT
	category,
	SUM(sales_amount) AS total_sales
FROM gold.fact_sales f
LEFT JOIN gold.dim_products p ON p.product_key = f.product_key
GROUP BY category;
*/
/*
WITH category_sales AS (
	SELECT
		category,
		SUM(sales_amount) AS total_sales
	FROM gold.fact_sales f
	LEFT JOIN gold.dim_products p ON p.product_key = f.product_key
	GROUP BY category
)
SELECT
	category,
	total_sales,
	SUM(total_sales) OVER () AS overall_sales,
	CONCAT(ROUND((CAST(total_sales AS FLOAT) / SUM(total_sales) OVER ()) * 100, 2), '%') AS percentage_of_total
FROM category_sales
ORDER BY total_sales DESC;
*/

-- Active query: category share of total sales with percentage
WITH category_sales AS (
    SELECT
        p.category,
        SUM(f.sales_amount) AS total_sales
    FROM gold.fact_sales f
    LEFT JOIN gold.dim_products p
        ON p.product_key = f.product_key
    GROUP BY p.category
)
SELECT
    category,
    total_sales,
    SUM(total_sales) OVER () AS overall_sales,
    ROUND((CAST(total_sales AS FLOAT) / SUM(total_sales) OVER ()) * 100, 2) AS percentage_of_total
FROM category_sales
ORDER BY total_sales DESC;