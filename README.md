# IPL Cricket Analysis

This project contains a structured IPL cricket analysis workflow for cleaning, exploratory data analysis, SQL analytics, and plotting visuals for a Power BI dashboard.

## Folder structure

- `data/` — raw IPL CSV files
- `analysis/` — Python-based EDA and data cleaning script
- `sql/` — analytical SQL queries
- `outputs/` — cleaned CSVs and generated charts
- `powerbi/` — target folder for the final Power BI dashboard file

## How to run

1. Install required packages:
   ```bash
   pip install -r requirements.txt
   ```
2. Run the analysis workflow:
   ```bash
   python analysis/ipl_eda.py
   ```
3. Use SQL in `sql/ipl_queries.sql` for business-level analytics.

## Deliverables prepared for Power BI

- Cleaned match and delivery datasets
- Trend and comparison charts
- KPI summary CSV for dashboard metrics
- Reusable SQL queries for additional analytical views
