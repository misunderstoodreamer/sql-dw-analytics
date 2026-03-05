/*
=============================================================
Create Database and Schemas
=============================================================
Script Purpose:
    This script creates a new database named 'DataWarehouseAnalytics' after checking if it already exists.
    If the database exists, it is dropped and recreated. Additionally, this script creates a schema called gold.

WARNING:
    Running this script will drop the entire 'DataWarehouseAnalytics' database if it exists.
    All data in the database will be permanently deleted. Proceed with caution
    and ensure you have proper backups before running this script.
*/

USE master;
GO

-- Drop existing database to allow clean recreation; single-user mode ensures no active connections block the drop
IF EXISTS (SELECT 1 FROM sys.databases WHERE name = 'DataWarehouseAnalytics')
BEGIN
    ALTER DATABASE DataWarehouseAnalytics SET SINGLE_USER WITH ROLLBACK IMMEDIATE;
    DROP DATABASE DataWarehouseAnalytics;
END;
GO

-- Create the DataWarehouseAnalytics database for gold-layer analytics
CREATE DATABASE DataWarehouseAnalytics;
GO

USE DataWarehouseAnalytics;
GO

-- Gold schema holds the final dimensional model tables for reporting
CREATE SCHEMA gold;
GO

-- Customer dimension: demographics, identifiers, and SCD attributes
CREATE TABLE gold.dim_customers(
	customer_key int,
	customer_id int,
	customer_number nvarchar(50),
	first_name nvarchar(50),
	last_name nvarchar(50),
	country nvarchar(50),
	marital_status nvarchar(50),
	gender nvarchar(50),
	birthdate date,
	create_date date
);
GO

-- Product dimension: hierarchy (category/subcategory), cost, and product line
CREATE TABLE gold.dim_products(
	product_key int ,
	product_id int ,
	product_number nvarchar(50) ,
	product_name nvarchar(50) ,
	category_id nvarchar(50) ,
	category nvarchar(50) ,
	subcategory nvarchar(50) ,
	maintenance nvarchar(50) ,
	cost int,
	product_line nvarchar(50),
	start_date date 
);
GO

-- Sales fact: order-level transactions with FK references to dim_customers and dim_products
CREATE TABLE gold.fact_sales(
	order_number nvarchar(50),
	product_key int,
	customer_key int,
	order_date date,
	shipping_date date,
	due_date date,
	sales_amount int,
	quantity tinyint,
	price int 
);
GO

-- Load dimension and fact data from CSV; replace {path_to_csv_files} with actual path before execution
TRUNCATE TABLE gold.dim_customers;
GO

-- Load customer dimension from CSV; FIRSTROW=2 skips header
BULK INSERT gold.dim_customers
FROM '{path_to_csv_files}\gold.dim_customers.csv'
WITH (
	FIRSTROW = 2,
	FIELDTERMINATOR = ',',
	TABLOCK
);
GO

TRUNCATE TABLE gold.dim_products;
GO

-- Load product dimension from CSV; FIRSTROW=2 skips header
BULK INSERT gold.dim_products
FROM '{path_to_csv_files}\gold.dim_products.csv'
WITH (
	FIRSTROW = 2,
	FIELDTERMINATOR = ',',
	TABLOCK
);
GO

TRUNCATE TABLE gold.fact_sales;
GO

-- Load sales fact from CSV; TABLOCK improves bulk insert performance
BULK INSERT gold.fact_sales
FROM '{path_to_csv_files}\gold.fact_sales.csv'
WITH (
	FIRSTROW = 2,
	FIELDTERMINATOR = ',',
	TABLOCK
);
GO
