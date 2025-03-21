-- Credit Exposure Per Customer
SELECT
  d.customer_id,
  SUM(d.loan_amount) AS total_disbursed,
  COALESCE(SUM(r.amount), 0) AS total_repaid,
  SUM(d.loan_amount) - COALESCE(SUM(r.amount), 0) AS net_exposure
FROM disbursements d
LEFT JOIN repayments r ON d.customer_id = r.customer_id
GROUP BY d.customer_id
ORDER BY net_exposure DESC;