-- ADVANCED SQL PROJECT
-- Change over time, Cumulative Analysis, Performance Analysis, Part to Whole Analysis, Data Segmentation, Data Reporting, Customer Report, Product Report


SELECT YEAR(order_date) as Order_Year, SUM(sales_amount) as Sum_Sales, 
COUNT(DISTINCT customer_key) as CustCount, SUM(quantity) as Sum_Quant
FROM sales
WHERE order_date IS NOT NULL
GROUP BY YEAR(order_date)
ORDER BY YEAR(order_date)

-- 2013 was the best year for the business as sales and customer count peaked in this year. 
-- However 2014 observed the largest pitfalls in sales.

SELECT FORMAT(order_date, 'MMM-yyyy') as Order_date, SUM(sales_amount) as Sum_Sales, 
COUNT(DISTINCT customer_key) as CustCount, SUM(quantity) as Sum_Quant
FROM sales
WHERE order_date IS NOT NULL
GROUP BY FORMAT(order_date, 'MMM-yyyy')
ORDER BY SUM(sales_amount) DESC, FORMAT(order_date, 'MMM-yyyy')

-- Sales peaked in the month of December of 2013, 2012 and 2010 and June of 2011 each year for the company. 


--CUMULATIVE VALUES OVER TIME
SELECT
Order_Date,
Sum_Sales,
SUM(Sum_Sales) OVER (ORDER BY Order_Date) as Running_Sales
FROM
(SELECT
DATETRUNC(year, order_date) as Order_Date, SUM(sales_amount) as Sum_Sales
FROM sales
WHERE order_date IS NOT NULL
GROUP BY DATETRUNC(year, order_date))t


SELECT
Order_Date,
Sum_Sales,
SUM(Sum_Sales) OVER (ORDER BY Order_Date) as Running_Sales,
AVG(avg_price) OVER (ORDER BY Order_Date) as Running_Avg_Price
FROM
(SELECT
DATETRUNC(year, order_date) as Order_Date, SUM(sales_amount) as Sum_Sales,
AVG(price) as avg_price
FROM sales
WHERE order_date IS NOT NULL
GROUP BY DATETRUNC(year, order_date))t

-- PERFORMANCE ANALYSIS
---- Comparison of Current Sales with Avg. sales
WITH yearly_product_sales AS(
SELECT 
YEAR(s.order_date) as order_year,
p.product_name,
SUM(s.sales_amount) as current_sales
FROM sales s
LEFT JOIN products p
	ON s.product_key = p.product_key
WHERE s.order_date IS NOT NULL
GROUP BY YEAR(s.order_date), p.product_name
)
SELECT
order_year, product_name, current_sales,
AVG(current_sales) OVER (PARTITION BY product_name) avg_sales,
current_sales - AVG(current_sales) OVER (PARTITION BY product_name) as diff_avg,
CASE
	WHEN current_sales - AVG(current_sales) OVER (PARTITION BY product_name) < 0 THEN 'Below Average'
	WHEN current_sales - AVG(current_sales) OVER (PARTITION BY product_name) > 0 THEN 'Above Average'
	ELSE 'Avg'
END avg_change
FROM yearly_product_sales

---- Current Sales with previous year
WITH yearly_product_sales AS(
SELECT 
YEAR(s.order_date) as order_year,
p.product_name,
SUM(s.sales_amount) as current_sales
FROM sales s
LEFT JOIN products p
	ON s.product_key = p.product_key
WHERE s.order_date IS NOT NULL
GROUP BY YEAR(s.order_date), p.product_name
)
SELECT
order_year, product_name, current_sales,
AVG(current_sales) OVER (PARTITION BY product_name) avg_sales,
current_sales - AVG(current_sales) OVER (PARTITION BY product_name) as diff_avg,
CASE
	WHEN current_sales - AVG(current_sales) OVER (PARTITION BY product_name) < 0 THEN 'Below Average'
	WHEN current_sales - AVG(current_sales) OVER (PARTITION BY product_name) > 0 THEN 'Above Average'
	ELSE 'Avg'
