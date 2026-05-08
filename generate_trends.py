import sqlite3
import pandas as pd
import os

print("Generating trends dataset...")

# CONNECT TO DATABASE
conn = sqlite3.connect("patents.db")

# CREATE OUTPUT FOLDER IF NOT EXISTS
os.makedirs("output/reports", exist_ok=True)

# QUERY YEARLY PATENT TRENDS
trends = pd.read_sql("""
SELECT year, COUNT(*) AS total_patents
FROM patents
GROUP BY year
ORDER BY year
""", conn)

# SAVE TO CSV
trends.to_csv("output/reports/trends.csv", index=False)

print("Trends file created successfully!")
print(trends.head())

conn.close()