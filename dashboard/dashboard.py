STREAMLIT FIX

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from statsmodels.tsa.seasonal import seasonal_decompose
import numpy as np


st.set_page_config(page_title="Analisis Kualitas Udara di Aotizhongxin")


file_path = 'https://raw.githubusercontent.com/fatmasyifa/myproject/main/PRSA_Data_Aotizhongxin_20130301-20170228.csv'
data = pd.read_csv(file_path)


st.title('Dashboard Analisis Kualitas Udara di Aotizhongxin')




st.write('Dashboard ini merupakan media untuk menyampaikan hasil analisis data kualitas udara di Aotizhongxin secara interaktif yang berfokus pada tingkat PM2.5 dan hubungannya dengan berbagai macam kondisi cuaca.')



st.markdown("""
- **Name**: Fatimah Fatma Syifa
- **Email**: fatmasyifa32@gmail.com
- **Dicoding ID**: fatmasyifa

Dashboard ini menunjukkan analisis data kualitas udara yang berfokus pada tingkat PM2.5 dari Aotizhongxin yang bertujuan untuk mengungkap kecenderungan, variasi per musim, dan kualitas udara yang diakibatkan perbedaan kondisi cuaca. Analisis ini berguna untuk studi lingkungan dan memantau kesehatan masyarakat.
""")


st.sidebar.header('User Input Features')


selected_year = st.sidebar.selectbox('Pilih Tahun', list(data['year'].unique()))
selected_month = st.sidebar.selectbox('Pilih Bulan', list(data['month'].unique()))


data_filtered = data[(data['year'] == selected_year) & (data['month'] == selected_month)].copy()


st.subheader('Data berdasarkan periode yang dipilih')
st.write(data_filtered.describe())


st.subheader('Tingkat PM2.5 (harian)')
fig, ax = plt.subplots()
ax.plot(data_filtered['day'], data_filtered['PM2.5'])
plt.xlabel('Hari dalam bulan')
plt.ylabel('Konsentrasi PM2.5')
st.pyplot(fig)


st.subheader('Korelasi Heatmap dari indikator kualitas udara')
corr = data_filtered[['PM2.5', 'NO2', 'SO2', 'CO', 'O3', 'TEMP', 'PRES', 'DEWP']].corr()
fig, ax = plt.subplots()
sns.heatmap(corr, annot=True, ax=ax)
plt.title('Korelasi Heatmap')
st.pyplot(fig)


st.subheader('Analisis Kecenderungan Per Musim')
seasonal_trends = data.groupby('month')['PM2.5'].mean()
fig, ax = plt.subplots()
seasonal_trends.plot(kind='bar', color='skyblue', ax=ax)
plt.title('Tingkat rata-rata bulanan PM2.5')
plt.xlabel('Bulan')
plt.ylabel('Rata-rata PM2.5')
st.pyplot(fig)



st.subheader('Tingkat 2.5 (harian)')
fig, ax = plt.subplots()
ax.plot(data_filtered['day'], data_filtered['PM2.5'])
plt.xlabel('Hari dalam bulan')
plt.ylabel('Konsentrasi PM2.5')
st.pyplot(fig)


st.subheader('Distribusi Polutan')
selected_pollutant = st.selectbox('Pilih Polutan', ['PM2.5', 'PM10', 'SO2', 'NO2', 'CO'])
fig, ax = plt.subplots()
sns.boxplot(x='month', y=selected_pollutant, data=data[data['year'] == selected_year], ax=ax)
st.pyplot(fig)


st.subheader('Dekomposisi Rangkaian Waktu PM2.5')
try:
    data_filtered['PM2.5'].ffill(inplace=True)
    decomposed = seasonal_decompose(data_filtered['PM2.5'], model='aditif', period=24) # Adjust period as necessary
    fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(10, 8))
    decomposed.trend.plot(ax=ax1, title='Kecenderungan')
    decomposed.seasonal.plot(ax=ax2, title='Musim')
    decomposed.resid.plot(ax=ax3, title='Residu')
    plt.tight_layout()
    st.pyplot(fig)
except ValueError as e:
    st.error("Tidak dapat menunjukkan dekomposisi rangkaian waktu: " + str(e))



st.subheader('Rata-rata Tingkat PM2.5 (jam)')
try:
    
    data['hour'] = data['hour'].astype(int)
    data['PM2.5'] = pd.to_numeric(data['PM2.5'], errors='coerce')
    data['PM2.5'].ffill(inplace=True)

    
    hourly_avg = data.groupby('hour')['PM2.5'].mean()

    
    fig, ax = plt.subplots()
    sns.heatmap([hourly_avg.values], ax=ax, cmap='coolwarm')
    plt.title('Rata-rata Tingkat PM2.5 (jam)')
    st.pyplot(fig)
except Exception as e:
    st.error(f"Error: {e}")


st.subheader('Analisis Arah Angin')
wind_data = data_filtered.groupby('wd')['PM2.5'].mean()
fig = plt.figure(figsize=(8, 6))
ax = fig.add_subplot(111, polar=True)
theta = np.linspace(0, 2 * np.pi, len(wind_data))
bars = ax.bar(theta, wind_data.values, align='center', alpha=0.5)
plt.title('Tingkat PM2.5 Berdasarkan Arah Angin')
st.pyplot(fig)



st.subheader('Curah Hujan vs Tingkat PM2.5')
fig, ax = plt.subplots()
sns.scatterplot(x='RAIN', y='PM2.5', data=data_filtered, ax=ax)
plt.title('Curah Hujan vs Tingkat PM2.5')
st.pyplot(fig)


st.subheader('Korelasi Heatmap Interaktif')
selected_columns = st.multiselect('Pilih kolom untuk menentukan korelasi', data.columns, default=['PM2.5', 'NO2', 'TEMP', 'PRES', 'DEWP'])
corr = data[selected_columns].corr()
fig, ax = plt.subplots()
sns.heatmap(corr, annot=True, ax=ax)
st.pyplot(fig)




st.subheader('Kesimpulan')
st.write("""
- Dashboard memberikan analisis data kualitas udara yang lebih detail dan interaktif.
- Berbagai visualisasi memberikan wawasan tentang tingkat PM2.5, distribusi tingkat PM2.5, dan faktor-faktor yang mempengaruhinya.
- Kecenderungan per musim dan pengaruh berbagai kondisi cuaca dan polutan terhadap kualitas udara digambarkan dengan jelas.
- User dapat menjelajahi data secara dinamis untuk mendapatkan pemahaman lebih mendalam tentang tren kualitas udara.
""")
