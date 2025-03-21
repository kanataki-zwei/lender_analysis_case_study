SELECT
  (SELECT COUNT(DISTINCT customer_id) FROM disbursements) AS unique_borrowers,
  (SELECT ROUND(AVG(loan_amount)::numeric, 2) FROM disbursements) AS avg_loan_amount,
  (SELECT SUM(loan_amount) FROM disbursements) AS total_disbursed,
  (SELECT SUM(amount) FROM repayments) AS total_repaid,
  (
    SELECT ROUND(
      (SUM(d.loan_amount) - COALESCE(SUM(r.amount), 0))::numeric,
      2
    )
    FROM disbursements d
    LEFT JOIN repayments r ON d.customer_id = r.customer_id
  ) AS total_credit_exposure;