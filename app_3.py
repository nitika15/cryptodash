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

# Percent Change Time Frame Selector
time_frame = st.sidebar.selectbox("Percent Change Time Frame", ["1 month", "7 days", "24 hours"])

# Convert start_date and end_date to Timestamp objects
start_date = pd.Timestamp(start_date)
end_date = pd.Timestamp(end_date)

# Filter data based on selected time frame
if time_frame == "1 month":
    filtered_data = data[(data['Name'] == selected_crypto) & (data['Date'] >= start_date - pd.DateOffset(months=1)) & (data['Date'] <= end_date)]
elif time_frame == "7 days":
    filtered_data = data[(data['Name'] == selected_crypto) & (data['Date'] >= start_date - pd.DateOffset(days=7)) & (data['Date'] <= end_date)]
elif time_frame == "24 hours":
    filtered_data = data[(data['Name'] == selected_crypto) & (data['Date'] >= start_date - pd.DateOffset(hours=24)) & (data['Date'] <= end_date)]

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


# Top 3 Performers
st.subheader('Top 3 Performers')
top_performers = filtered_data.groupby('Name')['Price Change (%)'].sum().nlargest(3)
for performer, percentage in top_performers.items():
    st.write(f"{performer}: {percentage:.2f}%")

# Worst 3 Performers
st.subheader('Worst 3 Performers')
worst_performers = filtered_data.groupby('Name')['Price Change (%)'].sum().nsmallest(3)
for performer, percentage in worst_performers.items():
    st.write(f"{performer}: {percentage:.2f}%")



# Footer
st.write('Data Source: your_data_source_here')

if __name__ == '__main__':
    st.write("Dashboard created by Nitika Chauhan")  # Optional



