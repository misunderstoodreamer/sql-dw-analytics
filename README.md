# sql-dw-analytics

> Advanced T-SQL analytics and reporting views for extracting business insights from a dimensional Gold-layer data warehouse.

## Project Overview

This repository contains an end-to-end data analytics workflow built on a dimensional data model (Star Schema). The project focuses on extracting actionable business insights from a "Gold" layer data warehouse using advanced T-SQL queries. 

The development is structured into two main phases:
* **Phase 1 (Current):** Database initialization, dimensional data modeling, and advanced SQL analytics (Window Functions, CTEs, Data Segmentation, Time-Series Analysis).
* **Phase 2 (Planned):** Data visualization and dashboarding using Python, leveraging the SQL views generated in Phase 1.

## Data Architecture

The `DataWarehouseAnalytics` database utilizes a simplified Medallion architecture, specifically targeting the `gold` schema for downstream reporting and BI tools. 

The Star Schema consists of the following tables:
* `gold.dim_customers`: Customer dimension containing demographic and historical data.
* `gold.dim_products`: Product dimension containing categorization, pricing, and cost metrics.
* `gold.fact_sales`: Transactional fact table recording order details, quantities, and revenue.

## Repository Structure

The analytical scripts are modularized by business logic. Execute them sequentially:

| Script | Description |
|--------|-------------|
| `0. Create Database and Schemas.sql` | Database init. Drops/recreates `DataWarehouseAnalytics`, creates `gold` schema, dimension and fact tables, bulk-loads CSV data. |
| `1. Change Over Time Analysis.sql` | Monthly time-series aggregations on `fact_sales` for trend and seasonality. |
| `2. Cumulative Analysis.sql` | Running totals and moving averages via window functions. |
| `3. Performance Analysis.sql` | Yearly product performance vs product avg and prior year (LAG). |
| `4. Part-to-Whole Analysis.sql` | Category share of total sales with percentage. |
| `5. Data Segmentation.sql` | Product cost ranges; customer segments (VIP/REG/NEW) by spending and tenure. |
| `6. Customer Report.sql` | Creates `gold.report_customers` view: age groups, segment, recency, AOV, avg monthly spend. |
| `7. Product Report.sql` | Product-level metrics: category, segment (High/Mid/Low by revenue), recency, lifespan, AOR, avg monthly revenue. |
