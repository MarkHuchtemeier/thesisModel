from pathlib import Path

import pandas as pd
import numpy as np

from sklearn.model_selection import TimeSeriesSplit, cross_val_score
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.neural_network import MLPRegressor

def modelling_mlp():
    # --------------------------------------------------
    # Daten laden
    # --------------------------------------------------
    data_path = Path("src/dataProcessed/modelData.csv")

    df = pd.read_csv(data_path)

    # Falls eine Datumsspalte existiert, sinnvollerweise sortieren
    if "date" in df.columns:
        df["date"] = pd.to_datetime(df["date"], errors="coerce")
        df = df.sort_values("date").reset_index(drop=True)

    # --------------------------------------------------
    # Variablen festlegen
    # --------------------------------------------------
    features = [
        "short_term_share",
        "inflation_qoq",
        "gdp_growth_qoq"
    ]

    target = "liquidity"

    required_columns = features + [target]

    # Prüfen, ob alle benötigten Spalten vorhanden sind
    missing_columns = [col for col in required_columns if col not in df.columns]
    if missing_columns:
        raise ValueError(
            f"Diese benötigten Spalten fehlen im DataFrame: {missing_columns}\n"
            f"Vorhandene Spalten sind: {list(df.columns)}"
        )

    # --------------------------------------------------
    # Modell-Datensatz vorbereiten
    # --------------------------------------------------
    df_model = df[required_columns].copy()

    # Alle Modellspalten sicherheitshalber numerisch machen
    for col in required_columns:
        df_model[col] = pd.to_numeric(df_model[col], errors="coerce")

    # Fehlende Werte entfernen
    df_model = df_model.dropna()

    # Prüfen, ob noch genug Beobachtungen übrig sind
    n_obs = len(df_model)
    if n_obs < 8:
        raise ValueError(
            f"Zu wenige Beobachtungen nach dropna(): {n_obs}. "
            "Für TimeSeriesSplit und ein MLP ist das zu wenig."
        )

    X = df_model[features]
    y = df_model[target]

    # --------------------------------------------------
    # Pipeline: Skalierung + MLP
    # --------------------------------------------------
    mlp_model = Pipeline([
        ("scaler", StandardScaler()),
        ("mlp", MLPRegressor(
            hidden_layer_sizes=(3,),
            activation="relu",
            solver="lbfgs",
            alpha=0.1,
            max_iter=5000,
            random_state=42
        ))
    ])

    # --------------------------------------------------
    # Zeitreihen-CV
    # --------------------------------------------------
    # Bei sehr kleinen Datensätzen lieber nicht zu viele Splits wählen
    n_splits = min(4, n_obs - 1)
    if n_splits < 2:
        raise ValueError("Zu wenige Beobachtungen für TimeSeriesSplit.")

    tscv = TimeSeriesSplit(n_splits=n_splits)

    # --------------------------------------------------
    # Cross Validation
    # --------------------------------------------------
    mae_scores = -cross_val_score(
        mlp_model,
        X,
        y,
        cv=tscv,
        scoring="neg_mean_absolute_error"
    )

    rmse_scores = np.sqrt(-cross_val_score(
        mlp_model,
        X,
        y,
        cv=tscv,
        scoring="neg_mean_squared_error"
    ))

    r2_scores = cross_val_score(
        mlp_model,
        X,
        y,
        cv=tscv,
        scoring="r2"
    )

    # --------------------------------------------------
    # Ergebnisse ausgeben
    # --------------------------------------------------
    print("Anzahl Beobachtungen:", n_obs)
    print("Verwendete Features:", features)
    print()

    print("MAE je Fold:", mae_scores)
    print("RMSE je Fold:", rmse_scores)
    print("R² je Fold:", r2_scores)
    print()

    print("Mittlere MAE:", mae_scores.mean())
    print("Mittlere RMSE:", rmse_scores.mean())
    print("Mittleres R²:", r2_scores.mean())

    # =========================
    # LaTeX-Tabelle: MLP-Konfiguration
    # =========================
    config_df = pd.DataFrame({
        "Parameter": [
            "Library",
            "Modell",
            "Features",
            "Zielvariable",
            "Hidden Layer",
            "Aktivierungsfunktion",
            "Solver",
            "Regularisierung alpha",
            "Max. Iterationen",
            "Cross-Validation"
        ],
        "Ausprägung": [
            "scikit-learn",
            "MLPRegressor",
            ", ".join(features),
            target,
            "(3,)",
            "relu",
            "lbfgs",
            "0.1",
            "5000",
            f"TimeSeriesSplit mit {n_splits} Splits"
        ]
    })

    #print(config_df.to_latex(
    #    index=False,
    #    escape=True,
    #    caption="Konfiguration des verwendeten MLP-Modells",
    #    label="tab:mlp_config"
    #))

    # =========================
    # LaTeX-Tabelle: CV-Ergebnisse
    # =========================
    cv_df = pd.DataFrame({
        "Fold": [f"Fold {i+1}" for i in range(len(mae_scores))] + ["Mittelwert"],
        "MAE": list(mae_scores) + [mae_scores.mean()],
        "RMSE": list(rmse_scores) + [rmse_scores.mean()],
        "R²": list(r2_scores) + [r2_scores.mean()]
    })

    #print(cv_df.to_latex(
    #    index=False,
    #    float_format="%.4f",
    #    escape=False,
    #    caption="Ergebnisse der Time-Series-Cross-Validation des MLP-Modells",
    #    label="tab:mlp_cv_results"
    #))
