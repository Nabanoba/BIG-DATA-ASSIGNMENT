import streamlit as st
import pandas as pd

# PAGE CONFIG
st.set_page_config(page_title="Patent Analytics Dashboard", layout="wide")

st.title("📊 Patent Analytics Dashboard")
# LOAD DATA SAFELY
try:
    inventors = pd.read_csv("output/reports/top_inventors.csv")
    companies = pd.read_csv("output/reports/top_companies.csv")
    countries = pd.read_csv("output/reports/country_trends.csv")
except Exception as e:
    st.error(f"Missing report files: {e}")
    st.stop()

# LOAD TOTALS FROM CSVs 
try:
    total_patents = pd.read_csv("output/reports/top_inventors.csv")  # fallback method
    total_patents_value = "Use report.json or SQL query"
except:
    total_patents_value = "N/A"

# BEST METHOD: derive from SQL output if available via CSV fallback
try:
    import sqlite3
    conn = sqlite3.connect("patents.db")
    total_patents_value = pd.read_sql(
        "SELECT COUNT(DISTINCT patent_id) AS total FROM patents",
        conn
    ).iloc[0, 0]
except:
    total_patents_value = "N/A"

# DERIVED COUNTS
total_inventors = len(inventors)
total_companies = len(companies)
total_countries = len(countries)

# KPI SECTION
st.header("📌 Key Insights")

# KPI ROW 1 (MAIN STATS)
col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Total Patents",
    f"{total_patents_value:,}" if isinstance(total_patents_value, int) else total_patents_value
)

col2.metric("Top Inventor", inventors.iloc[0]["name"] if not inventors.empty else "N/A")

col3.metric("Top Company", companies.iloc[0]["company_name"] if not companies.empty else "N/A")

col4.metric("Top Country", countries.iloc[0]["country"] if not countries.empty else "N/A")



# KPI ROW 2 (TOTAL COUNTS)

col5, col6, col7 = st.columns(3)

# LAYOUT STYLE (SMALLER GRAPHS)

st.markdown("---")


# TOP INVENTORS
st.subheader("🥇 Top Inventors")

colA, colB = st.columns([2, 1])
with colA:
    st.bar_chart(inventors.set_index("name")["total_patents"])
with colB:
    st.dataframe(inventors)


# TOP COMPANIES
st.subheader("🏢 Top Companies")

colA, colB = st.columns([2, 1])
with colA:
    st.bar_chart(companies.set_index("company_name")["total_patents"])
with colB:
    st.dataframe(companies)

# TOP COUNTRIES
st.subheader("🌍 Top Countries")

colA, colB = st.columns([2, 1])
with colA:
    st.bar_chart(countries.set_index("country")["total_patents"])
with colB:
    st.dataframe(countries)


# OPTIONAL PREDICTIONS
st.markdown("---")
st.subheader("📈 Patent Prediction")

try:
    preds = pd.read_csv("output/reports/predictions.csv")
    st.line_chart(preds.set_index("year"))
except:
    st.info("Run predict.py to generate predictions.") 