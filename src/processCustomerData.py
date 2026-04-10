import pandas as pd

# Pfad Kundendaten
file_path = "src/dataRaw/portfolio_data.csv"

# CSV einlesen
df = pd.read_csv(file_path, sep=";")

# Spaltennamen vereinheitlichen
df = df.rename(columns={
    "maturity_3y": "maturity_0y_3y",
    "maturity_3y-5y": "maturity_3y_5y",
    "maturity_5y-7y": "maturity_5y_7y",
    "maturity_7y-10y": "maturity_7y_10y",
    "maturity_10y-15y": "maturity_10y_15y",
    "maturity_15y-20y": "maturity_15y_20y",
    "maturity_20y-30y": "maturity_20y_30y",
    "maturity_30y+": "maturity_30y_plus"
})

# Datum umwandeln
df["date"] = pd.to_datetime(df["date"], dayfirst=True, errors="coerce")
numeric_cols = [col for col in df.columns if col != "date"]

for col in numeric_cols:
    df[col] = (
        df[col]
        .astype(str)                         # alles zu String
        .str.replace("%", "", regex=False)   # Prozentzeichen entfernen
        .str.replace(",", ".", regex=False)  # deutsches Komma → Punkt
        .str.strip()                         # Leerzeichen entfernen
    )
    
    df[col] = pd.to_numeric(df[col], errors="coerce")

# Variable für lange und kurze Zeit einfügen
df["long_term_share"] = (
    df["maturity_5y_7y"]
    +df["maturity_7y_10y"]
    +df["maturity_10y_15y"]
    + df["maturity_15y_20y"]
    + df["maturity_20y_30y"]
    + df["maturity_30y_plus"]
)

df["short_term_share"] = df["maturity_0y_3y"] + df["maturity_3y_5y"]

df["short_term_share"] = df["short_term_share"].round(3)
df["long_term_share"] = df["long_term_share"].round(3)

# Alten maturity-Spalten löschen
cols_to_drop = [
    "maturity_0y_3y",
    "maturity_3y_5y",
    "maturity_5y_7y",
    "maturity_7y_10y",
    "maturity_10y_15y",
    "maturity_15y_20y",
    "maturity_20y_30y",
    "maturity_30y_plus"
]

df = df.drop(columns=cols_to_drop)

# Kurzer Check
print(df.head())
#print(df.shape)
#print(df.isna().sum())
#print(df.describe())

# Bereinigte Datei speichern
output_path = "src/dataProcessed/customer_data_clean.csv"
df.to_csv(output_path, index=False)