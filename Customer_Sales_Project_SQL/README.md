Customers Sales Analysis Project

📌 Overview

This project explores customer and product sales data using advanced SQL techniques. It includes deep-dive analyses into trends, performance, contribution metrics, customer and product segmentation, and key performance indicators (KPIs). It is designed for use in BI dashboards or reporting systems.

🧩 Key Analysis Areas

📈 1. Time Series Analysis

    Annual and Monthly Sales Trends
    Peak Sales Periods
    Best and Worst Performing Years
    Example Insight: "2013 was the best year for business with peak customer counts and sales. 2014 showed a significant decline."

🔁 2. Cumulative Sales Tracking

    Running totals of sales over years
    Rolling averages for average price
    Used functions: SUM() OVER, AVG() OVER, DATETRUNC()

📊 3. Performance Benchmarking

    Product performance vs. average sales
    Year-on-Year comparisons
    Top/bottom performer ranking using RANK() or DENSE_RANK()

🧮 4. Part-to-Whole Analysis

    Share of categories in overall sales
    Example Insight: "Bikes occupied the highest share of the company’s business."

🔍 5. Customer Segmentation

    Grouping by spending behavior (Cost Ranges)
    Methods to classify high, medium, and low-value customers
    Metrics Used: 
        Total Orders
        Total Sales
        Average Monthly Spend
        Time Since Last Order

🧑‍🤝‍🧑 6. Customer Report

    Demographics (name, age, gender, marital status)
    Transaction summaries
    Key KPIs:
        Total Sales per Customer
        Recency (months since last order)
        Frequency (orders per period)
        Monetary (average order value)
    Supports RFM Analysis

📦 7. Product Report

    Product-level metrics:
        Category & Subcategory distribution
        Quantity sold
        Lifespan
        Average Order Revenue
        Monthly Revenue Contribution
    Identify high/mid/low performers

🛠️ Tools & Features

    SQL Window Functions (OVER(), RANK())

    CTEs (WITH clauses)

    Data Aggregation (GROUP BY)

    Date Truncation & Formatting (DATETRUNC, FORMAT)

    Joins across tables (sales, products, customers)

✅ How to Run

    Load the .sql file into your SQL engine (PostgreSQL, SQL Server, etc.).
    Ensure your database has the required tables and columns as outlined.
    Run queries modularly or in sequence for full analysis.
    Interpret insights or visualize them using Power BI/Tableau.

📌 Insights Delivered

    Best and worst sales years
    Monthly seasonality patterns
    Category contribution heatmap
    Customer behavioral segments
    Product profitability mapping

👨‍💻 Author

Shreyak

SQL Developer | Business Analyst | Data Scientist | Data Storyteller

