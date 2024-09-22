import streamlit as st
from polygon import RESTClient
import pandas as pd
import config  # Ensure your API key is correctly stored in this config file

# Initialize the Polygon REST client
client = RESTClient(config.API_KEY)

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

# Fetch and Display Data
if st.button("Fetch Data"):
    st.write("Fetching data...")

    try:
        # Fetch aggregate data based on user input
        aggs = client.get_aggs(
            ticker=ticker,
            multiplier=multiplier,
            timespan=timespan,
            from_=from_date.strftime('%Y-%m-%d'),
            to=to_date.strftime('%Y-%m-%d')
        )

        # Convert the response data to a DataFrame
        df = pd.DataFrame(aggs)

        if df.empty:
            st.error("No data available for the selected parameters. Please try different inputs.")
        else:
            # Convert timestamp to datetime format
            df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')

            # Display the DataFrame in the app
            st.dataframe(df)

            # Download button for Excel file
            output_filename = f"{ticker}_stock_data_{from_date}_to_{to_date}.xlsx"
            df.to_excel(output_filename, index=False)
            st.success(f"Data fetched successfully and saved to '{output_filename}'.")
            st.download_button(label="Download Excel File", data=open(output_filename, 'rb').read(),
                               file_name=output_filename)

    except Exception as e:
        st.error(f"An error occurred: {e}")
