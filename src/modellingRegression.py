import pandas as pd
import statsmodels.api as sm
import matplotlib.pyplot as plt
from scipy.stats import shapiro
from statsmodels.stats.diagnostic import linear_reset, het_white
from statsmodels.stats.outliers_influence import variance_inflation_factor

def modelling_regression(filepath_dataset, features):
    df = pd.read_csv(filepath_dataset)
    df["date"] = pd.to_datetime(df["date"])
    df = df.sort_values("date")

    # =========================
    # 1. Zielvariable und Regressoren festlegen
    # =========================
    X = df[features]
    y = df["liquidity"]   

    df = pd.concat([y, X], axis=1).dropna() 

    # Konstante für Intercept hinzufügen
    X = sm.add_constant(X)

    # =========================
    # 2. Lineare Regression schätzen
    # =========================
    model = sm.OLS(y, X).fit()

    # =========================
    # 3. Ergebnisse ausgeben
    # =========================
    print(model.summary())
    latex_table = model.summary().as_latex()
    #print(latex_table)

    # =========================
    # 4. Diagnostische Tests
    # =========================
    # Residuen und fitted values
    residuals = model.resid
    fitted = model.fittedvalues

    # -------------------------
    # RESET-Test
    # H0: Modell ist korrekt spezifiziert / keine vernachlässigte Nichtlinearität
    # -------------------------
    reset_test = linear_reset(model, power=2, use_f=True)
    print("\n===== RESET-Test =====")
    print(f"F-Statistik: {reset_test.fvalue:.4f}")
    print(f"p-Wert:      {reset_test.pvalue:.4f}")

    # -------------------------
    # White-Test
    # H0: Homoskedastizität
    # -------------------------
    white_test = het_white(residuals, model.model.exog)
    white_labels = ["LM-Statistik", "LM-p-Wert", "F-Statistik", "F-p-Wert"]

    print("\n===== White-Test =====")
    for name, value in zip(white_labels, white_test):
        print(f"{name}: {value:.4f}")

    # -------------------------
    # Shapiro-Wilk-Test
    # H0: Residuen sind normalverteilt
    # -------------------------
    shapiro_stat, shapiro_p = shapiro(residuals)

    print("\n===== Shapiro-Wilk-Test =====")
    print(f"W-Statistik: {shapiro_stat:.4f}")
    print(f"p-Wert:      {shapiro_p:.4f}")

    # -------------------------
    # VIF
    # -------------------------
    # X muss die Regressormatrix mit Konstante sein
    X_vif = X.copy()

    vif_data = pd.DataFrame()
    vif_data["Variable"] = X_vif.columns
    vif_data["VIF"] = [
        variance_inflation_factor(X_vif.values, i)
        for i in range(X_vif.shape[1])
    ]

    print("\n===== Variance Inflation Factor (VIF) =====")
    print(vif_data)

    latex_vif = vif_data.to_latex(index=False, float_format="%.4f")
    #print(latex_vif)

    # =========================
    # 5. Plots
    # =========================

    # -------------------------
    # Residuenplot: Residuen gegen fitted values
    # -------------------------
    plt.figure(figsize=(7, 5))
    plt.scatter(fitted, residuals)
    plt.axhline(0, linestyle="--")
    plt.xlabel("Fitted values")
    plt.ylabel("Residuals")
    plt.tight_layout()
    plt.show()

    # -------------------------
    # Verteilungsplot der Residuen: Histogramm
    # -------------------------
    plt.figure(figsize=(7, 5))
    plt.hist(residuals, bins=10)
    plt.xlabel("Residuals")
    plt.ylabel("Frequency")
    plt.tight_layout()
    plt.show()

    # -------------------------
    # QQ-Plot der Residuen
    # -------------------------
    plt.figure(figsize=(7, 5))
    sm.qqplot(residuals, line="45", fit=True)
    plt.tight_layout()
    plt.show()