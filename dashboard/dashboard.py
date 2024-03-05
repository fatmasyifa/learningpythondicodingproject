import streamlit as st
import numpy as np
import pandas as pd
import statsmodels.api as sm
from scipy.stats import f_oneway
import matplotlib.pyplot as plt
import seaborn as sns

# Read data
df = pd.read_csv('./data/PRSA_Data_Aotizhongxin_20130301-20170228.csv')

# Display initial assessment
st.title("Initial Assessment")
st.write("Head of the DataFrame:")
st.write(df.head())

# Missing data analysis
st.title("Missing Data Analysis")
missing_percentage = df.isnull().mean() * 100
cols_to_plot = ['PM2.5', 'PM10']
data_missing = df[cols_to_plot].isnull()
data_missing['year'] = df['year']
data_missing_2013 = data_missing[data_missing['year'] == 2013]
plt.figure(figsize=(20, 8))
sns.heatmap(data_missing_2013.drop('year', axis=1).T, cmap='viridis', cbar=False)
plt.title('Missing Data Pattern for 2013')
plt.xlabel('Date')
plt.ylabel('Pollutant')
plt.yticks(rotation=0)
st.set_option('deprecation.showPyplotGlobalUse', False)
st.pyplot()


st.write("Missing Percentage:")
st.write(missing_percentage)
st.write("Sum of Missing Data for 2013:")
st.write(data_missing_2013.sum())

# Data preprocessing
data_imputed = df.fillna(method='ffill')
duplicates = data_imputed.duplicated().sum()
constant_columns = data_imputed.columns[data_imputed.nunique() <= 1]
data_types = data_imputed.dtypes
st.write("Duplicates:", duplicates)
st.write("Constant Columns:", constant_columns)
st.write("Data Types:", data_types)

# Summary Statistics
st.title("Summary Statistics")
summary_statistics = data_imputed.describe()
st.write(summary_statistics)

# Time series analysis
st.title("Time Series Analysis")
data_imputed['date'] = pd.to_datetime(data_imputed[['year', 'month', 'day', 'hour']])
data_time_series = data_imputed[['date', 'PM2.5', 'NO2']].set_index('date').resample('M').mean()
plt.figure(figsize=(15, 6))
plt.plot(data_time_series.index, data_time_series['PM2.5'], label='PM2.5', color='blue')
plt.plot(data_time_series.index, data_time_series['NO2'], label='NO2', color='green')
plt.title('Monthly Average Concentrations of PM2.5 and NO2')
plt.xlabel('Date')
plt.ylabel('Concentration')
plt.legend()
st.pyplot()

# Correlation Matrix
st.title("Correlation Matrix")
correlation_matrix = data_imputed[['PM2.5', 'PM10', 'SO2', 'NO2', 'CO', 'O3', 'TEMP', 'PRES', 'DEWP', 'RAIN', 'WSPM']].corr()
st.write(correlation_matrix)

# ANOVA Test
groups = data_imputed.groupby('year')['PM2.5']
anova_test_data = [group[1] for group in groups]
anova_test_result = f_oneway(*anova_test_data)
st.write("ANOVA Test Result:", anova_test_result)

# Seasonal Trends
seasonal_trends = data_imputed.groupby('month')['PM2.5'].mean()
st.write("Seasonal Trends:", seasonal_trends)

# Weather Correlations
weather_correlations = df[['TEMP', 'PRES', 'DEWP', 'RAIN', 'PM2.5']].corr()['PM2.5']
st.write("Correlations with Weather Conditions:", weather_correlations)

# Plot Seasonal Trends
plt.figure(figsize=(10, 6))
seasonal_trends.plot(kind='bar', color='skyblue')
plt.title('Average PM2.5 Levels by Month')
plt.xlabel('Month')
plt.ylabel('Average PM2.5')
plt.xticks(ticks=range(0, 12), labels=[str(m) for m in range(1, 13)], rotation=0)
st.pyplot()
