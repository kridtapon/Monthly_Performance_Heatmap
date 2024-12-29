import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import yfinance as yf

# Set the Streamlit page configuration
st.set_page_config(
    page_title="Monthly Returns Heatmap",
    layout="centered",
    initial_sidebar_state="expanded",
)

# Title of the application
st.title("Monthly Returns Heatmap by Year")

# Sidebar inputs for asset symbol and date range
st.sidebar.header("Asset and Date Range")
symbol = st.sidebar.text_input("Enter Asset Symbol (e.g., BTC-USD)", value="BTC-USD")
start_date = st.sidebar.date_input("Start Date", value=pd.to_datetime("2014-01-01"))
end_date = st.sidebar.date_input("End Date", value=pd.to_datetime("2024-12-31"))

# Function to fetch and plot data
def plot_heatmap(symbol, start_date, end_date):
    # Fetch historical data for the given asset based on selected date range
    asset_data = yf.download(symbol, start=start_date, end=end_date, interval="1mo")

    # Check if data is empty
    if asset_data.empty:
        st.error(f"Could not retrieve data for symbol: {symbol}. Please check the symbol and try again.")
        return

    # Display data preview
    st.write(f"### Data Preview for {symbol}:")
    st.dataframe(asset_data.tail())  # Display the first few rows of data for inspection

    # Calculate monthly returns
    asset_data['Monthly Return'] = asset_data['Close'].pct_change()

    # Extract year and month from the DateTime index
    asset_data['Year'] = asset_data.index.year
    asset_data['Month'] = asset_data.index.month

    # Group by Year and Month to get average monthly returns for each year
    monthly_returns = asset_data.groupby(['Year', 'Month'])['Monthly Return'].mean().unstack()

    # Plotting the heatmap
    st.write(f"### Heatmap of Monthly Returns for {symbol}")
    plt.figure(figsize=(12, 6))
    sns.heatmap(monthly_returns, annot=True, cmap='RdYlGn', fmt='.2%', cbar=True, linewidths=0.5)

    # Show the plot in Streamlit
    st.pyplot(plt)

# Display a default example heatmap when the app loads
example_symbol = "BTC-USD"
example_start_date = pd.to_datetime("2014-01-01")
example_end_date = pd.to_datetime("2024-12-31")

st.write("### Example Heatmap (BTC-USD from 2014 to 2024):")
plot_heatmap(example_symbol, example_start_date, example_end_date)

# Button to update chart based on user input
if st.sidebar.button("Update Chart"):
    plot_heatmap(symbol, start_date, end_date)







