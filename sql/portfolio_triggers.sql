SELECT
  DATE_TRUNC('month', d.disb_date) AS month,
  SUM(d.loan_amount) AS total_disbursed,
  COALESCE(SUM(r.amount), 0) AS total_repaid,
  ROUND((
    COALESCE(SUM(r.amount), 0) * 100.0 / NULLIF(SUM(d.loan_amount), 0)
  )::numeric, 2) AS repay_rate_pct
FROM disbursements d
LEFT JOIN repayments r ON d.customer_id = r.customer_id
GROUP BY month
ORDER BY month;