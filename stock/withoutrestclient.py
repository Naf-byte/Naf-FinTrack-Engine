import streamlit as st
import pandas as pd
import requests

# Your Polygon API key
API_KEY = 'y6LU1NRQtO2ogTHRIcMMxQoI2whgMPeG'

# Set page configuration
st.set_page_config(page_title="Stock Data Fetcher", layout="centered", page_icon="📈")

# Custom CSS for a modern UI
st.markdown(
    """
    <style>
    .main {
        background-color: #F3F4F6; 
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0px 0px 15px rgba(0, 0, 0, 0.1);
        font-family: 'Arial', sans-serif;
    }
    .stButton>button {
        background-color: #5A189A;
        color: #FFFFFF;
        font-size: 16px;
        padding: 10px 20px;
        border: none;
        border-radius: 5px;
        cursor: pointer;
    }
    .stButton>button:hover {
        background-color: #9D4EDD;
    }
    .stTextInput>div>div>input {
        background-color: #E5E5E5;
        color: #333333;
        border: 1px solid #CCCCCC;
        border-radius: 5px;
        padding: 10px;
    }
    </style>
    """, unsafe_allow_html=True
)

# App Title and Description
st.title("📈 Stock Data Fetcher")
st.markdown("Use this app to fetch stock data from the Polygon API based on your custom inputs.")

# User Input Widgets
ticker = st.text_input("Enter Ticker Symbol (e.g., AAPL):", value="AAPL").upper()
multiplier = st.number_input("Enter Multiplier (e.g., 1 for minute data):", min_value=1, value=1)
timespan = st.selectbox("Select Timespan:", options=["minute", "hour", "day"], index=0)
from_date = st.date_input("Start Date:", value=pd.to_datetime("2014-01-01"))
to_date = st.date_input("End Date:", value=pd.to_datetime("2024-01-01"))

# Function to fetch data from the Polygon API
def fetch_data(ticker, multiplier, timespan, from_date, to_date, api_key):
    url = f"https://api.polygon.io/v2/aggs/ticker/{ticker}/range/{multiplier}/{timespan}/{from_date}/{to_date}"
    params = {
        'apiKey': api_key
    }
    response = requests.get(url, params=params)
    
    if response.status_code == 200:
        return response.json()
    else:
        st.error(f"Error fetching data: {response.status_code} - {response.text}")
        return None

# Fetch and Display Data
if st.button("Fetch Data"):
    st.write("Fetching data...")

    # Fetch data from Polygon API
    data = fetch_data(ticker, multiplier, timespan, from_date.strftime('%Y-%m-%d'), to_date.strftime('%Y-%m-%d'), API_KEY)
    
    if data and 'results' in data:
        # Convert the response data to a DataFrame
        df = pd.DataFrame(data['results'])

        # Convert timestamp to datetime format
        df['t'] = pd.to_datetime(df['t'], unit='ms')
        df.rename(columns={'t': 'timestamp', 'o': 'open', 'c': 'close', 'h': 'high', 'l': 'low', 'v': 'volume'}, inplace=True)
        
        # Display the DataFrame in the app
        st.dataframe(df)

        # Save the DataFrame to an Excel file
        output_filename = f"{ticker}_stock_data_{from_date}_to_{to_date}.xlsx"
        df.to_excel(output_filename, index=False)
        st.success(f"Data fetched successfully and saved to '{output_filename}'.")
        st.download_button(label="Download Excel File", data=open(output_filename, 'rb').read(), file_name=output_filename)
    else:
        st.error("No data available for the selected parameters. Please try different inputs.")
