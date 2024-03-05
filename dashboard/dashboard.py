

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np


st.set_page_config(page_title="Analisis Kualitas Udara di Aotizhongxin")


data = pd.read_csv('./data/PRSA_Data_Aotizhongxin_20130301-20170228.csv')


st.title('Dashboard Analisis Kualitas Udara di Aotizhongxin')




st.write('Dashboard ini merupakan media untuk menyampaikan hasil analisis data kualitas udara di Aotizhongxin secara interaktif yang berfokus pada tingkat PM2.5 dan hubungannya dengan berbagai macam kondisi cuaca.')



st.markdown("""
- **Name**: Fatimah Fatma Syifa
- **Email**: fatmasyifa32@gmail.com
- **Dicoding ID**: fatmasyifa


""")
#Missing data

# Create a Streamlit app
st.title('Missing Data Analysis')

# Assuming df is your DataFrame

# Calculate missing percentage
missing_percentage = df.isnull().mean() * 100

# Specify columns to plot
cols_to_plot = ['PM2.5', 'PM10']

# Create a DataFrame for missing data
data_missing = df[cols_to_plot].isnull()
data_missing['year'] = df['year']

# Filter data for the year 2013
data_missing_2013 = data_missing[data_missing['year'] == 2013]

# Plot missing data pattern for 2013
plt.figure(figsize=(20, 8))
sns.heatmap(data_missing_2013.drop('year', axis=1).T, cmap='viridis', cbar=False)
plt.title('Missing Data Pattern for 2013')
plt.xlabel('Date')
plt.ylabel('Pollutant')
plt.yticks(rotation=0)

# Show the plot in the Streamlit app
st.pyplot()

# Display missing percentage and sum of missing data for 2013
st.write("Missing Percentage:")
st.write(missing_percentage)
st.write("Sum of Missing Data for 2013:")
st.write(data_missing_2013.sum())

#Monthly Average Concentrations of PM2.5 and NO2

# Create a Streamlit app
st.title('Monthly Average Concentrations of PM2.5 and NO2')

# Load your data (data_imputed) assuming it's already loaded and preprocessed
# Assuming data_imputed is your DataFrame containing 'year', 'month', 'day', 'hour', 'PM2.5', and 'NO2'

# Preprocess data
data_imputed['date'] = pd.to_datetime(data_imputed[['year', 'month', 'day', 'hour']])
data_time_series = data_imputed[['date', 'PM2.5', 'NO2']].set_index('date').resample('M').mean()

# Plot the data
fig, ax = plt.subplots(figsize=(15, 6))
ax.plot(data_time_series.index, data_time_series['PM2.5'], label='PM2.5', color='blue')
ax.plot(data_time_series.index, data_time_series['NO2'], label='NO2', color='green')
ax.set_title('Monthly Average Concentrations of PM2.5 and NO2')
ax.set_xlabel('Date')
ax.set_ylabel('Concentration')
ax.legend()

# Show the plot in the Streamlit app
st.pyplot(fig)


#Correlation matrix
# Assuming data_imputed is your DataFrame containing the required columns

# Create a Streamlit app
st.title('Correlation Matrix')

# Calculate correlation matrix
correlation_matrix = data_imputed[['PM2.5', 'PM10', 'SO2', 'NO2', 'CO', 'O3', 'TEMP', 'PRES', 'DEWP', 'RAIN', 'WSPM']].corr()

# Display correlation matrix
st.write(correlation_matrix)

#One way Anava
st.subheader('Analisis Kecenderungan Per Musim')
seasonal_trends = data.groupby('month')['PM2.5'].mean()
fig, ax = plt.subplots()
seasonal_trends.plot(kind='bar', color='skyblue', ax=ax)
plt.title('Tingkat rata-rata bulanan PM2.5')
plt.xlabel('Bulan')
plt.ylabel('Rata-rata PM2.5')
st.pyplot(fig)

