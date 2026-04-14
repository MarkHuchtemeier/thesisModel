import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("src/dataProcessed/processedData.csv")
df["date"] = pd.to_datetime(df["date"])

# Basic Checks
df.info()
print(df.describe())
print(df.head())

# =========================
# Histogramme
# =========================
numeric_cols = df.select_dtypes(include="number").columns

# alle Histogramme in einem Raster
df[numeric_cols].hist(figsize=(14, 10), bins=20)

plt.tight_layout()
plt.show()

# =========================
# Deskriptive Tabellen
# =========================
# Zusammenfassung
summary = pd.DataFrame({
    "Variable": df.columns,
    "Datentyp": df.dtypes.astype(str),
    "Anzahl": df.count().values
})

#Übersicht Inhalt Variablen
# Datum ausschließen
cols = [col for col in df.columns if col != "date"]

desc = df[cols].describe()

# Nur relevante Kennzahlen
desc = desc.loc[["min", "25%", "50%", "mean", "75%", "max"]]
desc.index = ["Min.", "1st Qu.", "Median", "Mean", "3rd Qu.", "Max."]

# Runden
desc = desc.round(2)

# Optional: schönere Namen (empfohlen)
desc.columns = [
    "Equity", "Derivatives", "Bonds", "Liquidity",
    "Real Estate", "Commodities",
    "Long-Term Share", "Short-Term Share",
    "GDP Growth", "Inflation",
    "Short Rate", "Long Rate"
]

# =========================
# LaTeX Export
# =========================
latex_table = desc.to_latex(
    caption="Descriptive statistics of portfolio and macroeconomic variables",
    label="tab:descriptive_stats",
    float_format="%.4f"
)

summary_table = summary.to_latex(
    index=False,
    caption="Anzahl Beobachtungen und Datentyp je Regressor",
    label="tab:data_summary"
)

print(summary_table)
print(latex_table)