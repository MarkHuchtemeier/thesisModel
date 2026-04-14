import pandas as pd

customer_df = pd.read_csv("src/dataProcessed/customer_data_clean.csv")
customer_df["date"] = pd.to_datetime(customer_df["date"])

# =========================
# 1. Short Rate einlesen
# =========================
short_rate_path = "src/dataRaw/BBIG1.M.D0.EUR.MMKT.EURIBOR.M03.AVE.MA.csv"
short_rate_df = pd.read_csv(
    short_rate_path,
    sep=";",
    skiprows=9,          # erste 9 Zeilen überspringen
    header=None,          # keine Header in Datei
    usecols=[0, 1]
)

# Spaltennamen setzen
short_rate_df.columns = ["date", "short_rate"]

# Datum umwandeln
short_rate_df["date"] = pd.to_datetime(short_rate_df["date"])
short_rate_df["date"] = short_rate_df["date"] + pd.offsets.MonthEnd(0)

# Numerisch machen
short_rate_df["short_rate"] = (
    short_rate_df["short_rate"]
    .astype(str)
    .str.replace(",", ".", regex=False)
    .str.strip()
)
short_rate_df["short_rate"] = pd.to_numeric(short_rate_df["short_rate"], errors="coerce")

# Umwandeln von Prozent in numerisch
short_rate_df["short_rate"] = short_rate_df["short_rate"]

# In Quartale aggregieren
short_rate_df = short_rate_df.set_index("date").resample("QE").mean().reset_index()

# Nur notwendige Quartale behalten
short_rate_df = short_rate_df[
    short_rate_df["date"].isin(customer_df["date"])
]

print(short_rate_df.head())

# =========================
# 2. Long Rate einlesen
# =========================
long_rate_path = "src/dataRaw/BBSSY.D.REN.EUR.A630.000000WT1010.A.csv"
long_rate_df = pd.read_csv(
    long_rate_path,
    sep=";",
    skiprows=9,          # erste 9 Zeilen überspringen
    header=None,          # keine Header in Datei
    usecols=[0, 1]
)

long_rate_df.columns = ["date", "long_rate"]

# Datum umwandeln
long_rate_df["date"] = pd.to_datetime(long_rate_df["date"])
long_rate_df["date"] = long_rate_df["date"] + pd.offsets.MonthEnd(0)

# Numerisch machen
long_rate_df["long_rate"] = (
    long_rate_df["long_rate"]
    .astype(str)
    .str.replace(",", ".", regex=False)
    .str.strip()
)
long_rate_df["long_rate"] = pd.to_numeric(long_rate_df["long_rate"], errors="coerce")

# Umwandeln von Prozent in numerisch
long_rate_df["long_rate"] = long_rate_df["long_rate"]

# In Quartale aggregieren
long_rate_df = long_rate_df.set_index("date").resample("QE").mean().reset_index()

# Nur notwendige Quartale behalten
long_rate_df = long_rate_df[
    long_rate_df["date"].isin(customer_df["date"])
]

print(long_rate_df.head())

# =========================
# 3. Inflation einlesen
# =========================
inflation_path = "src/dataRaw/prc_hicp_midx_linear.csv"
inflation_df = pd.read_csv(
    inflation_path,
    sep=",",
    skiprows=1,          # erste Zeile überspringen
    header=None,          # keine Header in Datei
    usecols=[5, 6, 7]
)

# Spalten benennen
inflation_df.columns = ["country" ,"date", "inflation"]

# Datum umwandeln
inflation_df["date"] = pd.to_datetime(inflation_df["date"])
inflation_df["date"] = inflation_df["date"] + pd.offsets.MonthEnd(0)

# Numerisch machen
inflation_df["inflation"] = (
    inflation_df["inflation"]
    .astype(str)
    .str.replace(",", ".", regex=False)
    .str.strip()
)
inflation_df["inflation"] = pd.to_numeric(inflation_df["inflation"], errors="coerce")

# Unnötige Werte herausfiltern
inflation_df = inflation_df[(inflation_df["country"] == "Germany") & (inflation_df["date"] > "2019-09")]

# Spalte mit Land löschen
inflation_df = inflation_df.drop("country", axis=1)

# In Quartale aggregieren
inflation_df = inflation_df.set_index("date").resample("QE").mean().reset_index()

# Nur notwendige Quartale behalten
inflation_df = inflation_df[
    inflation_df["date"].isin(customer_df["date"])
]

print(inflation_df.head())

# =========================
# 4. BIP einlesen
# =========================
gdp_path = "src/dataRaw/namq_10_gdp_linear.csv"
gdp_df = pd.read_csv(
    gdp_path,
    sep=",",
    skiprows=1,          # erste Zeile überspringen
    header=None,          # keine Header in Datei
    usecols=[6, 7, 8]
)

# Spalten benennen
gdp_df.columns = ["country" ,"date", "gdp"]

# Datum umwandeln
gdp_df["date"] = pd.PeriodIndex(gdp_df["date"], freq="Q").to_timestamp(how="end")

# Numerisch machen
gdp_df["gdp"] = (
    gdp_df["gdp"]
    .astype(str)
    .str.replace(",", ".", regex=False)
    .str.strip()
)
gdp_df["gdp"] = pd.to_numeric(gdp_df["gdp"], errors="coerce")

# Unnötige Werte herausfiltern
gdp_df = gdp_df[(gdp_df["country"] == "Germany") & (gdp_df["date"] > "2019-09")]

# Spalte mit Land löschen
gdp_df = gdp_df.drop("country", axis=1)

# In Quartale aggregieren
gdp_df = gdp_df.set_index("date").resample("QE").mean().reset_index()

# Nur notwendige Quartale behalten
gdp_df = gdp_df[
    gdp_df["date"].isin(customer_df["date"])
]

print(gdp_df.head())

# =========================
# 5. Dataframes mergen
# =========================
customer_df = customer_df.merge(gdp_df, on="date", how="left")
customer_df = customer_df.merge(inflation_df, on="date", how="left")
customer_df = customer_df.merge(short_rate_df, on="date", how="left")
customer_df = customer_df.merge(long_rate_df, on="date", how="left")

# In csv-Datei speichern
output_path = "src/dataProcessed/processedData.csv"
customer_df.to_csv(output_path, index=False)