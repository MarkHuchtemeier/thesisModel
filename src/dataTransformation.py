import pandas as pd

def transform_data():
    print("starting transformation of data")
    # =========================
    # 1. Daten einlesen
    # =========================
    df = pd.read_csv("src/dataProcessed/processedData.csv")
    df["date"] = pd.to_datetime(df["date"])
    df = df.sort_values("date")

    # =========================
    # 2. Basismodell erstellen
    # =========================
    df_model = df.copy()

    # =========================
    # 3. Makro-Transformationen
    # =========================
    df_model = df_model.sort_values("date").copy()

    # BIP: Quartalswachstum in %
    df_model["gdp_growth_qoq"] = df_model["gdp"].pct_change() * 100

    # Inflation: Quartalsveränderung in %
    df_model["inflation_qoq"] = df_model["inflation"].pct_change() * 100

    # Absolute Levels entfernen
    df_model = df_model.drop(columns=["gdp", "inflation"])

    # =========================
    # 4. Zinsstruktur
    # =========================
    df_model["term_spread"] = df_model["long_rate"] - df_model["short_rate"]
    df_model = df_model.drop(columns=["short_rate", "long_rate"])

    # NaNs entfernen
    df_model = df_model.dropna()

    # =========================
    # 5. Basismodell speichern
    # =========================
    df_model.to_csv("src/dataProcessed/modelData.csv", index=False)

    # =========================
    # 6. Lag-Datensatz erstellen
    # =========================
    df_model_lag = df_model.copy()

    # Lags (t-1)
    df_model_lag["gdp_growth_qoq_lag1"] = df_model_lag["gdp_growth_qoq"].shift(1)
    df_model_lag["inflation_qoq_lag1"] = df_model_lag["inflation_qoq"].shift(1)

    # Optional: auch für term_spread
    df_model_lag["term_spread_lag1"] = df_model_lag["term_spread"].shift(1)

    # NaNs entfernen
    df_model_lag = df_model_lag.dropna()

    # =========================
    # Lag-2 Datensatz erstellen
    # =========================
    df_model_lag2 = df_model.copy()

    # Lags (t-2)
    df_model_lag2["gdp_growth_qoq_lag2"] = df_model_lag2["gdp_growth_qoq"].shift(2)
    df_model_lag2["inflation_qoq_lag2"] = df_model_lag2["inflation_qoq"].shift(2)

    # Optional: auch für term_spread
    df_model_lag2["term_spread_lag2"] = df_model_lag2["term_spread"].shift(2)

    # NaNs entfernen (durch Lags)
    df_model_lag2 = df_model_lag2.dropna()

    # =========================
    # 7. Lag-Datensatz speichern
    # =========================
    df_model_lag.to_csv("src/dataProcessed/modelData_lag1.csv", index=False)
    df_model_lag2.to_csv("src/dataProcessed/modelData_lag2.csv", index=False)

    # =========================
    # 8. Output
    # =========================
    print("Baseline:")
    print(df_model.head())
    print(df_model.shape)

    print("\nMit Lags:")
    print(df_model_lag.head())
    print(df_model_lag.shape)

    print("finished transformation of data")