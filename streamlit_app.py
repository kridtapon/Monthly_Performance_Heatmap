import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import yfinance as yf

# Set the Streamlit page configuration
st.set_page_config(
    page_title="Bitcoin Monthly Returns Heatmap",
    layout="centered",
    initial_sidebar_state="expanded",
)

# Title of the application
st.title("Bitcoin Monthly Returns Heatmap by Year")

# Sidebar inputs for start and end dates
st.sidebar.header("Date Range")
start_date = st.sidebar.date_input("Start Date", value=pd.to_datetime("2014-01-01"))
end_date = st.sidebar.date_input("End Date", value=pd.to_datetime("2024-12-31"))

# Function to fetch and plot data
def plot_heatmap(start_date, end_date):
    # Fetch historical Bitcoin data based on selected date range
    btc_data = yf.download("BTC-USD", start=start_date, end=end_date, interval="1mo")

    # Check the column names of the data
    st.write("### Data Preview:")
    st.dataframe(btc_data.tail())  # Display the first few rows of data for inspection

    # Calculate monthly returns
    btc_data['Monthly Return'] = btc_data['Close'].pct_change()

    # Extract year and month from the DateTime index
    btc_data['Year'] = btc_data.index.year
    btc_data['Month'] = btc_data.index.month

    # Group by Year and Month to get average monthly returns for each year
    monthly_returns = btc_data.groupby(['Year', 'Month'])['Monthly Return'].mean().unstack()

    # Plotting the heatmap
    st.write("### Heatmap of Bitcoin Monthly Returns")
    plt.figure(figsize=(12, 6))
    sns.heatmap(monthly_returns, annot=True, cmap='RdYlGn', fmt='.2%', cbar=True, linewidths=0.5)

    # Show the plot in Streamlit
    st.pyplot(plt)

# Display the default chart first
plot_heatmap(pd.to_datetime("2014-01-01"), pd.to_datetime("2024-12-31"))

# Button to update chart based on selected dates
if st.sidebar.button("Update Chart"):
    plot_heatmap(start_date, end_date)




