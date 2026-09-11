# IPL Cricket Analysis

This project contains a structured IPL cricket analysis workflow for cleaning, exploratory data analysis, SQL analytics, and plotting visuals for a Power BI dashboard.

## Folder structure

- `data/` — raw IPL CSV files
- `analysis/` — Python-based EDA and data cleaning script
- `sql/` — analytical SQL queries
- `outputs/` — cleaned CSVs and generated charts
- `powerbi/` — target folder for the final Power BI dashboard file

## How to download and run the project

### 1. Clone the repository

Make sure Git and Python 3.10 or later are installed, then run:

```bash
git clone https://github.com/sashibitcode/IPL-Cricket-Analysis.git
cd IPL-Cricket-Analysis
```

### 2. Create and activate a virtual environment (recommended)

On Windows PowerShell:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

On macOS or Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install the required Python packages

```bash
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

### 4. Run the analysis workflow

Run the following command from the project root directory:

```bash
python analysis/ipl_eda.py
```

The script reads the raw files from `data/` and creates or updates:

- `data/matches_clean.csv` — cleaned match data
- `data/deliveries_clean.csv` — cleaned delivery data
- `outputs/ipl_summary.csv` — summary KPIs
- `outputs/plots/` — generated analysis charts

### 5. Use the SQL queries (optional)

Open `sql/ipl_queries.sql` in your preferred SQL editor or database tool. The queries can be used for additional IPL analytics after loading the CSV files into a database.

### 6. Open the results in Power BI (optional)

1. Open Power BI Desktop.
2. Import `data/matches_clean.csv` and `data/deliveries_clean.csv`.
3. Import `outputs/ipl_summary.csv` for KPI cards.
4. Use the charts in `outputs/plots/` as references for building the dashboard.
5. Save the final Power BI report as a `.pbix` file inside the `powerbi/` folder.

### Troubleshooting

- Run all commands from the `IPL-Cricket-Analysis` project root directory.
- If `python` is not recognized on Windows, install Python and enable **Add Python to PATH** during installation.
- If PowerShell blocks virtual environment activation, run PowerShell as your user and use:
  ```powershell
  Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
  ```
- To leave the virtual environment, run `deactivate`.

## Deliverables prepared for Power BI

- Cleaned match and delivery datasets
- Trend and comparison charts
- KPI summary CSV for dashboard metrics
- Reusable SQL queries for additional analytical views
