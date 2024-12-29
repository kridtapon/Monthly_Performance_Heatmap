import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import yfinance as yf
import streamlit as st

# Title for the Streamlit app
st.title("Monthly Returns Heatmap")

# User input for start date, end date, and symbol
start_date = st.date_input("Start Date", pd.to_datetime("2014-01-01"))
end_date = st.date_input("End Date", pd.to_datetime("2024-12-31"))
symbol = st.text_input("Enter Symbol (e.g., BTC-USD)", "BTC-USD")

# Ensure that the start date is before the end date
if start_date > end_date:
    st.error("Start date must be before end date.")
else:
    # Download historical data for the given symbol and date range
    data = yf.download(symbol, start=start_date, end=end_date)
    data.columns = ['Close', 'High', 'Low', 'Open', 'Volume']
    data = data.resample("ME").agg({"Open":"first",
                                   "High":"max",
                                   "Low":"min",
                                   "Close":"last",
                                   "Volume":"sum"})

    # Calculate monthly returns
    data['Monthly Return'] = data['Close'].pct_change()

    # Extract year and month from the DateTime index
    data['Year'] = data.index.year
    data['Month'] = data.index.month

    # Group by Year and Month to get average monthly returns for each year
    monthly_returns = data.groupby(['Year', 'Month'])['Monthly Return'].mean().unstack()

    # Plotting the heatmap with a red-to-green colormap
    fig, ax = plt.subplots(figsize=(12, 6))
    sns.heatmap(monthly_returns, annot=True, cmap='RdYlGn', fmt='.2%', linewidths=0.5, cbar_kws={'label': 'Monthly Return'}, ax=ax)
    ax.set_title(f'{symbol} Monthly Returns Heatmap by Year')
    ax.set_ylabel('Year')
    ax.set_xlabel('Month')
    ax.set_xticks(np.arange(0, 12, 1))
    ax.set_xticklabels(['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'], rotation=45)

    # Display the plot in Streamlit
    st.pyplot(fig)









