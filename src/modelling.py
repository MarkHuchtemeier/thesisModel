import pandas as pd
import statsmodels.api as sm
import matplotlib.pyplot as plt
from scipy.stats import shapiro
from statsmodels.stats.diagnostic import linear_reset, het_breuschpagan
from statsmodels.stats.outliers_influence import variance_inflation_factor

# =========================
# 1. Daten einlesen
# =========================
df = pd.read_csv("src/dataProcessed/modelData.csv")
df["date"] = pd.to_datetime(df["date"])
df = df.sort_values("date")

# =========================
# 2. Zielvariable und Regressoren festlegen
# =========================
y = df["liquidity"]

#date,equity,derivatives,bonds,liquidity,real_estate,commodities,long_term_share,short_term_share,gdp_growth_qoq,inflation_qoq,term_spread


#X = df[[
#    "equity",
#    "bonds",
#    "short_term_share",
#    "gdp_growth_qoq",
#    "inflation_qoq",
#    "term_spread"
#]]

X = df[[
    "short_term_share",
    "gdp_growth_qoq",
    "inflation_qoq",
    #"term_spread"
]]

# =========================
# 3. Fehlende Werte entfernen
# =========================
data = pd.concat([y, X], axis=1).dropna()

y = data["liquidity"]
X = data[[
    "short_term_share",
    "gdp_growth_qoq",
    "inflation_qoq",
    #"term_spread"
]]

# Konstante für Intercept hinzufügen
X = sm.add_constant(X)

# =========================
# 4. Lineare Regression schätzen
# =========================
model = sm.OLS(y, X).fit()

# =========================
# 5. Ergebnisse ausgeben
# =========================
print(model.summary())

# =========================
# 6. Diagnostische Tests
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
# Breusch-Pagan-Test
# H0: Homoskedastizität
# -------------------------
bp_test = het_breuschpagan(residuals, model.model.exog)
bp_labels = ["LM-Statistik", "LM-p-Wert", "F-Statistik", "F-p-Wert"]

print("\n===== Breusch-Pagan-Test =====")
for name, value in zip(bp_labels, bp_test):
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

# =========================
# 7. Plots
# =========================

# -------------------------
# Residuenplot: Residuen gegen fitted values
# -------------------------
plt.figure(figsize=(7, 5))
plt.scatter(fitted, residuals)
plt.axhline(0, linestyle="--")
plt.title("Residuals vs Fitted")
plt.xlabel("Fitted values")
plt.ylabel("Residuals")
plt.tight_layout()
plt.show()

# -------------------------
# Verteilungsplot der Residuen: Histogramm
# -------------------------
plt.figure(figsize=(7, 5))
plt.hist(residuals, bins=10)
plt.title("Histogram of Residuals")
plt.xlabel("Residuals")
plt.ylabel("Frequency")
plt.tight_layout()
plt.show()

# -------------------------
# QQ-Plot der Residuen
# -------------------------
plt.figure(figsize=(7, 5))
sm.qqplot(residuals, line="45", fit=True)
plt.title("Q-Q Plot of Residuals")
plt.tight_layout()
plt.show()