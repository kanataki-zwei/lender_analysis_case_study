import pandas as pd
import numpy as np
from datetime import datetime
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

# -----------------------------
# 1. Load & Parse Raw Data
# -----------------------------
# Load raw files
disb = pd.read_csv("data/raw/Disbursements.csv")
repay = pd.read_csv("data/raw/Repayments.csv")

# Convert to datetime safely
disb["disb_date"] = pd.to_datetime(disb["disb_date"], errors="coerce")
repay["date_time"] = pd.to_datetime(repay["date_time"], errors="coerce")

# Warn if parsing failed
if disb["disb_date"].isna().any():
    print("⚠️ Warning: Some disbursement dates could not be parsed.")
if repay["date_time"].isna().any():
    print("⚠️ Warning: Some repayment dates could not be parsed.")

# -----------------------------
# 2. Aggregate Monthly Metrics
# -----------------------------
# Extract month
disb["month"] = disb["disb_date"].dt.to_period("M").dt.to_timestamp()
repay["month"] = repay["date_time"].dt.to_period("M").dt.to_timestamp()

# Calculate fee percentage
disb["fee_pct"] = disb["loan_fee"] / disb["loan_amount"]

# Monthly disbursement metrics
monthly_disb = disb.groupby("month").agg(
    total_disbursed=("loan_amount", "sum"),
    total_fees=("loan_fee", "sum"),
    avg_fee_pct=("fee_pct", "mean")
).reset_index()

# Monthly repayments
monthly_repay = repay.groupby("month").agg(
    total_repaid=("amount", "sum")
).reset_index()

# Merge and compute profit
monthly = pd.merge(monthly_disb, monthly_repay, on="month", how="left")
monthly["total_repaid"] = monthly["total_repaid"].fillna(0)
monthly["repayment_rate"] = monthly["total_repaid"] / monthly["total_disbursed"]
monthly["provisioning_amount"] = (1 - monthly["repayment_rate"]) * monthly["total_disbursed"]
monthly["net_profit"] = monthly["total_fees"] - monthly["provisioning_amount"]
monthly["month_index"] = np.arange(len(monthly))

# Round for readability
monthly = monthly.round(2)

# Save intermediate file
monthly.to_csv("data/cleaned/monthly_metrics.csv", index=False)
print("✅ Saved: data/cleaned/monthly_metrics.csv")

# -----------------------------
# 3. Forecast Setup
# -----------------------------
monthly = monthly.sort_values("month")
target_col = "net_profit"

# -----------------------------
# 4. Rolling Average Forecast
# -----------------------------
rolling_mean = monthly[target_col].rolling(window=3).mean()
rolling_forecast = [rolling_mean.iloc[-1]] * 3

# -----------------------------
# 5. Linear Regression Forecast
# -----------------------------
X = monthly[["month_index"]]
y = monthly[target_col]
model = LinearRegression()
model.fit(X, y)

future_indices = np.arange(len(monthly), len(monthly) + 3).reshape(-1, 1)
regression_forecast = model.predict(future_indices)

# -----------------------------
# 6. Accuracy Evaluation
# -----------------------------
def evaluate_forecast(true, predicted, label):
    mae = mean_absolute_error(true, predicted)
    rmse = np.sqrt(mean_squared_error(true, predicted))
    mape = np.mean(np.abs((true - predicted) / true)) * 100
    r2 = r2_score(true, predicted)
    print(f"\n📊 {label} Accuracy:")
    print(f"MAE: {mae:.2f}, RMSE: {rmse:.2f}, MAPE: {mape:.2f}%, R²: {r2:.2f}")

if len(monthly) >= 6:
    actual_last3 = monthly[target_col].iloc[-3:]
    X_test = monthly[["month_index"]].iloc[-3:]
    reg_pred_last3 = model.predict(X_test)

    rolling_preds = [
        rolling_mean.iloc[-3],
        rolling_mean.iloc[-2],
        rolling_mean.iloc[-1]
    ]
    evaluate_forecast(actual_last3, rolling_preds, "Rolling Average")
    evaluate_forecast(actual_last3, reg_pred_last3, "Linear Regression")

# -----------------------------
# 7. Final Forecast Output
# -----------------------------
last_month = monthly["month"].max()
forecast_months = pd.date_range(last_month + pd.DateOffset(months=1), periods=3, freq="MS")

forecast_df = pd.DataFrame({
    "forecast_month": forecast_months.strftime("%Y-%m"),
    "rolling_net_profit": np.round(rolling_forecast, 2),
    "regression_net_profit": np.round(regression_forecast, 2)
})

forecast_df.to_csv("data/cleaned/profit_loss_forecast.csv", index=False)
print("\n✅ Forecast saved to: data/cleaned/profit_loss_forecast.csv")
print(forecast_df)