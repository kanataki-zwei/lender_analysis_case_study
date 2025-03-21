# Strategic Lending Analysis (SQL)          

The analysis for this project has been done on SQL and the outputs have been stored under `data/cleaned` folder.

## 1. Key Features of the Lending Product

The lending product offered by the target company is designed around short-term microloans with standardized structures.    

Analysis from `key_features.csv` reveals:

- **Loan Tenures**: Most loans fall into short durations like 7, 14, or 30 days, indicating high-frequency repayment cycles.
- **Loan Size**: Average loan amounts vary by tenure, with slightly higher values associated with longer durations.
- **Fees**: The average loan fee ranges between 10% and 20% of the principal, representing significant short-term interest returns.

These characteristics align with a mobile-lending or microfinance model targeting quick liquidity and fast turnover.

---

## 2. Key Performance Metrics and Trends

From `portfolio_triggers.csv` and `kpi_summary.csv`, we observe:

- **Repayment Performance**: Repayment percentages range from 70% to 90% in most months, with a few outlier dips.
- **Repayment Trend**: Monthly repayment rates show stability with slight fluctuations, possibly indicating external factors (economic or seasonal).
- **Active Exposure**: Outstanding credit remains significant and should be monitored closely.

These metrics suggest the lending product is performing reliably but could benefit from enhanced risk detection.

---

## 3. Credit Exposure & Risk Management

From `credit_exposure.csv`:

- A small segment of customers contributes disproportionately to total net exposure.
- There are notable gaps between total disbursed and total repaid among some customer cohorts.

**Current risk management** appears minimal. No tiering, limits, or predictive triggers are being applied to proactively flag underperforming borrowers.

**Recommendation**: Introduce credit scoring, cohort-level exposure tracking, and maximum loan caps based on repayment history.

---

## 4. Provisioning and Write-Off Thresholds

Based on `provisioning_analysis.csv`:

- **Provision 100%**: Customers repaying less than 30% of their loans
- **Provision 50%**: Repayment rate between 30% and 70%
- **Provision 10%**: Repayment rate between 70% and 99.99%

This tiered model allows early detection of credit loss potential and aligns with prudential provisioning practices.

**Recommendation**: Implement automated provisioning policy tied to repayment percentage bands to maintain a healthy reserve buffer.

---

## 5. Portfolio Triggers / Alerts

From `portfolio_triggers.csv`, the following triggers are suggested:

- **Trigger 1**: Alert if monthly repayment rate drops below 70%
- **Trigger 2**: Alert if total monthly disbursed exceeds 25% above average of the last 3 months
- **Trigger 3**: Flag top 10 customers by exposure if their net repayment drops for 2 consecutive months

These thresholds support proactive intervention and can be embedded in a BI dashboard.

---

## 6. Data-Driven Product Design Recommendations

Insights from `product_recommendations.csv` reveal repayment performance by tenure:

- Shorter tenures (7-day) show significantly lower repayment rates compared to 14 or 30-day loans.

**Recommendations:**

- Phase out or revise 7-day loan structure.
- Offer longer tenures with step-up fees to incentivize timely repayment.
- Apply behavioral segmentation to personalize loan offers based on historical repayment behavior.

---

## ✅ Conclusion

The lending product demonstrates strong potential, but proactive credit risk controls, dynamic portfolio monitoring, and product redesign can significantly improve profitability and reduce write-offs.

---

## Appendix

- SQL Files: see `/sql/`
- Output Data: see `/data/cleaned/`
- [Looker Dashboard:](https://lookerstudio.google.com/reporting/1933bca8-52fb-4027-b4ee-259f5d169e83)

---      

# 3-Month Profit/Loss Forecast Analysis (Python)

This section evaluates and compares two forecasting methods applied to projected net profits over the next 3 months.

---

## Forecast Summary

| Forecast Month | Rolling Net Profit (KES) | Regression Net Profit (KES) |
|----------------|---------------------------|------------------------------|
| **2024-09**     | -1,060,816.28             | -662,783.98                  |
| **2024-10**     | -1,060,816.28             | -274,106.79                  |
| **2024-11**     | -1,060,816.28             | 114,570.39                   |

---

## Interpretation

### Rolling Average Forecast
- Assumes that the past 3 months' average net loss continues unchanged.
- Forecasts a **consistent net loss of KES -1,060,816.28** across all 3 months.
- Useful as a conservative baseline but **does not capture improving trends**.

### Linear Regression Forecast
- Models a gradual recovery in profitability.
- Forecasts show **a steady upward trend**, moving from:
  - KES -662,783.98 (Sep)
  - KES -274,106.79 (Oct)
  - to KES **114,570.39 profit** (Nov)

---

## Recommendation

- The **regression model** appears more realistic, especially if recent operational improvements or repayment performance justify the upward trend.
- Consider using the **regression output** for reporting and planning, while **keeping the rolling average as a conservative fallback**.
- If business context supports it, you may also **blend the two models** to balance optimism and caution.

---

### 📎 Next Steps

- Add monthly granularity by customer segments or loan tenure.
- Use actual forecasts to update provisioning policies and marketing targets.



*Prepared by Patrick*
