SELECT
  DATE_TRUNC('month', disb_date) AS month,
  SUM(loan_amount) AS total_disbursed
FROM disbursements
GROUP BY 1
ORDER BY 1;
