import streamlit as st
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

# Missing data analysis
st.title("Missing Data Analysis")
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
st.pyplot()
st.markdown("""
Terdapat persentase data yang hilang untuk polutan relatif kecil, dengan PM2.5 yang hilang sekitar 2,63%, dan PM10 yang hilang sekitar 2,05%. Variabel polutan dan cuaca lainnya juga memiliki persentase data yang hilang dalam jumlah kecil, sehingga menunjukkan bahwa kumpulan data tersebut relatif lengkap. Heatmap tahun 2013 menunjukkan bahwa data yang hilang untuk PM2.5 dan PM10 tidak mengikuti pola yang jelas, sehingga menunjukkan bahwa hilangnya data tersebut mungkin terjadi secara acak atau tidak sistematis. Tidak ada data yang hilang dalam jangka panjang, yang merupakan pertanda baik untuk analisis deret waktu.
""")
# Time series analysis
st.title("Time Series Analysis")
data_imputed = df.fillna(method='ffill')
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

# Plot Seasonal Trends
plt.figure(figsize=(10, 6))
seasonal_trends = data_imputed.groupby('month')['PM2.5'].mean()
seasonal_trends.plot(kind='bar', color='skyblue')
plt.title('Average PM2.5 Levels by Month')
plt.xlabel('Month')
plt.ylabel('Average PM2.5')
plt.xticks(ticks=range(0, 12), labels=[str(m) for m in range(1, 13)], rotation=0)
st.pyplot()

# Summary Statistics
st.title("Summary Statistics")
summary_statistics = data_imputed.describe()
st.write(summary_statistics)

# Correlation Matrix
st.title("Correlation Matrix")
correlation_matrix = data_imputed[['PM2.5', 'PM10', 'SO2', 'NO2', 'CO', 'O3', 'TEMP', 'PRES', 'DEWP', 'RAIN', 'WSPM']].corr()
st.write(correlation_matrix)
