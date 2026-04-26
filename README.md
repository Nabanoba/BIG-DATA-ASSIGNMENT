#  Big Data Patent Analytics System Assignment

# Author
 Name:Nabanoba Yunia  
 Registration Number:23/U/24741/EVE 
 Course: Big Data

# Project Overview
This project performs large-scale analysis of global patent data using Python, Pandas, and SQLite.

It processes raw TSV datasets, cleans and transforms the data, stores it in a relational database, and performs advanced SQL analytics to generate insights and visualizations.

The system demonstrates a full **data engineering pipeline**:  
Raw Data → Cleaning → Database → SQL Analysis → Reports → Graphs 

# Data Processing Approach (Chunk-Based Loading)

Due to the large size of the patent datasets (millions of records), loading the entire dataset into memory at once was inefficient and caused the system to crash.

To address this, chunk-based processing was implemented using Pandas, as shown in the `main.py` file.

Instead of loading the entire dataset at once, the data is read in smaller portions (chunks), processed, and then stored in the database incrementally.

# How It Works
-The dataset is divided into smaller chunks (e.g., 3000 rows at a time)  
-Each chunk is cleaned and transformed  
-The processed chunk is inserted into the SQLite database  
 The process repeats until all data is loaded  

# Why This Approach Was Used
-Prevents memory overflow and system crashes  
-Allows efficient handling of large datasets  
-Improves performance on limited hardware  
-Enables scalable data processing  

# Result
This approach ensures that the system can process millions of records efficiently without running out of memory.

# Objectives
-Clean and process large TSV patent datasets
-Store structured data in SQLite database
-Perform advanced SQL analytics:
   JOIN queries
   CTE (WITH statements)
   Ranking using window functions
-Analyze:
  Top inventors
  Top companies
   Top countries
   Patent trends over time
-Generate graphs and reports
-Ensure reproducibility of results

# Technologies Used
 Python 
 Pandas
 SQLite 
 Matplotlib 
 JSON
 Git & GitHub

# Project Structure
BIG-DATA-ASSIGNMENT 2/
│
├── main.py # Data cleaning + database pipeline
├── analysis.py # SQL analysis (7 queries)
├── graphs.py # Data visualization
│
├── g_patent.tsv # Raw dataset (PATENTS)
├── g_patent_abstract.tsv # Raw dataset (ABSTRACTS)
├── g_inventor_disambiguated.tsv # Raw dataset (INVENTORS)
├── g_assignee_disambiguated.tsv # Raw dataset (COMPANIES)
├── g_location_disambiguated.tsv # Raw dataset (LOCATIONS)
│
├── patents.db # SQLite database (auto-generated)
│
├── output/
│ ├── cleaned/ # Cleaned datasets (CSV)
│ ├── reports/ # Final analysis outputs
│ └── graphs/ # Visualizations (PNG)
│
├── .gitignore
└── README.md


# Dataset Description (TSV Files)
# g_patent.tsv
Contains:
 Patent ID
 Title
 Date of filing
# g_patent_abstract.tsv
Contains:
 Patent ID
 Abstract text

# g_inventor_disambiguated.tsv
Contains:
Inventor ID
 Inventor names
 Patent ID
 Location ID

# g_assignee_disambiguated.tsv
Contains:
 Company (assignee) ID
 Company name
 Patent ID

# g_location_disambiguated.tsv
Contains:
 Location ID
 Country information

# Explanation of Ignored Files (.gitignore)
Some files are excluded from GitHub to improve performance and reduce repository size:

# Large TSV Files
 Raw datasets are very large (millions of rows)
 They can be regenerated using `main.py`
Kept locally for processing only

# Database Files (*.db)
 Auto-generated SQLite database
 Can be recreated anytime
 Not needed for version control

# Cleaned Data (output/cleaned/)
 Intermediate processed datasets
Final results are already stored in reports

# System Files
 `__pycache__/`
`*.pyc`

# SQL Analysis (7 Queries)

# Q1: Top Inventors
Finds inventors with the most patents.

# Q2: Top Companies
Identifies companies owning the most patents.

# Q3: Top Countries
Shows countries producing the most patents.

# Q4: Trends Over Time
Analyzes yearly patent growth.

# Q5: JOIN Query
Combines patents, inventors, and companies.

# Q6: CTE Query
Breaks complex queries into structured steps.

# Q7: Ranking Query
Ranks inventors using SQL window functions.

# Key Insights
- USA leads global patent production
- Samsung and IBM dominate patent ownership
- Patent growth increased significantly after 2000
- Innovation concentrated in Asia, USA, and Europe
- Small group of inventors hold large patent shares

# How to Run the Project
 1. Install dependencies
```bash
pip install pandas matplotlib

2. Run pipeline
     python main.py

3. Run analysis
    python analysis.py

4. Generate graphs
    python graphs.py

Conclusion

This project demonstrates a full big data workflow from raw TSV datasets to meaningful insights using Python and SQL.