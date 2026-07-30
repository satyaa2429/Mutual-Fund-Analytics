-- Top 5 Funds by Expense Ratio
SELECT scheme_name, expense_ratio_pct
FROM fact_performance
ORDER BY expense_ratio_pct DESC
LIMIT 5;

-- Average Expense Ratio
SELECT AVG(expense_ratio_pct)
FROM fact_performance;

-- Fund Count by Category
SELECT category, COUNT(*)
FROM dim_fund
GROUP BY category;

-- Average Returns
SELECT
AVG(return_1yr_pct) AS Avg1Year,
AVG(return_3yr_pct) AS Avg3Year,
AVG(return_5yr_pct) AS Avg5Year
FROM fact_performance;

-- Risk Category Distribution
SELECT risk_grade, COUNT(*)
FROM fact_performance
GROUP BY risk_grade;