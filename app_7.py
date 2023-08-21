import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Load Data
@st.cache_data
def load_data():
    data = pd.read_csv('data.csv', parse_dates=['Date'])
    return data

data = load_data()

# Custom formatting function for y-axis labels
def format_y_labels(x, pos):
    if x >= 1e9:
        return f'{x/1e9:.3g}B'  # Format in billions
    elif x >= 1e6:
        return f'{x/1e6:.3g}M'  # Format in millions
    else:
        return f'{x:.3g}'

# Main Heading
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@700&display=swap');
.big-title {
    font-family: 'Poppins', sans-serif;
    font-size: 32px;
    font-weight: 700;
    color: #333;
}
</style>
""", unsafe_allow_html=True)
st.title("Cryptocurrency Insights Dashboard")
st.markdown('<p style="font-size: 16px; ">Analyzing and visualizing cryptocurrency metrics.</p>', unsafe_allow_html=True)


# Sidebar with crypto selector
st.sidebar.markdown("## Cryptocurrency Metrics Dashboard")
crypto_list = data['Name'].unique()
selected_crypto = st.sidebar.selectbox('Select Cryptocurrency', crypto_list)

# Date Range Selector
st.sidebar.markdown("### Date Range")
start_date = st.sidebar.date_input("Start Date", data['Date'].min())
end_date = st.sidebar.date_input("End Date", data['Date'].max())

# Percent Change Time Frame Selector
st.sidebar.markdown("### Time Frame for Percent Change")
time_frame = st.sidebar.selectbox("Select Time Frame", ["1 month", "7 days", "24 hours"])

# Convert start_date and end_date to Timestamp objects
start_date = pd.Timestamp(start_date)
end_date = pd.Timestamp(end_date)

# Filter data based on selected time frame and cryptocurrency
if selected_crypto == 'All':
    if time_frame == "1 month":
        filtered_data = data[(data['Date'] >= start_date - pd.DateOffset(months=1)) & (data['Date'] <= end_date)]
    elif time_frame == "7 days":
        filtered_data = data[(data['Date'] >= start_date - pd.DateOffset(days=7)) & (data['Date'] <= end_date)]
    elif time_frame == "24 hours":
        filtered_data = data[(data['Date'] >= start_date - pd.DateOffset(hours=24)) & (data['Date'] <= end_date)]
else:
    if time_frame == "1 month":
        filtered_data = data[(data['Name'] == selected_crypto) & (data['Date'] >= start_date - pd.DateOffset(months=1)) & (data['Date'] <= end_date)]
    elif time_frame == "7 days":
        filtered_data = data[(data['Name'] == selected_crypto) & (data['Date'] >= start_date - pd.DateOffset(days=7)) & (data['Date'] <= end_date)]
    elif time_frame == "24 hours":
        filtered_data = data[(data['Name'] == selected_crypto) & (data['Date'] >= start_date - pd.DateOffset(hours=24)) & (data['Date'] <= end_date)]


# Title


# Volume Trends
st.subheader('Volume Trends')
st.line_chart(filtered_data.set_index('Date')['Volume'])

# Market Capitalization Trends
st.subheader('Market Capitalization Trends')
st.line_chart(filtered_data.set_index('Date')['Marketcap'])

# Historical Performance
st.subheader('Historical Market Trends')
st.area_chart(filtered_data.set_index('Date')[['Open', 'High', 'Low', 'Close']])

# Price Changes
filtered_data['Price Change (%)'] = ((filtered_data['Close'] - filtered_data['Open']) / filtered_data['Open']) * 100
st.subheader('Price Changes (%)')
st.bar_chart(filtered_data.set_index('Date')['Price Change (%)'])

# Extreme Price Movements
st.subheader('Extreme Price Movements')
max_price_increase = filtered_data['Price Change (%)'].idxmax()
max_price_decrease = filtered_data['Price Change (%)'].idxmin()
st.write(f"Day with Largest Increase: {filtered_data.loc[max_price_increase, 'Date']} ({filtered_data.loc[max_price_increase, 'Price Change (%)']:.2f}%)")
st.write(f"Day with Largest Decrease: {filtered_data.loc[max_price_decrease, 'Date']} ({filtered_data.loc[max_price_decrease, 'Price Change (%)']:.2f}%)")

# Compare Performance of All Cryptocurrencies
st.subheader('Compare Performance of All Cryptocurrencies')

# Initialize comparison_parameter
comparison_parameter = st.selectbox("Select Parameter to Compare", ["Volume", "Marketcap", "High", "Low"])


# Group data by cryptocurrency and calculate the mean for the selected parameter
grouped_data = data.groupby('Name')[comparison_parameter].mean().sort_values()

# Create a bar chart to visualize the performance
plt.figure(figsize=(10, 6))
bar_chart = plt.barh(grouped_data.index, grouped_data.values, color='skyblue')
plt.xlabel(comparison_parameter)
plt.ylabel('Cryptocurrency')
plt.title(f'Average {comparison_parameter} for All Cryptocurrencies')
plt.gca().xaxis.set_major_formatter(plt.FuncFormatter(format_y_labels))
st.pyplot(plt)
st.markdown(f'### Average {comparison_parameter} for All Cryptocurrencies')


# Display Top 3 and Worst 3 Performers
top_performers = grouped_data.nlargest(3)
worst_performers = grouped_data.nsmallest(3)

st.subheader('Top 3 Performers')
st.table(top_performers)

st.subheader('Worst 3 Performers')
st.table(worst_performers)



