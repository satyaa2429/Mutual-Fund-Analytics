# Mutual Fund Analytics Data Dictionary

## dim_fund
Contains master information about mutual fund schemes.

Columns:
- amfi_code
- scheme_name
- fund_house
- category
- sub_category
- plan
- risk_category

## fact_nav
Historical NAV values.

Columns:
- amfi_code
- nav_date
- nav

## fact_transactions
Investor transaction details.

Columns:
- transaction_id
- investor_id
- amfi_code
- transaction_date
- transaction_type
- amount_inr

## fact_performance
Fund performance metrics.

Columns:
- expense_ratio_pct
- return_1yr_pct
- return_3yr_pct
- return_5yr_pct
- risk_grade

## fact_aum
Assets Under Management by year.

Columns:
- fund_house
- year
- aum_cr