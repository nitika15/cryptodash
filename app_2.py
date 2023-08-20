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

# Date Range Selector
start_date = st.sidebar.date_input("Start Date", data['Date'].min())
end_date = st.sidebar.date_input("End Date", data['Date'].max())

# Convert start_date and end_date to Timestamp objects
start_date = pd.Timestamp(start_date)
end_date = pd.Timestamp(end_date)

filtered_data = data[(data['Name'] == selected_crypto) & (data['Date'] >= start_date) & (data['Date'] <= end_date)]

# Title
st.title(f'{selected_crypto} Metrics Dashboard')

# Volume Trends
st.subheader('Volume Trends')
st.line_chart(filtered_data.set_index('Date')['Volume'])

# Market Capitalization Trends
st.subheader('Market Capitalization Trends')
st.line_chart(filtered_data.set_index('Date')['Marketcap'])

# Historical Performance
st.subheader('Historical High vs Low Prices')
st.line_chart(filtered_data.set_index('Date')[['High', 'Low']])

# Price Changes
filtered_data['Price Change (%)'] = ((filtered_data['Close'] - filtered_data['Open']) / filtered_data['Open']) * 100
st.subheader('Price Changes (%)')
st.line_chart(filtered_data.set_index('Date')['Price Change (%)'])

# Extreme Price Movements
st.subheader('Extreme Price Movements')
max_price_increase = filtered_data['Price Change (%)'].idxmax()
max_price_decrease = filtered_data['Price Change (%)'].idxmin()
st.write(f"Day with Largest Increase: {filtered_data.loc[max_price_increase, 'Date']} ({filtered_data.loc[max_price_increase, 'Price Change (%)']:.2f}%)")
st.write(f"Day with Largest Decrease: {filtered_data.loc[max_price_decrease, 'Date']} ({filtered_data.loc[max_price_decrease, 'Price Change (%)']:.2f}%)")

# Footer
st.write('Data Source: your_data_source_here')

if __name__ == '__main__':
    st.write("Dashboard created by [Your Name]")  # Optional
