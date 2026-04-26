import pandas as pd
import sqlite3
import os
import json

print("STARTING CLEAN PIPELINE...")

# RESET DATABASE
db_path = "patents.db"

if os.path.exists(db_path):
    os.remove(db_path)

conn = sqlite3.connect(db_path)

# FOLDERS
os.makedirs("output/cleaned", exist_ok=True)
os.makedirs("output/reports", exist_ok=True)

# SAFE READ SETTINGS
read_opts = dict(
    sep="\t",
    dtype=str,
    chunksize=3000,
    engine="python",
    on_bad_lines="skip",
    encoding="utf-8"
)

# PATENTS
for chunk in pd.read_csv(
    "g_patent.tsv",
    usecols=["patent_id", "patent_title", "patent_date"],
    **read_opts
):
    chunk = chunk.dropna(subset=["patent_id"])

    chunk = chunk.rename(columns={"patent_title": "title"})
    chunk["year"] = pd.to_datetime(chunk["patent_date"], errors="coerce").dt.year

    chunk.to_sql("patents", conn, if_exists="append", index=False)

print("Patents loaded")

# save sample cleaned file
pd.read_sql("SELECT * FROM patents LIMIT 200000", conn)\
  .to_csv("output/cleaned/patents_clean.csv", index=False)


#  ABSTRACTS
for chunk in pd.read_csv(
    "g_patent_abstract.tsv",
    usecols=["patent_id", "patent_abstract"],
    **read_opts
):
    chunk = chunk.rename(columns={"patent_abstract": "abstract"})
    chunk.to_sql("abstracts", conn, if_exists="append", index=False)

print("Abstracts loaded")

# INVENTORS
for chunk in pd.read_csv(
    "g_inventor_disambiguated.tsv",
    usecols=[
        "patent_id",
        "inventor_id",
        "disambig_inventor_name_first",
        "disambig_inventor_name_last",
        "location_id"
    ],
    **read_opts
):
    chunk["name"] = (
        chunk["disambig_inventor_name_first"].fillna("") + " " +
        chunk["disambig_inventor_name_last"].fillna("")
    ).str.strip()

    chunk = chunk[["patent_id", "inventor_id", "name", "location_id"]]
    chunk.to_sql("inventors", conn, if_exists="append", index=False)

print("Inventors loaded")

# COMPANIES
for chunk in pd.read_csv(
    "g_assignee_disambiguated.tsv",
    usecols=["patent_id", "assignee_id", "disambig_assignee_organization"],
    **read_opts
):
    chunk = chunk.rename(columns={
        "assignee_id": "company_id",
        "disambig_assignee_organization": "company_name"
    })

    chunk.to_sql("companies", conn, if_exists="append", index=False)

print("Companies loaded")

#  LOCATIONS 
try:
    locations_df = pd.read_csv(
        "g_location_disambiguated.tsv",
        sep="\t",
        usecols=["location_id", "disambig_country"],
        dtype=str,
        engine="python",
        on_bad_lines="skip"
    )

    locations_df = locations_df.rename(columns={"disambig_country": "country"})

except:
    print("WARNING: Locations file missing or corrupted")
    locations_df = pd.DataFrame(columns=["location_id", "country"])

locations_df.to_sql("locations", conn, if_exists="replace", index=False)
locations_df.to_csv("output/cleaned/locations_clean.csv", index=False)

print("Locations loaded")

# RELATIONSHIPS
conn.execute("DROP TABLE IF EXISTS relationships")

conn.execute("""
CREATE TABLE relationships AS
SELECT
    i.patent_id,
    i.inventor_id,
    i.name,
    i.location_id,
    c.company_id,
    c.company_name
FROM inventors i
LEFT JOIN companies c
ON i.patent_id = c.patent_id
""")

print("Relationships created")

#  ALL 7 REQUIRED QUERIES
# TOP INVENTORS
top_inventors = pd.read_sql("""
SELECT name, COUNT(DISTINCT patent_id) AS total_patents
FROM relationships
GROUP BY name
ORDER BY total_patents DESC
LIMIT 10
""", conn)

# TOP COMPANIES
top_companies = pd.read_sql("""
SELECT company_name, COUNT(DISTINCT patent_id) AS total_patents
FROM relationships
WHERE company_name IS NOT NULL
GROUP BY company_name
ORDER BY total_patents DESC
LIMIT 10
""", conn)

#  COUNTRIES
top_countries = pd.read_sql("""
SELECT l.country, COUNT(DISTINCT r.patent_id) AS total_patents
FROM relationships r
JOIN locations l ON r.location_id = l.location_id
GROUP BY l.country
ORDER BY total_patents DESC
LIMIT 10
""", conn)

#  TRENDS
trends = pd.read_sql("""
SELECT year, COUNT(*) AS total_patents
FROM patents
GROUP BY year
ORDER BY year
""", conn)

# JOIN QUERY
join_query = pd.read_sql("""
SELECT p.patent_id, p.title, r.name, r.company_name
FROM patents p
JOIN relationships r
ON p.patent_id = r.patent_id
LIMIT 20
""", conn)

# CTE QUERY
cte_query = pd.read_sql("""
WITH inventor_summary AS (
    SELECT name, COUNT(DISTINCT patent_id) AS total_patents
    FROM relationships
    GROUP BY name
)
SELECT * FROM inventor_summary
ORDER BY total_patents DESC
LIMIT 10
""", conn)

#  RANKING QUERY
ranking = pd.read_sql("""
SELECT name,
       total_patents,
       RANK() OVER (ORDER BY total_patents DESC) AS rank
FROM (
    SELECT name, COUNT(DISTINCT patent_id) AS total_patents
    FROM relationships
    GROUP BY name
)
""", conn)

#  REPORT EXPORTS
top_inventors.to_csv("output/reports/top_inventors.csv", index=False)
top_companies.to_csv("output/reports/top_companies.csv", index=False)
top_countries.to_csv("output/reports/country_trends.csv", index=False)

total_patents = pd.read_sql(
    "SELECT COUNT(DISTINCT patent_id) FROM patents",
    conn
).iloc[0, 0]

report = {
    "total_patents": int(total_patents),
    "top_inventors": top_inventors.to_dict("records"),
    "top_companies": top_companies.to_dict("records"),
    "top_countries": top_countries.to_dict("records"),
    "trends": trends.to_dict("records")
}

with open("output/reports/report.json", "w") as f:
    json.dump(report, f, indent=4)


#  CONSOLE REPORT (REQUIRED)

print("\n================ PATENT REPORT ================")
print("Total Patents:", total_patents)

print("\nTOP INVENTORS")
print(top_inventors.to_string(index=False))

print("\nTOP COMPANIES")
print(top_companies.to_string(index=False))

print("\nTOP COUNTRIES")
print(top_countries.to_string(index=False))

print("\nPIPELINE COMPLETE")
print("FILES SAVED IN: output/cleaned & output/reports")

conn.close()