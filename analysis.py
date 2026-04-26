import pandas as pd
import sqlite3
import os

print("RUNNING ADVANCED ANALYSIS...")

# connect to database
conn = sqlite3.connect("patents.db")

os.makedirs("output/reports", exist_ok=True)

# JOIN QUERY
join_df = pd.read_sql("""
SELECT p.patent_id,
       p.title,
       r.name AS inventor,
       r.company_name
FROM patents p
JOIN relationships r
ON p.patent_id = r.patent_id
LIMIT 20
""", conn)

join_df.to_csv("output/reports/join_results.csv", index=False)

print("\nJOIN QUERY SAMPLE:")
print(join_df.head())

# CTE QUERY
cte_df = pd.read_sql("""
WITH inventor_summary AS (
    SELECT name, COUNT(*) AS total_patents
    FROM relationships
    GROUP BY name
)
SELECT *
FROM inventor_summary
ORDER BY total_patents DESC
LIMIT 10
""", conn)

cte_df.to_csv("output/reports/cte_results.csv", index=False)

print("\nCTE RESULTS:")
print(cte_df)

# RANKING QUERY
ranking_df = pd.read_sql("""
SELECT name,
       total_patents,
       RANK() OVER (ORDER BY total_patents DESC) AS rank
FROM (
    SELECT name, COUNT(*) AS total_patents
    FROM relationships
    GROUP BY name
)
LIMIT 10
""", conn)

ranking_df.to_csv("output/reports/ranking.csv", index=False)

print("\nRANKING RESULTS:")
print(ranking_df)

# INSIGHTS
print("\n===== INSIGHTS =====")

top = ranking_df.iloc[0]
print(f"Top ranked inventor: {top['name']} (Rank {top['rank']})")

print("JOIN shows relationship between patents, inventors, and companies")
print("CTE simplifies complex aggregation")
print("RANKING orders inventors using window functions")

print("\nANALYSIS COMPLETE")

conn.close()