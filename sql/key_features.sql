-- Loan Tenure Breakdown (PostgreSQL-compatible)
SELECT
  tenure,
  COUNT(*) AS total_loans,
  ROUND(AVG(loan_amount)::numeric, 2) AS avg_loan_amount,
  ROUND(AVG(loan_fee)::numeric, 2) AS avg_loan_fee,
  ROUND(AVG(loan_fee * 100.0 / loan_amount)::numeric, 2) AS avg_fee_pct
FROM disbursements
GROUP BY tenure
ORDER BY total_loans DESC;