END avg_change,
LAG(current_sales) OVER (PARTITION BY product_name ORDER BY order_year) py_sales,
current_sales - LAG(current_sales) OVER (PARTITION BY product_name ORDER BY order_year) diff_py,
CASE
	WHEN current_sales - LAG(current_sales) OVER (PARTITION BY product_name ORDER BY order_year) < 0 THEN 'Declining'
	WHEN current_sales - LAG(current_sales) OVER (PARTITION BY product_name ORDER BY order_year) > 0 THEN 'Rising'
	ELSE 'No Change'
END avg_change
FROM yearly_product_sales
ORDER BY product_name, order_year


-- PART TO WHOLE ANALYSIS
----Categories contributing to overall sales
SELECT p.category, SUM(s.sales_amount) total_sales
FROM sales s
LEFT JOIN products p
	ON p.product_key = s.product_key
GROUP BY category

WITH CTE AS 
(SELECT p.category, SUM(s.sales_amount) total_sales
FROM sales s
LEFT JOIN products p
	ON p.product_key = s.product_key
GROUP BY category)
SELECT category, total_sales, SUM(total_sales) OVER () All_sales,
CONCAT(ROUND((CAST(total_sales AS FLOAT)/SUM(total_sales) OVER ())*100,3),'%') AS Share_of_each_Category
FROM CTE
ORDER BY Share_of_each_Category DESC

---- Bikes occupied the highest share of the company's business. 
---- Additionally, the data describes that other categories had very minute shares as compared to bikes.



--SEGMENTATION OF PRODUCTS BY COSTS AND CREATE COST RANGES
WITH product_segments AS
(SELECT 
product_key, product_name, cost,
CASE
	WHEN cost < 100 THEN 'Below 100'
	WHEN cost BETWEEN 101 AND 500 THEN '101-500'
	WHEN cost BETWEEN 501 AND 1000 THEN '501-1000'
	WHEN cost > 1000 THEN 'Above 1000'
END Cost_Range
FROM products)
SELECT COUNT(product_name), Cost_Range FROM product_segments
GROUP BY Cost_Range

---Grouping customers based on their spending behaviour
------METHOD 1
WITH CTE AS 
(SELECT
c.customer_key, SUM(s.sales_amount) AS Sum_Sales,
MIN(order_date) AS first_order,
MAX(order_date) AS last_order,
DATEDIFF(month, MIN(order_date), MAX(order_date)) AS lifespan
FROM sales s
LEFT JOIN customers c
	ON s.customer_key = c.customer_key
GROUP BY c.customer_key
)
SELECT 
CASE
	WHEN Sum_Sales > 5000 AND lifespan >= 12 THEN 'VIP'
	WHEN Sum_Sales <= 5000 AND lifespan >= 12 THEN 'Regular'
	WHEN lifespan < 12 THEN 'New'
END AS Customer_Type,
COUNT(customer_key) AS Total_Customers
FROM CTE
GROUP BY CASE
	WHEN Sum_Sales > 5000 AND lifespan >= 12 THEN 'VIP'
	WHEN Sum_Sales <= 5000 AND lifespan >= 12 THEN 'Regular'
	WHEN lifespan < 12 THEN 'New'
END 

------- METHOD 2
WITH CTE AS 
(SELECT
c.customer_key, SUM(s.sales_amount) AS Sum_Sales,
MIN(order_date) AS first_order,
MAX(order_date) AS last_order,
DATEDIFF(month, MIN(order_date), MAX(order_date)) AS lifespan
FROM sales s
LEFT JOIN customers c
	ON s.customer_key = c.customer_key
GROUP BY c.customer_key
)
SELECT Customer_Type, COUNT(customer_key) AS Total_Customers
FROM (
SELECT customer_key, 
CASE
	WHEN Sum_Sales > 5000 AND lifespan >= 12 THEN 'VIP'
	WHEN Sum_Sales <= 5000 AND lifespan >= 12 THEN 'Regular'
	WHEN lifespan < 12 THEN 'New'
END AS Customer_Type
FROM CTE) t
GROUP BY Customer_Type




