"""
London Housing Market Analysis (1995-2019)
===========================================
A data science project that explores the London housing market using the
"London Housing Data" dataset (UK Government / Land Registry, ONS, Met Police).

Author: MC641033
Course: CISC7204 Data Science and Data Visualization
Date: October 2026

Research question:
    How have London house prices evolved between 1995 and 2019,
    and how do price levels differ across boroughs?

This script:
    1. Loads and cleans the data
    2. Computes summary statistics
    3. Produces three visualizations saved to ./visualizations
    4. Prints the key findings

Run:  python london_housing_analysis.py
"""

import pandas as pd
import numpy as np
import matplotlib
matplotlib.use("Agg")  # headless backend (no display needed)
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import os

# ---------------------------------------------------------------------------
# 1. Load data
# ---------------------------------------------------------------------------
DATA_PATH = os.path.join("data", "London Housing Data.csv")
FIG_DIR = "visualizations"
os.makedirs(FIG_DIR, exist_ok=True)

df = pd.read_csv(DATA_PATH)
print(f"Loaded {len(df):,} records, {df['area'].nunique()} London areas, "
      f"{df['date'].min()} - {df['date'].max()}")

# ---------------------------------------------------------------------------
# 2. Clean data
# ---------------------------------------------------------------------------
# Parse dates (format: d/m/yyyy)
df["date"] = pd.to_datetime(df["date"], format="%d/%m/%Y")
df["year"] = df["date"].dt.year
df["month"] = df["date"].dt.month

# Missing values: crime figures only exist for some areas/years
print(f"Missing values before cleaning: {int(df.isna().sum().sum())}")
crime_df = df.dropna(subset=["no_of_crimes"]).copy()
print(f"Records with crime data: {len(crime_df):,}")

# ---------------------------------------------------------------------------
# 3. Analysis
# ---------------------------------------------------------------------------
# London-wide monthly average price
london_monthly = (
    df.groupby("date")["average_price"]
    .mean()
    .resample("ME")
    .mean()
    .dropna()
)

# Annual average price
annual_price = df.groupby("year")["average_price"].mean()

# Average price by area (overall + latest year)
area_price = df.groupby("area")["average_price"].mean().sort_values(ascending=False)
area_price_latest = (
    df[df["year"] == 2018].groupby("area")["average_price"].mean().sort_values(ascending=False)
)

# ---------------------------------------------------------------------------
# 4. Visualizations
# ---------------------------------------------------------------------------
plt.rcParams.update({
    "figure.dpi": 150,
    "font.size": 10,
    "axes.titlesize": 12,
    "axes.titleweight": "bold",
    "axes.spines.top": False,
    "axes.spines.right": False,
})

# --- Figure 1: London house price trend (1995-2019) ------------------------
fig, ax = plt.subplots(figsize=(9, 4.8))
ax.plot(london_monthly.index, london_monthly.values, color="#1f77b4", lw=2)
ax.set_title("Average House Price in London, 1995 - 2020")
ax.set_xlabel("Year")
ax.set_ylabel("Average price (GBP)")
ax.xaxis.set_major_locator(mdates.YearLocator(4))
ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y"))
ax.grid(True, alpha=0.3)
# Annotate the 2008 financial-crisis dip
crisis = london_monthly.loc["2007-01":"2009-06"]
if len(crisis):
    trough = crisis.idxmin()
    ax.annotate("2008 financial crisis\ndip", xy=(trough, crisis.min()),
                xytext=(mdates.date2num(pd.Timestamp("2002-06-01")), london_monthly.min() * 1.05),
                arrowprops=dict(arrowstyle="->", color="crimson"), color="crimson", fontsize=9)
fig.tight_layout()
fig.savefig(os.path.join(FIG_DIR, "fig1_london_price_trend.png"), bbox_inches="tight")
plt.close(fig)

# --- Figure 2: Top 10 most expensive areas (latest full year 2018) ---------
top10 = area_price_latest.head(10).iloc[::-1]  # ascending for horizontal bar
fig, ax = plt.subplots(figsize=(9, 4.8))
ax.barh(top10.index, top10.values / 1000, color="#2ca02c", alpha=0.85)
ax.set_title("Top 10 London Boroughs by Average House Price (2018)")
ax.set_xlabel("Average price (thousand GBP)")
ax.grid(True, axis="x", alpha=0.3)
for i, v in enumerate(top10.values / 1000):
    ax.text(v + 5, i, f"£{v:,.0f}k", va="center", fontsize=8)
fig.tight_layout()
fig.savefig(os.path.join(FIG_DIR, "fig2_top10_areas.png"), bbox_inches="tight")
plt.close(fig)

# --- Figure 3: House prices vs. crime and sales volume ---------------------
# Borough-level aggregates with crime data
area_stats = (
    crime_df.groupby("area")
    .agg(avg_price=("average_price", "mean"),
         avg_crime=("no_of_crimes", "mean"),
         total_sold=("houses_sold", "sum"))
)
fig, ax = plt.subplots(figsize=(9, 4.8))
sc = ax.scatter(area_stats["avg_crime"], area_stats["avg_price"] / 1000,
                s=area_stats["total_sold"] / area_stats["total_sold"].max() * 300 + 20,
                alpha=0.7, color="#ff7f0e", edgecolor="white")
ax.set_title("House Price vs. Crime Rate across London Boroughs")
ax.set_xlabel("Average monthly crimes")
ax.set_ylabel("Average house price (thousand GBP)")
ax.grid(True, alpha=0.3)
# Simple trend line
z = np.polyfit(area_stats["avg_crime"], area_stats["avg_price"] / 1000, 1)
p = np.poly1d(z)
xs = np.linspace(area_stats["avg_crime"].min(), area_stats["avg_crime"].max(), 100)
ax.plot(xs, p(xs), "k--", lw=1, alpha=0.6, label="linear trend")
ax.legend(loc="upper right")
fig.tight_layout()
fig.savefig(os.path.join(FIG_DIR, "fig3_price_vs_crime.png"), bbox_inches="tight")
plt.close(fig)

print(f"\nVisualizations saved to ./{FIG_DIR}")

# ---------------------------------------------------------------------------
# 5. Key findings (printed for reproducibility)
# ---------------------------------------------------------------------------
overall_growth = (london_monthly.iloc[-1] / london_monthly.iloc[0] - 1) * 100
print("\n=== KEY FINDINGS ===")
print(f"London average price: GBP {london_monthly.iloc[0]:,.0f} (1995) -> "
      f"GBP {london_monthly.iloc[-1]:,.0f} ({london_monthly.index[-1].year}), "
      f"+{overall_growth:.0f}% over the period")
print(f"Peak annual average: GBP {annual_price.max():,.0f} in {annual_price.idxmax()}")
print(f"Most expensive borough (2018): {area_price_latest.index[0]} "
      f"(GBP {area_price_latest.iloc[0]:,.0f})")
print(f"Least expensive borough (2018): {area_price_latest.index[-1]} "
      f"(GBP {area_price_latest.iloc[-1]:,.0f})")
print(f"Price-crime correlation: {area_stats['avg_price'].corr(area_stats['avg_crime']):.2f}")
print(f"Total houses sold (recorded): {int(df['houses_sold'].sum()):,}")
