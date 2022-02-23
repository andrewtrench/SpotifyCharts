import pandas as pd

charts_df = pd.read_excel('spotify_sa_chart.xlsx', engine="openpyxl")
features_df = pd.read_excel('chart_features.xlsx', engine="openpyxl")

merged = pd.merge(charts_df, features_df, on='id', how='inner')
merged.to_excel('merged_data.xlsx', engine="openpyxl")