--===============================================================================================================
--===============================================================================================================
--Customer Report------------------------------------------------------------------------------------------------

--Highlights of the Report---------------------------------------------------------------------------------------
----Information on essential demographics like name, age, sex, marital status and others
----Key metrics like transaction details, segments of customers, and age groups
----Aggregate Metrics including
	------ Total Orders
	------ Total Sales
	------ Total Products
	------ Total Quantity Produced
----Necessary KPIs
	------ time (in months) since last order
	------ avg order value
	------ avg monthly spending

-- Retrieving Core Values from Tables (Base Table)

WITH Demographics AS (
SELECT 
s.order_number, s.product_key, s.order_date, s.sales_amount, s.quantity,
c.customer_key, c.customer_number, CONCAT(first_name, ' ', last_name) AS Full_Name, 
c.gender, DATEDIFF(year, c.birthdate, GETDATE()) AS age
FROM sales s
LEFT JOIN customers c
		ON s.customer_key = c.customer_key
WHERE order_date IS NOT NULL)
SELECT customer_key, customer_number, Full_Name, gender, age 
FROM Demographics

-- Aggregations (Total Orders, Total Sales, Total Products, Total Quantity Produced)
WITH Aggregations AS (
SELECT 
s.order_number, s.product_key, s.order_date, s.sales_amount, s.quantity,
c.customer_key, c.customer_number, CONCAT(first_name, ' ', last_name) AS Full_Name, 
c.gender, DATEDIFF(year, c.birthdate, GETDATE()) AS age
FROM sales s
LEFT JOIN customers c
		ON s.customer_key = c.customer_key
WHERE order_date IS NOT NULL)
SELECT 
	customer_key, customer_number, Full_Name, gender, age,
	COUNT(DISTINCT order_number) AS total_orders,
	SUM(sales_amount) AS total_sales,
	SUM(DISTINCT product_key) AS total_products,
	SUM(quantity) AS total_quantity,
	MAX(order_date) AS latest_order,
	DATEDIFF(month, MIN(order_date), MAX(order_date)) AS lifespan
FROM Aggregations
GROUP BY customer_key, customer_number, Full_Name, gender, age


---Segmenting Customers
WITH Aggregations AS (
SELECT 
s.order_number, s.product_key, s.order_date, s.sales_amount, s.quantity,
c.customer_key, c.customer_number, CONCAT(first_name, ' ', last_name) AS Full_Name, 
c.gender, DATEDIFF(year, c.birthdate, GETDATE()) AS age
FROM sales s
LEFT JOIN customers c
		ON s.customer_key = c.customer_key
WHERE order_date IS NOT NULL)
, customer_agg AS (
SELECT 
	customer_key, customer_number, Full_Name, gender, age,
	COUNT(DISTINCT order_number) AS total_orders,
	SUM(sales_amount) AS total_sales,
	SUM(DISTINCT product_key) AS total_products,
	SUM(quantity) AS total_quantity,
	MAX(order_date) AS latest_order,
	DATEDIFF(month, MIN(order_date), MAX(order_date)) AS lifespan
FROM Aggregations
GROUP BY customer_key, customer_number, Full_Name, gender, age
)
SELECT
	customer_key, customer_number, Full_Name, gender, age,
	CASE
		WHEN age <= 30 THEN 'Young'
		WHEN age BETWEEN 31 AND 55 THEN 'Middle-Aged'
		WHEN age > 55 THEN 'Old'
	END age_group,
	CASE
		WHEN total_sales > 5000 AND lifespan >= 12 THEN 'VIP'
		WHEN total_sales <= 5000 AND lifespan >= 12 THEN 'Regular'
		WHEN lifespan < 12 THEN 'New'
	END AS Customer_Type,
	total_orders,
	total_sales,
	total_products,
	total_quantity,
	latest_order,
	lifespan
FROM customer_agg

