WITH customer_loans AS (
  SELECT
    d.customer_id,
    SUM(d.loan_amount) AS total_disbursed,
    COALESCE(SUM(r.amount), 0) AS total_repaid,
    ROUND((
      COALESCE(SUM(r.amount), 0) * 100.0 / NULLIF(SUM(d.loan_amount), 0)
    )::numeric, 2) AS repay_pct
  FROM disbursements d
  LEFT JOIN repayments r ON d.customer_id = r.customer_id
  GROUP BY d.customer_id
)
SELECT
  customer_id,
  total_disbursed,
  total_repaid,
  repay_pct,
  CASE
    WHEN repay_pct < 30 THEN 'Provision 100%'
    WHEN repay_pct BETWEEN 30 AND 70 THEN 'Provision 50%'
    WHEN repay_pct BETWEEN 70 AND 99.99 THEN 'Provision 10%'
    ELSE 'No Provision'
  END AS provisioning_recommendation
FROM customer_loans
ORDER BY repay_pct ASC;