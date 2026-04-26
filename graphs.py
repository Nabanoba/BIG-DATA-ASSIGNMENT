import pandas as pd
import matplotlib.pyplot as plt
import os

# CREATE GRAPH FOLDER
os.makedirs("output/graphs", exist_ok=True)

# SAFE FILE LOADING
def load_file(path):
    if os.path.exists(path):
        return pd.read_csv(path)
    else:
        print(f"Missing file: {path}")
        return None

top_inventors = load_file("output/reports/top_inventors.csv")
top_companies = load_file("output/reports/top_companies.csv")
top_countries = load_file("output/reports/country_trends.csv")
trends = load_file("output/reports/trends.csv")  # optional

#TOP INVENTORS GRAPH
if top_inventors is not None:
    plt.figure()
    plt.barh(top_inventors["name"], top_inventors["total_patents"])
    plt.title("Top Inventors by Patent Count")
    plt.xlabel("Number of Patents")
    plt.ylabel("Inventor")
    plt.gca().invert_yaxis()

    plt.savefig("output/graphs/top_inventors.png")
    plt.close()


# TOP COMPANIES GRAPH
if top_companies is not None:
    plt.figure()
    plt.barh(top_companies["company_name"], top_companies["total_patents"])
    plt.title("Top Companies by Patent Count")
    plt.xlabel("Number of Patents")
    plt.ylabel("Company")
    plt.gca().invert_yaxis()

    plt.savefig("output/graphs/top_companies.png")
    plt.close()

# TOP COUNTRIES GRAPH
if top_countries is not None:
    plt.figure()
    plt.bar(top_countries["country"], top_countries["total_patents"])
    plt.title("Top Countries by Patent Production")
    plt.xlabel("Country")
    plt.ylabel("Number of Patents")

    plt.savefig("output/graphs/top_countries.png")
    plt.close()

# TRENDS GRAPH
if trends is not None:
    plt.figure()
    plt.plot(trends["year"], trends["total_patents"])
    plt.title("Patent Trends Over Time")
    plt.xlabel("Year")
    plt.ylabel("Number of Patents")

    plt.savefig("output/graphs/patent_trends.png")
    plt.close()

# ANALYSIS (TEXT OUTPUT)
print("\n===== ANALYSIS =====")

if top_inventors is not None:
    top = top_inventors.iloc[0]
    print(f"Top Inventor: {top['name']} with {top['total_patents']} patents")

if top_companies is not None:
    top = top_companies.iloc[0]
    print(f"Top Company: {top['company_name']} with {top['total_patents']} patents")

if top_countries is not None:
    top = top_countries.iloc[0]
    print(f"Top Country: {top['country']} with {top['total_patents']} patents")

if trends is not None:
    peak = trends.loc[trends["total_patents"].idxmax()]
    print(f"Peak Year: {int(peak['year'])} with {int(peak['total_patents'])} patents")

print("\nGraphs saved in: output/graphs")
print("DONE")