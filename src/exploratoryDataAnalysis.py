import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import seaborn as sns

def exploratory_analysis():
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
    axes = df[numeric_cols].hist(figsize=(14, 10), bins=15)

    # Durch alle Subplots gehen
    for ax in axes.flatten():
        if ax.get_title() == "gdp":
            ax.xaxis.set_major_formatter(
                ticker.FuncFormatter(lambda x, pos: f'{x/1000:.0f}k')
            )

    plt.tight_layout()
    plt.show()

    # =========================
    # Korrelationsmatrix
    # =========================
    corr_matrix = df[numeric_cols].corr()

    fig, ax = plt.subplots(figsize=(16, 12))

    sns.heatmap(
        corr_matrix,
        annot=True,
        fmt=".2f",
        cmap="coolwarm",
        square=True,
        linewidths=0.5,
        ax=ax
    )

    # Labels lesbarer machen
    plt.xticks(rotation=45, ha="right", fontsize=10)
    plt.yticks(rotation=0, fontsize=10)

    # Mehr Platz unten und oben
    plt.subplots_adjust(bottom=0.25, top=0.92)


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

    # Übersicht Inhalt Variablen
    # Datum ausschließen
    cols = [col for col in df.columns if col != "date"]

    desc = df[cols].describe()

    # Nur relevante Kennzahlen
    desc = desc.loc[["min", "25%", "50%", "mean", "75%", "max"]]
    desc.index = ["Min.", "1st Qu.", "Median", "Mean", "3rd Qu.", "Max."]

    # Runden
    desc = desc.round(2)

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

    # Korrelationsmatrix als LaTeX
    corr_latex = corr_matrix.round(2).to_latex(
        caption="Korrelationsmatrix der numerischen Variablen",
        label="tab:correlation_matrix",
        float_format="%.2f"
    )

    print(summary_table)
    #print(latex_table)
    #print(corr_latex)