-- ============================================================
-- Mutual Fund Analytics — Day 2 Analytical SQL Queries
-- Database: bluestock_mf.db
-- ============================================================


-- 1. Top 5 mutual fund schemes by AUM
SELECT
    scheme_name,
    fund_house,
    ROUND(aum_crore, 2) AS aum_crore
FROM fact_performance
WHERE aum_crore IS NOT NULL
ORDER BY aum_crore DESC
LIMIT 5;


-- 2. Average NAV per month
SELECT
    strftime('%Y-%m', date) AS month,
    ROUND(AVG(nav), 4) AS average_nav
FROM fact_nav
WHERE date IS NOT NULL
  AND nav > 0
GROUP BY strftime('%Y-%m', date)
ORDER BY month;


-- 3. SIP investment and year-over-year growth
WITH yearly_sip AS (
    SELECT
        CAST(strftime('%Y', transaction_date) AS INTEGER) AS year,
        SUM(amount_inr) AS total_sip_amount
    FROM fact_transactions
    WHERE transaction_type = 'SIP'
    GROUP BY CAST(strftime('%Y', transaction_date) AS INTEGER)
),
sip_growth AS (
    SELECT
        year,
        total_sip_amount,
        LAG(total_sip_amount) OVER (ORDER BY year) AS previous_year_amount
    FROM yearly_sip
)
SELECT
    year,
    ROUND(total_sip_amount, 2) AS total_sip_amount,
    ROUND(
        ((total_sip_amount - previous_year_amount)
        / NULLIF(previous_year_amount, 0)) * 100,
        2
    ) AS yoy_growth_pct
FROM sip_growth
ORDER BY year;


-- 4. Transactions and investment amount by state
SELECT
    state,
    COUNT(*) AS transaction_count,
    ROUND(SUM(amount_inr), 2) AS total_investment_inr,
    ROUND(AVG(amount_inr), 2) AS average_transaction_inr
FROM fact_transactions
GROUP BY state
ORDER BY total_investment_inr DESC;


-- 5. Funds with an expense ratio below 1%
SELECT
    scheme_name,
    fund_house,
    category,
    plan,
    expense_ratio_pct
FROM fact_performance
WHERE expense_ratio_pct < 1
ORDER BY expense_ratio_pct ASC;


-- 6. Top 5 funds by five-year return
SELECT
    scheme_name,
    fund_house,
    category,
    ROUND(return_5yr_pct, 2) AS return_5yr_pct
FROM fact_performance
WHERE return_5yr_pct IS NOT NULL
ORDER BY return_5yr_pct DESC
LIMIT 5;


-- 7. Average returns and expense ratio by category
SELECT
    category,
    COUNT(*) AS scheme_count,
    ROUND(AVG(return_1yr_pct), 2) AS avg_1yr_return_pct,
    ROUND(AVG(return_3yr_pct), 2) AS avg_3yr_return_pct,
    ROUND(AVG(return_5yr_pct), 2) AS avg_5yr_return_pct,
    ROUND(AVG(expense_ratio_pct), 2) AS avg_expense_ratio_pct
FROM fact_performance
GROUP BY category
ORDER BY avg_3yr_return_pct DESC;


-- 8. Number of schemes by fund house
SELECT
    fund_house,
    COUNT(DISTINCT amfi_code) AS total_schemes
FROM dim_fund
GROUP BY fund_house
ORDER BY total_schemes DESC, fund_house ASC;


-- 9. Transaction performance by transaction type
SELECT
    transaction_type,
    COUNT(*) AS transaction_count,
    ROUND(SUM(amount_inr), 2) AS total_amount_inr,
    ROUND(AVG(amount_inr), 2) AS average_amount_inr,
    ROUND(MAX(amount_inr), 2) AS maximum_amount_inr
FROM fact_transactions
GROUP BY transaction_type
ORDER BY total_amount_inr DESC;


-- 10. Risk-grade distribution and performance
SELECT
    risk_grade,
    COUNT(*) AS scheme_count,
    ROUND(AVG(return_3yr_pct), 2) AS avg_3yr_return_pct,
    ROUND(AVG(expense_ratio_pct), 2) AS avg_expense_ratio_pct,
    ROUND(AVG(max_drawdown_pct), 2) AS avg_max_drawdown_pct
FROM fact_performance
GROUP BY risk_grade
ORDER BY scheme_count DESC;