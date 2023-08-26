import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go



st.set_page_config(layout="wide")
st.set_theme('dark')


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
    font-size: 20px;
    font-weight: 500;
    color: #333;
}
</style>
""", unsafe_allow_html=True)
st.markdown('<h1 style="font-size: 38px;">Cryptocurrency 101: A Beginner\'s Investment Guide</h1>', unsafe_allow_html=True)

st.markdown('<p style="font-size: 18px; ">This app is designed to help beginners learn about cryptocurrency investing. You can explore different metrics and trends to make informed investment decisions.</p>', unsafe_allow_html=True)

# Cryptocurrency Glossary Section
with st.expander("Cryptocurrency Glossary"):
    st.markdown("Learn key terms in the world of cryptocurrency investing:")
    crypto_glossary = {
        'Cryptocurrency': '_A digital or virtual form of currency that uses cryptography for secure transactions._',
        'Blockchain': '_A distributed and decentralized digital ledger that records transactions across multiple computers._',
        'Wallet': '_A digital tool for storing, sending, and receiving cryptocurrencies._',
        'Mining': '_The process of validating transactions and adding them to the blockchain, often requiring powerful hardware._',
        'Token': '_A digital asset issued on a blockchain, representing ownership of a particular asset or utility._',
        'Fiat Currency': '_Government-issued currency that is not backed by a physical commodity like gold._',
        'Decentralization': '_The distribution of control and decision-making across a network of participants._',
        'Smart Contract': '_Self-executing contracts with the terms of the agreement directly written into code._',
        'ICO': '_Initial Coin Offering - A fundraising method where new cryptocurrencies are sold to investors._',
        'HODL': '_A misspelled term for holding onto cryptocurrencies instead of selling them._',
        'Exchange': '_A platform for trading and exchanging cryptocurrencies._',
        'Market Cap': '_The total value of a cryptocurrency in circulation._',
        'Whale': '_An individual or entity that holds a large amount of cryptocurrency._',
        'Altcoin': '_Any cryptocurrency other than Bitcoin._',
        'Satoshi': '_The smallest unit of a Bitcoin._',
        'Private Key': '_A secret code that grants access to a cryptocurrency wallet._',
        'Public Key': '_An address used to receive cryptocurrency, derived from the private key._',
        'DApp': '_Decentralized Application - An application running on a blockchain network._',

        'ATH': '_All-Time High - The highest price ever reached by a cryptocurrency._',
        # Add more terms and definitions here
    }

    for term, definition in crypto_glossary.items():
        st.markdown(f"- _*{term}:*_ {definition}")

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

# Additional Educational Resources Section
st.sidebar.markdown("## Educational Resources")
st.sidebar.markdown("Learn more about cryptocurrency investing:")
st.sidebar.markdown("- [Cryptocurrency Basics](https://www.investopedia.com/terms/c/cryptocurrency.asp)")
st.sidebar.markdown("- [How to Buy Cryptocurrency](https://www.wikihow.com/Buy-Cryptocurrency)")
st.sidebar.markdown("- [Crypto Investment Strategies](https://www.coindesk.com/price/bitcoin)")

st.sidebar.markdown("- [Technical Analysis Guide](https://www.investopedia.com/terms/t/technicalanalysis.asp)")
st.sidebar.markdown("- [Crypto News and Trends](https://cointelegraph.com/)")

st.sidebar.markdown("- [Cryptocurrency Exchanges](https://www.investopedia.com/best-crypto-exchanges-5071855)")  # New link


st.sidebar.markdown("- [Introduction to Stablecoins](https://www.investopedia.com/terms/s/stablecoin.asp)")  # New link










# Table with selected data
st.subheader('Cryptocurrency Prices Data')

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
with st.expander("What is 7-Day Percentage Change?"):
    st.markdown("- _7-day percentage change measures the price change of a cryptocurrency over a 7-day period._")
    st.markdown("- _Positive percentage change indicates price appreciation, while negative percentage change indicates depreciation._")
    st.markdown("- _This metric helps traders and investors assess short-term price movements and volatility._")
    st.markdown("- _Understanding 7-day percentage change can aid in identifying short-term trends and potential trading opportunities._")

st.plotly_chart(fig)

# Volume Trends
st.subheader('Volume Trends')

with st.expander("What is Volume Trends?"):
    st.markdown("- _Volume trends refer to the amount of trading activity in a cryptocurrency._")
    st.markdown("- _High trading volume indicates a high level of interest and liquidity in the market._")
    st.markdown("- _Low trading volume can lead to higher price volatility and less reliable trends._")
    st.markdown("- _Understanding volume trends helps investors make informed decisions and predict market movements._")

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
with st.expander("What is Market Trends?"):
   st.markdown("- _Market trends show the historical performance of a cryptocurrency over time._")
   st.markdown("- _They include key metrics such as open, high, low, and close prices._")
   st.markdown("- _Analyzing market trends helps investors identify patterns and make predictions about future price movements._")
   st.markdown("- _Traders use various technical analysis tools to interpret market trends and make trading decisions._")


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
st.subheader('Historical Performance')
with st.expander("What is Historical Performance?"):
     st.markdown("- _Historical performance refers to the past price movements of a cryptocurrency._")
     st.markdown("- _It includes data points such as open, high, low, and close prices for specific time periods._")
     st.markdown("- _Analyzing historical performance helps investors identify trends, patterns, and cycles._")
     st.markdown("- _Traders use historical performance data to develop trading strategies and make informed decisions._")


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

st.subheader('Price Changes (%)')
with st.expander("What is Price Change?"):
     st.markdown("- _Price change refers to the percentage change in the price of a cryptocurrency over a specific period._")
     st.markdown("- _Positive price change indicates price appreciation, while negative price change indicates depreciation._")
     st.markdown("- _Price change is an important metric for short-term traders and investors looking to capitalize on price movements._")
     st.markdown("- _Understanding price change patterns can help investors time their entries and exits for optimal gains._")

filtered_data['Price Change (%)'] = ((filtered_data['Close'] - filtered_data['Open']) / filtered_data['Open']) * 100

fig = px.bar(filtered_data, x='Date', y='Price Change (%)', title='Price Change (%) in USD', color='Price Change (%)', color_continuous_scale='RdBu')

fig.update_yaxes(title_text='Price Change (%) in USD')  # Add title to y-axis
fig.update_layout(showlegend=False)  # Remove legend

st.plotly_chart(fig)

# Extreme Price Movements
st.subheader('Extreme Price Movements')
with st.expander("What is Extreme Price Movements?"):
   
    st.markdown("- _Extreme price movements refer to unusually large changes in cryptocurrency prices._")
    st.markdown("- _These movements can include significant price increases or decreases within a short period._")
    st.markdown("- _Extreme price movements can be caused by various factors, such as news events, market sentiment, or trading activities._")
    st.markdown("- _Traders and investors often monitor extreme price movements to gauge market dynamics and potential opportunities._")
    st.markdown("- _It's important to note that extreme price movements can carry higher risks due to increased volatility._")

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



