import pandas as pd
from sqlalchemy import create_engine

# Load CSVs
disb = pd.read_csv("data/raw/Disbursements.csv")
repay = pd.read_csv("data/raw/Repayments.csv")

# Clean disbursement date and tenure
disb['disb_date'] = pd.to_datetime(disb['disb_date'], errors='coerce')
disb['tenure_days'] = disb['tenure'].str.extract(r'(\d+)').astype(float)

# Clean repayment date
repay['date_time'] = pd.to_datetime(repay['date_time'], errors='coerce')

# Save cleaned versions
disb.to_csv("data/cleaned/disbursements_clean.csv", index=False)
repay.to_csv("data/cleaned/repayments_clean.csv", index=False)

# Connect to Postgres
engine = create_engine("postgresql://bi_user:bi_pass@localhost:5438/bi_db")

# Load into DB
disb.to_sql("disbursements", engine, if_exists="replace", index=False)
repay.to_sql("repayments", engine, if_exists="replace", index=False)

print("✅ Data loaded into PostgreSQL")
