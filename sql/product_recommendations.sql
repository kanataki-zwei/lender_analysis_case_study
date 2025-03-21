SELECT
  d.tenure,
  COUNT(DISTINCT d.customer_id) AS borrowers,
  ROUND((
    SUM(COALESCE(r.amount, 0)) * 100.0 / NULLIF(SUM(d.loan_amount), 0)
  )::numeric, 2) AS overall_repay_pct
FROM disbursements d
LEFT JOIN repayments r ON d.customer_id = r.customer_id
GROUP BY d.tenure
ORDER BY overall_repay_pct DESC;