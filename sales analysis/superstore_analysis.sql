-- Superstore Sales Performance Analysis
-- Tool: MySQL 8.0
-- Dataset: Sample Superstore (9,994 records)
CREATE DATABASE sales_analysis;
USE sales_analysis;
USE sales_analysis;

SELECT COUNT(*) AS total_rows
FROM superstore;
SELECT
    order_month,
    ROUND(SUM(Sales), 2) AS total_sales,
    ROUND(SUM(Profit), 2) AS total_profit
FROM (
    SELECT
        DATE_FORMAT(
            CASE
                WHEN `Order Date` LIKE '__/__/____'
                THEN STR_TO_DATE(`Order Date`, '%m/%d/%Y')
                ELSE STR_TO_DATE(`Order Date`, '%Y-%m-%d')
            END,
            '%Y-%m'
        ) AS order_month,
        Sales,
        Profit
    FROM superstore
) AS monthly_data
GROUP BY order_month
ORDER BY order_month;
SELECT
    Category,
    `Sub-Category`,
    ROUND(SUM(Sales), 2) AS Total_Sales,
    ROUND(SUM(Profit), 2) AS Total_Profit,
    ROUND(
        SUM(Profit) / SUM(Sales) * 100, 2
    ) AS Profit_Margin_Percentage
FROM superstore
GROUP BY Category, `Sub-Category`
ORDER BY Total_Profit DESC;
SELECT
    Region,
    ROUND(SUM(Sales), 2) AS Total_Sales,
    ROUND(SUM(Profit), 2) AS Total_Profit,
    ROUND(AVG(Discount) * 100, 2) AS Avg_Discount_Percentage
FROM superstore
GROUP BY Region
ORDER BY Total_Profit DESC;
SELECT
    Segment,
    COUNT(DISTINCT `Customer ID`) AS Total_Customers,
    ROUND(SUM(Sales), 2) AS Total_Sales,
    ROUND(SUM(Profit), 2) AS Total_Profit,
    ROUND(
        SUM(Profit) / SUM(Sales) * 100, 2
    ) AS Profit_Margin_Percentage
FROM superstore
GROUP BY Segment
ORDER BY Total_Profit DESC;
SELECT
    Discount,
    COUNT(*) AS Total_Orders,
    ROUND(SUM(Sales), 2) AS Total_Sales,
    ROUND(SUM(Profit), 2) AS Total_Profit,
    ROUND(
        SUM(Profit) / SUM(Sales) * 100, 2
    ) AS Profit_Margin_Percentage
FROM superstore
GROUP BY Discount
ORDER BY Discount;
SELECT
    `Product Name`,
    `Category`,
    ROUND(SUM(Sales), 2) AS Total_Sales,
    ROUND(SUM(Profit), 2) AS Total_Profit
FROM superstore
GROUP BY `Product Name`, `Category`
ORDER BY Total_Profit DESC
LIMIT 10;
SELECT
    `Product Name`,
    `Category`,
    ROUND(SUM(Sales), 2) AS Total_Sales,
    ROUND(SUM(Profit), 2) AS Total_Profit
FROM superstore
GROUP BY `Product Name`, `Category`
HAVING SUM(Profit) < 0
ORDER BY Total_Profit ASC
LIMIT 10;
SELECT
    `Ship Mode`,
    COUNT(DISTINCT `Order ID`) AS Total_Orders,
    ROUND(SUM(Sales), 2) AS Total_Sales,
    ROUND(SUM(Profit), 2) AS Total_Profit,
    ROUND(SUM(Profit) / SUM(Sales) * 100, 2) AS Profit_Margin
FROM superstore
GROUP BY `Ship Mode`
ORDER BY Total_Profit DESC;
SELECT
    `Customer ID`,
    `Customer Name`,
    COUNT(DISTINCT `Order ID`) AS Total_Orders,
    ROUND(SUM(Sales), 2) AS Total_Sales,
    ROUND(SUM(Profit), 2) AS Total_Profit
FROM superstore
GROUP BY `Customer ID`, `Customer Name`
ORDER BY Total_Sales DESC
LIMIT 10;