---Creating KPIs (Final Result)
CREATE VIEW customer_report AS
WITH Aggregations AS (
SELECT 
s.order_number, s.product_key, s.order_date, s.sales_amount, s.quantity,
c.customer_key, c.customer_number, CONCAT(first_name, ' ', last_name) AS Full_Name, 
c.gender, DATEDIFF(year, c.birthdate, GETDATE()) AS age
FROM sales s
LEFT JOIN customers c
		ON s.customer_key = c.customer_key
WHERE order_date IS NOT NULL)
, customer_agg AS (
SELECT 
	customer_key, customer_number, Full_Name, gender, age,
	COUNT(DISTINCT order_number) AS total_orders,
	SUM(sales_amount) AS total_sales,
	SUM(DISTINCT product_key) AS total_products,
	SUM(quantity) AS total_quantity,
	MAX(order_date) AS latest_order,
	DATEDIFF(month, MIN(order_date), MAX(order_date)) AS lifespan
FROM Aggregations
GROUP BY customer_key, customer_number, Full_Name, gender, age
)
SELECT
	customer_key, customer_number, Full_Name, gender, age, latest_order,
	DATEDIFF(month, latest_order, GETDATE()) AS Recency,
	CASE
		WHEN age <= 30 THEN 'Young'
		WHEN age BETWEEN 31 AND 55 THEN 'Middle-Aged'
		WHEN age > 55 THEN 'Old'
	END age_group,
	CASE
		WHEN total_sales > 5000 AND lifespan >= 12 THEN 'VIP'
		WHEN total_sales <= 5000 AND lifespan >= 12 THEN 'Regular'
		WHEN lifespan < 12 THEN 'New'
	END AS Customer_Type,
	total_orders,
	total_sales,
	total_sales/total_orders AS avg_orders,
	total_products,
	total_quantity,
	CASE WHEN lifespan = 0 THEN 0
	ELSE total_sales/lifespan
	END as avg_monthly_spend,
	lifespan
FROM customer_agg

--===============================================================================================================
--===============================================================================================================
--Product Report------------------------------------------------------------------------------------------------

--Highlights of the Report---------------------------------------------------------------------------------------
----Information on essentials like product name, category, sub category, and cost
----Identify High performers, low performers and mid-range
----Aggregate Metrics including
	------ Total Orders
	------ Total Sales
	------ Total Customers (unique)
	------ Total Quantity Sold
	------ Lifespan
----Necessary KPIs
	------ time (in months) since last order
	------ avg order revenue (AOR)
	------ avg monthly revenue

CREATE VIEW product_report AS
WITH product_info AS (
SELECT 
s.order_number, s.product_key, s.order_date, s.sales_amount, s.quantity, s.customer_key,
p.product_name, p.category, p.subcategory, p.cost
FROM sales s
LEFT JOIN products p
		ON s.product_key = p.product_key
WHERE order_date IS NOT NULL)
, product_agg AS (
SELECT 
	product_key, product_name, category, subcategory, cost,
	COUNT(DISTINCT order_number) AS total_orders,
	SUM(sales_amount) AS total_sales,
	COUNT(DISTINCT customer_key) AS total_customers,
	SUM(quantity) AS total_quantity,
	MAX(order_date) AS latest_order,
	DATEDIFF(month, MIN(order_date), MAX(order_date)) AS lifespan,
	ROUND(AVG(CAST(sales_amount AS FLOAT)/NULLIF(quantity,0)),3) AS avg_selling_price
FROM product_info
GROUP BY product_key, product_name, category, subcategory, cost)
SELECT
	product_key, product_name, category, subcategory, cost, latest_order,
	DATEDIFF(month, latest_order, GETDATE()) AS Recency_in_months,
	CASE
		WHEN total_sales > 60000 THEN 'High Performer'
		WHEN total_sales > = 15000 THEN 'Mid Range'
		ELSE 'Poor Performer'
	END Performance,
	total_orders,
	total_sales,
	avg_selling_price,
	total_customers,
	total_quantity,
	CASE 
		WHEN total_orders = 0 THEN 0
		ELSE total_sales/total_orders
	END as avg_order_revenue,
	CASE
		WHEN lifespan = 0 THEN 0
		ELSE total_sales/lifespan
	END as avg_monthly_revenue,
	lifespan
FROM product_agg


