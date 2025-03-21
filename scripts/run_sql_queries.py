import os
import pandas as pd
from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError

# PostgreSQL connection config
engine = create_engine("postgresql://bi_user:bi_pass@localhost:5438/bi_db")

# Folder paths
sql_dir = "sql"
output_dir = "data/cleaned"
os.makedirs(output_dir, exist_ok=True)

# Queries to run
queries = {
    "key_features": "key_features.sql",
    "credit_exposure": "credit_exposure.sql",
    "provisioning_analysis": "provisioning_analysis.sql",
    "portfolio_triggers": "portfolio_triggers.sql",
    "product_recommendations": "product_recommendations.sql",
    "kpi_summary": "kpi_summary.sql"
}

# Run each query with auto-rollback on failure
with engine.connect() as connection:
    for name, filename in queries.items():
        sql_path = os.path.join(sql_dir, filename)
        try:
            print(f"▶️ Running query: {name}")
            with open(sql_path, "r") as file:
                sql = file.read()

            # Begin transaction (safe mode)
            trans = connection.begin()

            # Execute query
            df = pd.read_sql(text(sql), connection)

            # Commit if successful
            trans.commit()

            # Save output
            output_path = os.path.join(output_dir, f"{name}.csv")
            df.to_csv(output_path, index=False)
            print(f"✅ Saved: {output_path}\n")

        except SQLAlchemyError as e:
            # Roll back failed transaction
            if 'trans' in locals():
                trans.rollback()
            print(f"❌ Error running '{name}' from {filename}")
            print(f"   👉 {str(e)}\n")