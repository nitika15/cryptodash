#!/usr/bin/env python
# coding: utf-8

# In[1]:


import streamlit as st
import pandas as pd
import numpy as np

# Load Data
@st.cache
def load_data():
    data = pd.read_csv('data.csv', parse_dates=['Date'])
    return data

data = load_data()

# Sidebar with crypto selector
crypto_list = data['Name'].unique()
selected_crypto = st.sidebar.selectbox('Select Cryptocurrency', crypto_list)

filtered_data = data[data['Name'] == selected_crypto]

# Title
st.title(f'{selected_crypto} Metrics Dashboard')
st.markdown("Explore the key metrics and trends of different cryptocurrencies.")

# Volume Trends
st.subheader('Volume Trends')
st.line_chart(filtered_data.set_index('Date')['Volume'])
st.markdown("The volume trends chart showcases the trading volume over time. It provides insights into periods of high activity and potential market interest.")

# Market Capitalization Trends
st.subheader('Market Capitalization Trends')
st.line_chart(filtered_data.set_index('Date')['Marketcap'])
st.markdown("The market capitalization trends chart displays the total market value of the selected cryptocurrency. It reflects the overall market sentiment and growth.")

# Historical Performance
st.subheader('Historical High vs Low Prices')
st.line_chart(filtered_data.set_index('Date')[['High', 'Low']])
st.markdown("The historical high vs low prices chart visualizes the trading range of the cryptocurrency. It helps to understand price volatility and potential support/resistance levels.")

# Price Changes
filtered_data['Price Change (%)'] = ((filtered_data['Close'] - filtered_data['Open']) / filtered_data['Open']) * 100
st.subheader('Price Changes (%)')
st.line_chart(filtered_data.set_index('Date')['Price Change (%)'])
st.markdown("The price changes chart depicts the percentage change between the opening and closing prices. It reveals intraday price movements and trends.")

# Extreme Price Movements
st.subheader('Extreme Price Movements')
max_price_increase = filtered_data['Price Change (%)'].idxmax()
max_price_decrease = filtered_data['Price Change (%)'].idxmin()
st.write(f"Day with Largest Increase: {filtered_data.loc[max_price_increase, 'Date']} ({filtered_data.loc[max_price_increase, 'Price Change (%)']:.2f}%)")
st.write(f"Day with Largest Decrease: {filtered_data.loc[max_price_decrease, 'Date']} ({filtered_data.loc[max_price_decrease, 'Price Change (%)']:.2f}%)")

# Price Range Distribution
st.subheader('Price Range Distribution')
bins = [0, 50, 100, 500, 1000, 5000, 10000, 50000, 100000]
hist_values = pd.cut(filtered_data['Close'], bins=bins).value_counts()
st.bar_chart(hist_values)
st.markdown("The price range distribution chart groups closing prices into bins, providing insights into the distribution of price levels.")

# Moving Averages
st.subheader('Moving Averages')
window_sizes = [10, 20, 50]
for window in window_sizes:
    filtered_data[f'Moving Avg {window}'] = filtered_data['Close'].rolling(window=window).mean()
    st.line_chart(filtered_data.set_index('Date')[f'Moving Avg {window}'])
st.markdown("The moving averages charts display the trend by smoothing out price fluctuations over different time periods.")

# Correlation Analysis
st.subheader('Correlation Analysis')
correlation_matrix = filtered_data[['Open', 'High', 'Low', 'Close', 'Volume', 'Marketcap']].corr()
st.write(correlation_matrix)
st.markdown("The correlation analysis table shows how different metrics are correlated. A value closer to 1 indicates strong positive correlation, while a value closer to -1 indicates strong negative correlation.")

# Footer
st.write('Data Source: your_data_source_here')
st.markdown("Dashboard created by [Your Name]")


# In[ ]:




