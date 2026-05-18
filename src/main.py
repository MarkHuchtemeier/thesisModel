import pandas as pd
from processCustomerData import clean_customer_data
from processMarketData import clean_market_data
from dataTransformation import transform_data
from exploratoryDataAnalysis import exploratory_analysis
from modellingRegression import modelling_regression
from mlp import modelling_mlp

def main():
    filepath_full_baseline = "src/dataProcessed/modelData.csv"
    filepath_reduced_regression = "src/dataProcessed/modelData_lag1.csv"
    filepath_final_regression = "src/dataProcessed/modelData_lag2.csv"

    features_full_baseline = [
        "equity",
        "bonds",
        "short_term_share",
        "gdp_growth_qoq",
        "inflation_qoq",
        "term_spread"
    ]

    features_reduced_regression = [
    "short_term_share",
        "gdp_growth_qoq",
        "inflation_qoq",
        "term_spread"
    ]

    features_final_regression = [
    "short_term_share",
        "gdp_growth_qoq",
        "inflation_qoq"
    ]

    clean_customer_data()
    clean_market_data()
    transform_data()
    exploratory_analysis()
    modelling_regression(filepath_full_baseline, features_full_baseline)
    modelling_regression(filepath_reduced_regression, features_reduced_regression)
    modelling_regression(filepath_final_regression, features_final_regression)
    modelling_mlp()

if __name__ == "__main__":
    main()