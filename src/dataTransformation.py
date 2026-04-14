import pandas as pd
import numpy as np

# =========================
# 1. Daten einlesen
# =========================
df = pd.read_csv("src/dataProcessed/processedData.csv")
df["date"] = pd.to_datetime(df["date"])
df = df.sort_values("date")

# =========================
# 2. Kopie erstellen
# =========================
df_model = df.copy()

# =========================
# 3. Makro-Transformationen
# =========================

# Sicherheit: nach Zeit sortieren
df_model = df_model.sort_values("date").copy()

# BIP: Quartalswachstum in %
df_model["gdp_growth_qoq"] = df_model["gdp"].pct_change() * 100

# Inflation: Quartalsveränderung des Preisindex in %
df_model["inflation_qoq"] = df_model["inflation"].pct_change() * 100

# Absolute Levels entfernen
df_model = df_model.drop(columns=["gdp", "inflation"])

df_model = df_model.dropna()

# =========================
# 4. Zinsstruktur
# =========================
df_model["term_spread"] = df_model["long_rate"] - df_model["short_rate"]

df_model = df_model.drop(columns=["short_rate", "long_rate"])

# =========================
# 5. Ergebnis speichern
# =========================
df_model.to_csv("src/dataProcessed/modelData.csv", index=False)

print(df_model.head())
print(df_model.shape)