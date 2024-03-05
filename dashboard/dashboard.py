import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(page_title="Analisis Kualitas Udara di Aotizhongxin")

# Read data
df = pd.read_csv('./data/PRSA_Data_Aotizhongxin_20130301-20170228.csv')
st.title('Dashboard Analisis Kualitas Udara di Aotizhongxin')




st.write('Dashboard ini merupakan media untuk menyampaikan hasil analisis data kualitas udara di Aotizhongxin secara interaktif yang berfokus pada tingkat PM2.5 dan hubungannya dengan berbagai macam kondisi cuaca.')



st.markdown("""
- **Name**: Fatimah Fatma Syifa
- **Email**: fatmasyifa32@gmail.com
- **Dicoding ID**: fatmasyifa

Dashboard ini menunjukkan analisis data kualitas udara yang berfokus pada tingkat PM2.5 dari Aotizhongxin yang bertujuan untuk mengungkap kecenderungan, variasi per musim, dan kualitas udara yang diakibatkan perbedaan kondisi cuaca. Analisis ini berguna untuk studi lingkungan dan memantau kesehatan masyarakat.
""")

# Time series analysis
data_imputed = df.fillna(method='ffill')
data_imputed['date'] = pd.to_datetime(data_imputed[['year', 'month', 'day', 'hour']])
data_time_series = data_imputed[['date', 'PM2.5', 'NO2']].set_index('date').resample('M').mean()

# Plot Monthly Average Concentrations of PM2.5 and NO2
plt.figure(figsize=(15, 6))
plt.plot(data_time_series.index, data_time_series['PM2.5'], label='PM2.5', color='blue')
plt.plot(data_time_series.index, data_time_series['NO2'], label='NO2', color='green')
plt.title('Monthly Average Concentrations of PM2.5 and NO2')
plt.xlabel('Date')
plt.ylabel('Concentration')
plt.legend()
st.pyplot()

# Plot Seasonal Trends
plt.figure(figsize=(10, 6))
seasonal_trends = data_imputed.groupby('month')['PM2.5'].mean()
seasonal_trends.plot(kind='bar', color='skyblue')
plt.title('Average PM2.5 Levels by Month')
plt.xlabel('Month')
plt.ylabel('Average PM2.5')
plt.xticks(ticks=range(0, 12), labels=[str(m) for m in range(1, 13)], rotation=0)
st.pyplot()
