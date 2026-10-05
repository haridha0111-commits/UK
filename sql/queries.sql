-- Run these statements against data/fabric.db with SQLite 3.
-- The database is rebuilt by `python pipeline/run_pipeline.py`.

-- 1. Find highest percentage change; always show source-period base counts.
SELECT product, product_group, prior_period, prior_complaints,
       latest_period, latest_complaints, absolute_change, percentage_change
FROM gold_product_half_year_change
ORDER BY ABS(percentage_change) DESC
LIMIT 10;

-- 2. Trace one Gold product back to the Silver source periods.
SELECT product, product_group, reporting_period, complaints_opened
FROM silver_product_complaints
WHERE product = 'Overdrafts'
ORDER BY reporting_period;

-- 3. Market outcomes are separate source measures, not joined complaint events.
SELECT reporting_period, complaints_closed, complaints_upheld, upheld_pct,
       total_redress_gbp, average_redress_upheld_gbp
FROM silver_market_outcomes
ORDER BY reporting_period;

-- 4. Inspect missing contextual-rate values. NULL is retained and is not zero.
SELECT reporting_period, COUNT(*) AS source_categories,
       SUM(CASE WHEN complaints_per_1000 IS NULL THEN 1 ELSE 0 END) AS null_rate_cells
FROM silver_product_context
GROUP BY reporting_period
ORDER BY reporting_period;

-- 5. Product-group aggregate derived by this project; reconcile before external use.
SELECT reporting_period, product_group, complaints_opened
FROM gold_product_group_period_totals
ORDER BY reporting_period, complaints_opened DESC;
