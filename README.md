# London Housing Market Analysis (1995 - 2020)

A data science project exploring how London house prices evolved between 1995 and 2020
and how price levels differ across the 45 London boroughs.

## Research Question

> How have average house prices in London changed from 1995 to 2020, and which
> boroughs are the most / least expensive? Is there a visible relationship
> between house prices, sales volume, and recorded crime?

## Dataset

- **Source:** *London Housing Data* (UK Land Registry house price data, Office for
  National Statistics, and Metropolitan Police crime statistics, aggregated by
  borough and month).
- **File:** `data/London Housing Data.csv`
- **Size:** 13,549 records, 45 areas, monthly from 1995-01 to 2020-01.
- **Fields:** `date`, `area`, `average_price`, `code`, `houses_sold`, `no_of_crimes`.
- **Usage permission:** public / open statistical data released by UK government
  agencies for research and educational use; contains no personal or sensitive data.

## Methods & Tools

- **Language:** Python 3
- **Libraries:** pandas (data wrangling), matplotlib (visualization), numpy
- **Steps:** data loading → date parsing → missing-value handling → monthly /
  yearly aggregation → borough-level comparison → correlation check → plotting

## Key Findings

1. London's average house price rose from **GBP ~76k (1995)** to **GBP ~463k
   (early 2020)**, an increase of about **+511%** over 25 years.
2. Prices dipped visibly during the **2008 financial crisis**, then recovered
   and continued to climb to a peak annual average of **GBP ~470k in 2017**.
3. The most expensive borough (2018) is **Kensington and Chelsea**
   (GBP ~1.36M); the least expensive is **North East** (GBP ~128k) — a ~10x gap.
4. A mild positive correlation (**r ≈ 0.29**) exists between average price and
   average monthly crimes at borough level, driven mainly by high-price
   inner-London boroughs also reporting higher crime counts.

## Limitations

- **Crime data are incomplete**: about 45% of rows have missing `no_of_crimes`,
  so the price–crime relationship is based on a subset of boroughs/months and
  should be read as suggestive, not causal.
- Average-price is a simple mean per borough/month; it does not control for
  housing type, size, or transaction mix.

## How to Run

```bash
# 1. Clone the repository
git clone https://github.com/<your-github-username>/data-science-project.git
cd data-science-project

# 2. (Optional) create a virtual environment
python -m venv .venv
source .venv/bin/activate      # Windows: .venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run the analysis (figures are saved to ./visualizations)
python london_housing_analysis.py
```

## Repository Layout

```
data-science-project/
├── README.md                     # this file
├── requirements.txt              # Python dependencies
├── london_housing_analysis.py    # analysis script (re-runnable)
├── london_housing_analysis.ipynb # same analysis as a Jupyter notebook
├── data/
│   └── London Housing Data.csv   # public dataset
└── visualizations/
    ├── fig1_london_price_trend.png
    ├── fig2_top10_areas.png
    └── fig3_price_vs_crime.png
```

---
*CISC7204 Data Science and Data Visualization — Practice 09 portfolio project.*
