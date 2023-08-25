import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go

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

# Table with selected data
st.subheader('Cryptocurrency Prices by Market Cap')

# Calculate percentage changes for 1h and 24h
filtered_data['1h (%)'] = (filtered_data['High'] - filtered_data['Low']) / filtered_data['Low'] * 100
filtered_data['24h (%)'] = (filtered_data['Close'] - filtered_data['Open']) / filtered_data['Open'] * 100

# Format values in million (M) and billion (B) USD
def format_value(value):
    if value >= 1e9:
        return f'{value/1e9:.2f}B USD'
    elif value >= 1e6:
        return f'{value/1e6:.2f}M USD'
    else:
        return f'{value:.2f} USD'

# Round off volume and market cap values
table_data = filtered_data.head(10)[['Name', 'Close', '1h (%)', '24h (%)', 'Volume', 'Marketcap']]
table_data['Volume'] = table_data['Volume'].apply(lambda x: format_value(round(x, 2)))
table_data['Marketcap'] = table_data['Marketcap'].apply(format_value)

st.table(table_data)



# Calculate 7-day percentage change
filtered_data['7d (%)'] = (filtered_data['Close'] - filtered_data['Open'].shift(7)) / filtered_data['Open'].shift(7) * 100

# Create a line chart for 7-day percentage change
fig = px.line(filtered_data, x='Date', y='7d (%)', title='7-Day Percentage Change')

# Custom line and marker styling
fig.update_traces(
    line=dict(width=2, color='royalblue'),
    marker=dict(size=8, color='royalblue', line=dict(width=2, color='white'))
)

# Customize the layout
fig.update_layout(
    xaxis_title='Date',
    yaxis_title='7-Day Percentage Change (%)',
    title_x=0.5,
    height=500,
    margin=dict(l=50, r=50, t=50, b=50),
    plot_bgcolor='rgba(0,0,0,0)',  # Transparent plot background
    paper_bgcolor='rgba(0,0,0,0.05)',  # Light gray paper background
    font=dict(family='Arial', size=12, color='black')
)

# Remove gridlines
fig.update_xaxes(showgrid=False)
fig.update_yaxes(showgrid=False)

# Display the Plotly figure using Streamlit
st.subheader('7-Day Percentage Change')
st.plotly_chart(fig)


# Volume Trends
st.subheader('Volume Trends')
st.markdown("Chart showing the volume trends over time.")

# Create Candlestick Chart for Volume Trends
fig = go.Figure(data=[go.Candlestick(x=filtered_data['Date'],
                open=filtered_data['Open'],
                high=filtered_data['High'],
                low=filtered_data['Low'],
                close=filtered_data['Close'])])

fig.update_layout(
    title_text='Volume Trends',
    yaxis_title='Prices in USD',
    xaxis_title='Date',
    showlegend=False
)

st.plotly_chart(fig)

import plotly.graph_objects as go

# Market Capitalization Trends
st.subheader('Market Capitalization Trends Over Time')
st.markdown("This chart displays the historical trends in market capitalization for the selected cryptocurrency. Market capitalization represents the total value of all coins in circulation and is an important metric for assessing the overall size and performance of a cryptocurrency.")

fig = px.line(filtered_data, x='Date', y='Marketcap', title='Market Capitalization Trends',
              labels={'Marketcap': 'Market Capitalization (USD)', 'Date': 'Date'})

fig.update_layout(
    yaxis_title='Market Capitalization (USD)',
    xaxis=dict(showline=True, showgrid=False),
    yaxis=dict(showline=True, showgrid=True, gridcolor='lightgrey'),
    showlegend=False
)

st.plotly_chart(fig)

# Historical Performance
st.subheader('Historical Market Trends')
st.markdown("Chart showing the historical performance trends over time.")

# Create a figure using Plotly Express
fig = px.area(filtered_data, x='Date', y=['Open', 'High', 'Low', 'Close'],
              labels={'variable': 'Price Type', 'value': 'Price (USD)', 'Date': 'Date'},
              title='Historical Market Trends',
              color_discrete_map={'Open': 'blue', 'High': 'green', 'Low': 'red', 'Close': 'purple'})

# Add customizations to the figure
fig.update_xaxes(title_text='Date')
fig.update_yaxes(title_text='Prices in USD')
fig.update_layout(legend_title_text='Price Type')

# Display the Plotly figure using Streamlit
st.plotly_chart(fig)




# Price Changes
filtered_data['Price Change (%)'] = ((filtered_data['Close'] - filtered_data['Open']) / filtered_data['Open']) * 100

st.subheader('Price Changes (%)')
fig = px.bar(filtered_data, x='Date', y='Price Change (%)', title='Price Change (%) in USD', color='Price Change (%)', color_continuous_scale='RdBu')

fig.update_yaxes(title_text='Price Change (%) in USD')  # Add title to y-axis
fig.update_layout(showlegend=False)  # Remove legend

st.plotly_chart(fig)

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
fig = px.bar(
    grouped_data, 
    x=comparison_parameter, 
    y=grouped_data.index, 
    orientation='h',
    labels={comparison_parameter: f'{comparison_parameter} (USD)', 'index': 'Cryptocurrency'},
    title=f'Average {comparison_parameter} for All Cryptocurrencies',
    color=grouped_data.values,  # Add color to the bars
    color_continuous_scale='Inferno',  # Choose a color scale
    text=grouped_data.values.round(2),  # Display data values on the bars
)

# Customize the layout
fig.update_layout(
    xaxis_title=f'{comparison_parameter} (USD)',  # X-axis title
    yaxis_title='Cryptocurrency',  # Y-axis title
    showlegend=False,  # Remove legend
    plot_bgcolor='rgba(0, 0, 0, 0)',  # Transparent plot background
    paper_bgcolor='black',  # Dark background
    font=dict(color='white'),  # Font color
)

# Display the Plotly figure using Streamlit
st.plotly_chart(fig)



# Display Top 3 and Worst 3 Performers
top_performers = grouped_data.nlargest(3)
worst_performers = grouped_data.nsmallest(3)

st.subheader('Top 3 Performers')
top_performers_table = top_performers.reset_index()  # Reset index to include "Name" as a column
top_performers_table.index = range(1, len(top_performers_table) + 1)  # Set index as 1, 2, 3...
top_performers_table = top_performers_table.rename(columns={comparison_parameter: f'Historical Market Trends ({comparison_parameter})', 'index': 'S.No.'})
top_performers_table[f'Historical Market Trends ({comparison_parameter})'] = top_performers_table[f'Historical Market Trends ({comparison_parameter})'].apply(lambda x: f'{x/1e9:.3g}B USD' if x >= 1e9 else f'{x/1e6:.3g}M USD')
st.table(top_performers_table)

st.subheader('Worst 3 Performers')
worst_performers_table = worst_performers.reset_index()  # Reset index to include "Name" as a column
worst_performers_table.index = range(1, len(worst_performers_table) + 1)  # Set index as 1, 2, 3...
worst_performers_table = worst_performers_table.rename(columns={comparison_parameter: f'Historical Market Trends ({comparison_parameter})', 'index': 'S.No.'})
worst_performers_table[f'Historical Market Trends ({comparison_parameter})'] = worst_performers_table[f'Historical Market Trends ({comparison_parameter})'].apply(lambda x: f'{x/1e9:.3g}B USD' if x >= 1e9 else f'{x/1e6:.3g}M USD')
st.table(worst_performers_table)

