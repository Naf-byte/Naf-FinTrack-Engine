import streamlit as st
import pandas as pd
import plotly.express as px
import yfinance as yf
from io import BytesIO

try:
    from polygon import RESTClient
except ImportError:
    RESTClient = None

# ---------- Custom CSS ----------
st.markdown("""
    <style>
    .main {
        background-color: #000000;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0px 0px 15px rgba(0, 0, 0, 0.1);
        font-family: 'Arial', sans-serif;
        color: #FFFFFF;
        text-align: center;
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
    .input-container {
        display: flex;
        justify-content: center;
        align-items: center;
        gap: 20px;
        flex-wrap: wrap;
    }
    .input-container div {
        flex: 1;
        min-width: 200px;
    }
    .green-container {
        background-color: #DFF2BF;
        padding: 10px;
        border-radius: 5px;
        color: #4F8A10;
        font-weight: bold;
        margin-bottom: 15px;
    }
    h1 {
        font-size: 36px;
        margin-bottom: 10px;
        margin-top: 0;
    }
    .tagline {
        font-size: 18px;
        color: #DDDDDD;
        margin-bottom: 10px;
    }
    .footer {
        position: fixed;
        bottom: 0;
        width: 100%;
        text-align: center;
        color: #DDDDDD;
        padding: 10px;
        font-size: 14px;
    }
    </style>
""", unsafe_allow_html=True)

# ---------- Helper Functions ----------
def to_excel_download(df, filename):
    output = BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=True)
    output.seek(0)
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.download_button(
            label="Download Excel File",
            data=output,
            file_name=filename,
            mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
# ---------- Home Page ----------
def show_home():
    st.markdown("<h2 style='text-align:center;'>🧠 Choose Your Data Source</h2>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        option = st.radio(
            "Select an Option:",
            ["Continue with Yahoo Finance", "Continue with Polygon Premium Insights"],
            index=None
        )
        if option == "Continue with Yahoo Finance":
            if st.button("📊 Launch Yahoo Finance Dashboard"):
                st.session_state.page = "yahoo"
        elif option == "Continue with Polygon Premium Insights":
            api_key = st.text_input("🔐 Enter your Polygon API key", type="password")
            if api_key and st.button("📈 Launch Premium Insights"):
                try:
                    client = RESTClient(api_key)
                    status = client.get_market_status()
                    st.session_state.polygon_key = api_key
                    st.session_state.page = "polygon"
                except Exception as e:
                    if "Unknown API Key" in str(e):
                        st.error("Invalid API Key. Please enter a valid API key.")
                    else:
                        st.error(f"API Key Error: {e}")

# ---------- Yahoo Finance Dashboard ---
# -------
def show_yahoo():
    st.markdown(
        '<style>div.block-container{padding-top:0rem; padding-left: 0rem; padding-right: 0rem;}</style>',
        unsafe_allow_html=True,
    )
    
    # st.set_page_config(page_title="Naf-YFinance - Stock Data Fetcher", layout="wide", page_icon="📈")
    # st.title("📊 Yahoo Finance Dashboard")

    st.set_page_config(page_title="Naf-YFinance - Stock Data Fetcher", layout="wide", page_icon="📈")
    # st.markdown("<h1 style='text-align:center;'>📊 Yahoo Finance Dashboard</h1>", unsafe_allow_html=True)
    # st.markdown('<p class="tagline" style="text-align:center;">Efficient Data Retrieval and Analysis for Investors with Advanced S&P-500 Stock Insights from Yahoo Finance </p>', unsafe_allow_html=True)

    # Custom CSS for a modern UI with black background
    st.markdown(
        """
        <style>
        .main {
            background-color: #000000;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0px 0px 15px rgba(0, 0, 0, 0.1);
            font-family: 'Arial', sans-serif;
            color: #FFFFFF;
            text-align: center;
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
        .input-container {
            display: flex;
            justify-content: center;
            align-items: center;
            gap: 20px;
            flex-wrap: wrap;
        }
        .input-container div {
            flex: 1;
            min-width: 200px;
        }
        .green-container {
            background-color: #DFF2BF;
            padding: 10px;
            border-radius: 5px;
            color: #4F8A10;
            font-weight: bold;
            margin-bottom: 15px;
        }

        .stButton .back-btn {
            background-color: #0B5345 !important;
            color: #fff !important;
            font-size: 16px;
            padding: 10px 20px;
            border-radius: 5px;
            border: none;
        }
        .stButton .back-btn:hover {
            background-color: #117A65 !important;
        }

        h1 {
            font-size: 36px;  /* Increased the size of the main heading */
            margin-bottom: 10px;
            margin-top: 0;  /* Removed extra padding from the top */
        }
        .tagline {
            font-size: 18px;
            color: #DDDDDD;
            margin-bottom: 10px;
        }
        .footer {
            position: fixed;
            bottom: 0;
            width: 100%;
            text-align: center;
            color: #DDDDDD;
            padding: 10px;
            font-size: 14px;
        }
        </style>
        """, unsafe_allow_html=True
    )



    # App Title and Tagline
    st.markdown("<h1 style='text-align:center;'>Naf-FinTrack Engine📈</h1>", unsafe_allow_html=True)
    # Naf - YFinance - Track S & P - 500 Stock Data with no hustle
    # st.markdown("""
    # <h1><img src= "Naf-YFinance Tracker.png" style="width:30px; vertical-align:middle; margin-right:10px;"> Naf-YFinance - Stock Data Fetcher</h1>
    # """, unsafe_allow_html=True)
    st.markdown('<p class="tagline">Efficient Data Retrieval and Analysis for Investors with Advanced S&P-500 Stock Insights from Yahoo Finance.</p>', unsafe_allow_html=True)

    # Sidebar for User Input
    st.sidebar.header("User Input")
    ticker = st.sidebar.text_input("Enter Ticker Symbol (e.g., AAPL):", value="AAPL").upper()
    multiplier = st.sidebar.number_input("Enter Multiplier (e.g., 1 for minute data):", min_value=1, value=1)
    timespan = st.sidebar.selectbox("Select Timespan:",
                                    options=["second", "minute", "hour", "day", "week", "month", "quarter", "year"],
                                    index=0)
    from_date = st.sidebar.date_input("Start Date:", value=pd.to_datetime("2014-01-01"))
    to_date = st.sidebar.date_input("End Date:", value=pd.to_datetime("2024-01-01"))

    # Function to fetch stock data and financials
    def fetch_data(ticker, from_date, to_date, multiplier, timespan):
        try:
            # Use yfinance to fetch historical stock data
            stock = yf.Ticker(ticker)
            data = stock.history(start=from_date, end=to_date)

            # Financial statements
            income_statement = stock.financials
            cash_flow = stock.cashflow
            balance_sheet = stock.balance_sheet

            return data, income_statement, cash_flow, balance_sheet

        except Exception as e:
            st.error(f"An error occurred: {e}")
            return pd.DataFrame(), pd.DataFrame(), pd.DataFrame(), pd.DataFrame()


    # Helper function to fetch data
    def fetch_gap_data(ticker, from_date, to_date):
        try:
            stock = yf.Ticker(ticker)
            data = stock.history(start=from_date, end=to_date)
            return data
        except Exception as e:
            st.error(f"An error occurred: {e}")
            return pd.DataFrame()

    # Main app
    st.title("Stock Analysis App")

    # Create tabs for different sections
    tab1, tab2, tab3 = st.tabs(["Stock Data", "Financial Statements", "Stock Analysis"])

    # Tab 1: Stock Data
    with tab1:
        st.header("Stock Data")
        # data, data, _, _, _ = fetch_data(ticker, from_date, to_date, multiplier, timespan)
        data, _, _, _ = fetch_data(ticker, from_date, to_date, multiplier, timespan)


        if not data.empty:
            fig = px.line(data, x=data.index, y='Close', title=f"{ticker} Stock Prices",
                        line_shape='linear',
                        color_discrete_sequence=['#5AB834'])
            st.plotly_chart(fig)
        else:
            st.error("No data available for the selected ticker.")

    if data.empty:
        st.error("No data available for the selected parameters.")
    else:
        st.dataframe(data)

        output_filename = f"{ticker}_stock_data_{from_date}_to_{to_date}.xlsx"
        data.index = data.index.tz_localize(None)
        data.to_excel(output_filename, index=True)
        st.success(f"Data fetched successfully and saved to '{output_filename}'.")

        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.download_button(label="Download Excel File", data=open(output_filename, 'rb').read(),
                            file_name=output_filename)


    # Tab 2: Financial Statements
    with tab2:
        st.header("Financial Statements")
        _, income_statement, cash_flow, balance_sheet = fetch_data(ticker, from_date, to_date, multiplier, timespan)

        # Display Income Statement and Cash Flow
        if not income_statement.empty:
            st.subheader("Income Statement")
            st.dataframe(income_statement)
            # Download button for Income Statement
            income_output_filename = f"{ticker}_income_statement.xlsx"
            income_statement.to_excel(income_output_filename)

            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                st.download_button(label="Download Income Statement", data=open(income_output_filename, 'rb').read(),
                                file_name=income_output_filename)
        else:
            st.error("No income statement data available.")

        if not cash_flow.empty:
            st.subheader("Cash Flow Statement")
            st.dataframe(cash_flow)
            # Download button for Cash Flow
            cash_flow_output_filename = f"{ticker}_cash_flow.xlsx"
            cash_flow.to_excel(cash_flow_output_filename)

            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                st.download_button(label="Download Cash Flow Statement", data=open(cash_flow_output_filename, 'rb').read(),
                                file_name=cash_flow_output_filename)
        else:
            st.error("No cash flow data available.")

        # Display Balance Sheet
        if not balance_sheet.empty:
            st.subheader("Balance Sheet")
            st.dataframe(balance_sheet)
            # Download button for Balance Sheet
            balance_sheet_output_filename = f"{ticker}_balance_sheet.xlsx"
            balance_sheet.to_excel(balance_sheet_output_filename)

            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                st.download_button(label="Download Balance Sheet", data=open(balance_sheet_output_filename, 'rb').read(),
                                file_name=balance_sheet_output_filename)
        else:
            st.error("No balance sheet data available.")

    # Tab 3: Stock Analysis
    with tab3:
        st.header("Stock Analysis")
        subtab1, subtab2 = st.tabs(["Stock Comparison", "Gap Analysis"])

        # Sub-tab 1: Stock Comparison
        with subtab1:
            st.subheader("Stock Comparison")

            # User inputs for stock comparison
            st.markdown('<div class="input-container">', unsafe_allow_html=True)
            col1, col2 = st.columns(2)

            with col1:
                ticker1 = st.text_input("Enter First Ticker Symbol (e.g., AAPL):", value="AAPL").upper()
                multiplier1 = st.number_input("Enter Multiplier for First Ticker (e.g., 1 for minute data):", min_value=1, value=1, key='multiplier1')
                timespan1 = st.selectbox("Select Timespan for First Ticker:",
                                        options=["second", "minute", "hour", "day", "week", "month", "quarter", "year"],
                                        index=0, key='timespan1')
                from_date1 = st.date_input("Start Date for First Ticker:", value=pd.to_datetime("2024-01-01"), key='from_date1')
                to_date1 = st.date_input("End Date for First Ticker:", value=pd.to_datetime("2024-09-30"), key='to_date1')

            with col2:
                ticker2 = st.text_input("Enter Second Ticker Symbol (e.g., MSFT):", value="MSFT").upper()
                multiplier2 = st.number_input("Enter Multiplier for Second Ticker:", min_value=1, value=1, key='multiplier2')
                timespan2 = st.selectbox("Select Timespan for Second Ticker:",
                                        options=["second", "minute", "hour", "day", "week", "month", "quarter", "year"],
                                        index=0, key='timespan2')
                from_date2 = st.date_input("Start Date for Second Ticker:", value=pd.to_datetime("2024-01-01"), key='from_date2')
                to_date2 = st.date_input("End Date for Second Ticker:", value=pd.to_datetime("2024-09-30"), key='to_date2')

            st.markdown('</div>', unsafe_allow_html=True)

            # Fetch data for both tickers
            data1, _, _, _ = fetch_data(ticker1, from_date1, to_date1, multiplier1, timespan1)
            data2, _, _, _ = fetch_data(ticker2, from_date2, to_date2, multiplier2, timespan2)

            if not data1.empty and not data2.empty:
                fig1 = px.line(data1, x=data1.index, y='Close', title=f"{ticker1} Stock Prices",
                            line_shape='linear',
                            color_discrete_sequence=['#FF7F0E'])
                fig2 = px.line(data2, x=data2.index, y='Close', title=f"{ticker2} Stock Prices",
                            line_shape='linear',
                            color_discrete_sequence=['#1F77B4'])

                st.subheader(f"Comparison of {ticker1} and {ticker2}")
                col1, col2 = st.columns(2)

                with col1:
                    st.plotly_chart(fig1)

                with col2:
                    st.plotly_chart(fig2)

                comparison_df = pd.DataFrame({
                    'Metrics': ['Highest Open Value', 'Lowest Close Value'],
                    f'{ticker1}': [data1['Open'].max(), data1['Close'].min()],
                    f'{ticker2}': [data2['Open'].max(), data2['Close'].min()]
                })

                st.subheader("Comparison Summary")
                st.dataframe(comparison_df)

            else:
                st.error("No data available for one or both tickers.")


        # Sub-tab 2: Gap Analysis
        # Helper function to fetch gap data
        def fetch_gap_data(ticker, from_date, to_date):
            try:
                stock = yf.Ticker(ticker)
                data = stock.history(start=from_date, end=to_date)
                return data
            except Exception as e:
                st.error(f"An error occurred: {e}")
                return pd.DataFrame()


        # Function to add colored KPI symbols for Gap %
        def add_kpi_symbols(row):
            if row['Gap %'] > 0:
                return f"<span style='color: green;'>▲ {row['Gap %']:.2f}%</span>"
            elif row['Gap %'] < 0:
                return f"<span style='color: red;'>🔻 {row['Gap %']:.2f}%</span>"
            else:
                return f"<span>➖ {row['Gap %']:.2f}%</span>"


        # Sub-tab 2: Gap Analysis
        with subtab2:
            # st.header("Gap Analysis")
            st.markdown("<h2 style='text-align:center;'>Gap Analysis</h2>", unsafe_allow_html=True)

            # User inputs for gap analysis
            gap_ticker = st.text_input("Enter Ticker Symbol for Gap Analysis:", value="AAPL").upper()
            gap_from_date = st.date_input("Start Date for Gap Analysis:", value=pd.to_datetime("2024-01-01"))
            gap_to_date = st.date_input("End Date for Gap Analysis:", value=pd.to_datetime("2024-09-30"))

            gap_data = fetch_gap_data(gap_ticker, gap_from_date, gap_to_date)

            if not gap_data.empty:
                # Calculate weekly high, low, opening, closing, and volume
                gap_data['Week'] = gap_data.index.to_period('W')
                weekly_data = gap_data.groupby('Week').agg(
                    Highest_in_week=('High', 'max'),
                    Lowest_in_week=('Low', 'min'),
                    Opening_week=('Open', 'first'),
                    Closing_week=('Close', 'last'),
                    Volume=('Volume', 'sum')
                ).reset_index()



                # Calculate the week start and end dates
                weekly_data['Week Start'] = weekly_data['Week'].apply(lambda x: x.start_time.strftime('%Y-%m-%d'))
                weekly_data['Week End'] = weekly_data['Week'].apply(
                    lambda x: (x.end_time - pd.Timedelta(days=2)).strftime('%Y-%m-%d'))
                weekly_data['Week Range'] = weekly_data['Week Start'] + ' - ' + weekly_data['Week End']

                # Add a "Week Number" column that shows Week 1, Week 2, etc.
                weekly_data['Week Number'] = 'Week ' + (weekly_data.index + 1).astype(str)

                # Calculate gap and gap percentage
                weekly_data['Gap'] = weekly_data['Closing_week'].shift(-2) - weekly_data['Opening_week']
                weekly_data['Gap %'] = (weekly_data['Gap'] / weekly_data['Opening_week'].shift(-1)) * 100

                # Add KPI symbols column
                weekly_data['Gap % with KPI'] = weekly_data.apply(add_kpi_symbols, axis=1)

                # Select only the relevant columns, including "Week Range"
                display_data = weekly_data[
                    ['Week Number', 'Week Range', 'Gap % with KPI', 'Highest_in_week', 'Lowest_in_week', 'Opening_week', 'Closing_week',
                    'Volume']]

                # Set custom style to prevent wrapping and center-align the table
                st.write("""
                <style>
                .table-container {
                    width: auto;
                    max-width: 100%;
                    margin: auto;
                    text-align: center;
                    white-space: nowrap;
                    overflow-x: auto;
                }
                .table-container table {
                    margin: auto;
                }
                .summary-heading {
                    margin: 0; /* Remove margin from the heading */
                }
                .summary-table-container {
                    display: flex;
                    justify-content: center;
                    align-items: center;
                    width: 100%;
                    margin: 0; /* Remove margin from the table container */
                }
                .summary-table {
                    width: auto;
                    max-width: 80%; /* Adjust as needed */
                    border-collapse: collapse;
                    text-align: center;
                }
                .summary-table th, .summary-table td {
                    border: 2px solid #ddd;
                    padding: 10px;
                }
                .summary-table th {
                    background-color: #f2f2f2;
                    color: #333;
                }
                .summary-table td {
                    background-color: #f9f9f9;
                }
                </style>
                """, unsafe_allow_html=True)

                # Display the table with custom style
                st.write('<div class="table-container">' + display_data.to_html(index=False, escape=False) + '</div>',
                        unsafe_allow_html=True)

                # Calculate Gap Analysis Summary
                highest_gap_row = weekly_data.loc[weekly_data['Gap %'].idxmax()]  # Find the row with the highest gap %

                # Create a summary DataFrame
                summary_df = pd.DataFrame({
                    'Metrics': ['Week Number', 'Highest in Week', 'Lowest in Week', 'Opening in Week', 'Closing in Week',
                                'Volume', 'Highest Gap %'],
                    'Value': [
                        highest_gap_row['Week Number'],
                        f"{highest_gap_row['Highest_in_week']:.2f}",
                        f"{highest_gap_row['Lowest_in_week']:.2f}",
                        f"{highest_gap_row['Opening_week']:.2f}",
                        f"{highest_gap_row['Closing_week']:.2f}",
                        f"{highest_gap_row['Volume']:,}",
                        highest_gap_row['Gap % with KPI']
                    ]
                })
                if not gap_data.empty:
                    gap_data['Gap'] = gap_data['Close'] - gap_data['Close'].shift(1)
                    gap_data.dropna(inplace=True)

                    st.subheader("Gap Analysis Data")
                    st.dataframe(gap_data[['Open', 'Close', 'Gap']])

                    # Graph for Gap Analysis
                    fig = px.line(gap_data, x=gap_data.index, y='Gap', title=f"{gap_ticker} Gap Analysis",
                                line_shape='linear', color_discrete_sequence=['#FF6347'])
                    st.plotly_chart(fig)

                # Display the summary DataFrame with st.write and HTML for KPI symbols
                st.subheader("Gap Analysis Summary")
                st.write('<div class="summary-heading"></div>', unsafe_allow_html=True)
                st.write(
                    '<div class="summary-table-container"><table class="summary-table">' + summary_df.to_html(index=False,
                                                                                                            escape=False) + '</table></div>',
                    unsafe_allow_html=True)

            else:
                st.error("No data available for the selected ticker and date range.")

    if st.button("⬅️ Back"):
        st.session_state.page = "home"

# ---------- Polygon Premium Insights Dashboard ----------
def show_polygon():
    # st.set_page_config(page_title="Naf-YFinance - Stock Data Fetcher", layout="wide", page_icon="📈")
    # st.title("💼 Polygon Premium Insights")
    st.set_page_config(page_title="Naf-YFinance - Stock Data Fetcher", layout="wide", page_icon="📈")
    st.markdown("<h1 style='text-align:center;'>💼 Polygon Premium Insights</h1>", unsafe_allow_html=True)
    st.markdown('<p class="tagline" style="text-align:center;">Efficient Data Retrieval and Analysis for Investors with Advanced S&P-500 Stock Insights from Polygon 📈</p>', unsafe_allow_html=True)


    api_key = st.session_state.get("polygon_key", "")
    if not api_key:
        st.warning("Please enter your Polygon API key to continue.")
        if st.button("⬅️ Back"):
            st.session_state.page = "home"
        return

    try:
        client = RESTClient(api_key)
    except Exception as e:
        st.error(f"Could not initialize Polygon client: {e}")
        if st.button("⬅️ Back"):
            st.session_state.page = "home"
        return

    # Set page configuration



    # Custom CSS for a modern UI with black background
    st.markdown(
        """
        <style>
        .main {
            background-color: #000000;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0px 0px 15px rgba(0, 0, 0, 0.1);
            font-family: 'Arial', sans-serif;
            color: #FFFFFF;
            text-align: center;
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
        .input-container {
            display: flex;
            justify-content: center;
            align-items: center;
            gap: 20px;
            flex-wrap: wrap;
        }
        .input-container div {
            flex: 1;
            min-width: 200px;
        }
        .stButton .back-btn {
            background-color: #0B5345 !important;
            color: #fff !important;
            font-size: 16px;
            padding: 10px 20px;
            border-radius: 5px;
            border: none;
        }
        .stButton .back-btn:hover {
            background-color: #117A65 !important;
        }
        .green-container {
            background-color: #DFF2BF;
            padding: 10px;
            border-radius: 5px;
            color: #4F8A10;
            font-weight: bold;
            margin-bottom: 15px;
        }
        h1 {
            font-size: 36px;  /* Increased the size of the main heading */
            margin-bottom: 10px;
            margin-top: 0;  /* Removed extra padding from the top */
        }
        .tagline {
            font-size: 18px;
            color: #DDDDDD;
            margin-bottom: 10px;
        }
        .footer {
            position: fixed;
            bottom: 0;
            width: 100%;
            text-align: center;
            color: #DDDDDD;
            padding: 10px;
            font-size: 14px;
        }
        </style>
        """, unsafe_allow_html=True
    )



    # App Title and Tagline
    st.markdown("<h1 style='text-align:center;'>Naf-FinTrack Engine📈</h1>", unsafe_allow_html=True)
    # Naf - YFinance - Track S & P - 500 Stock Data with no hustle
    # st.markdown("""
    # <h1><img src= "Naf-YFinance Tracker.png" style="width:30px; vertical-align:middle; margin-right:10px;"> Naf-YFinance - Stock Data Fetcher</h1>
    # """, unsafe_allow_html=True)
    st.markdown('<p class="tagline">Efficient Data Retrieval and Analysis for Investors with Advanced S&P-500 Stock Insights from Yahoo Finance.</p>', unsafe_allow_html=True)

    # Sidebar for User Input
    st.sidebar.header("User Input")
    ticker = st.sidebar.text_input("Enter Ticker Symbol (e.g., AAPL):", value="AAPL").upper()
    multiplier = st.sidebar.number_input("Enter Multiplier (e.g., 1 for minute data):", min_value=1, value=1)
    timespan = st.sidebar.selectbox("Select Timespan:",
                                    options=["second", "minute", "hour", "day", "week", "month", "quarter", "year"],
                                    index=0)
    from_date = st.sidebar.date_input("Start Date:", value=pd.to_datetime("2014-01-01"))
    to_date = st.sidebar.date_input("End Date:", value=pd.to_datetime("2024-01-01"))

    # Function to fetch stock data and financials
    def fetch_data(ticker, from_date, to_date, multiplier, timespan):
        try:
            aggs = client.get_aggs(
                ticker=ticker,
                multiplier=multiplier,
                timespan=timespan,
                from_=from_date.strftime('%Y-%m-%d'),
                to=to_date.strftime('%Y-%m-%d')
            )
            df = pd.DataFrame(aggs)

            # Download data using yfinance for visualization
            stock = yf.Ticker(ticker)
            data = stock.history(start=from_date, end=to_date)

            # Fetch financial data
            income_statement = stock.financials
            cash_flow = stock.cashflow
            balance_sheet = stock.balance_sheet  # Fetch balance sheet

            return df, data, income_statement, cash_flow, balance_sheet
        except Exception as e:
            st.error(f"An error occurred: {e}")
            return pd.DataFrame(), pd.DataFrame(), pd.DataFrame(), pd.DataFrame(), pd.DataFrame()

    # Helper function to fetch data
    def fetch_gap_data(ticker, from_date, to_date):
        try:
            stock = yf.Ticker(ticker)
            data = stock.history(start=from_date, end=to_date)
            return data
        except Exception as e:
            st.error(f"An error occurred: {e}")
            return pd.DataFrame()

    # Download button for Excel file
    from io import BytesIO

    # Convert to Excel in-memory
    def to_excel_download(df, filename):
        output = BytesIO()
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            df.to_excel(writer, index=True)
        output.seek(0)
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.download_button(
                label="Download Excel File",
                data=output,
                file_name=filename,
                mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
            )
    # Main app
    st.title("Stock Analysis App")

    # Create tabs for different sections
    tab1, tab2, tab3 = st.tabs(["Stock Data", "Financial Statements", "Stock Analysis"])

    # Tab 1: Stock Data
    with tab1:
        st.header("Stock Data")
        df, data, _, _, _ = fetch_data(ticker, from_date, to_date, multiplier, timespan)

        if not data.empty:
            fig = px.line(data, x=data.index, y='Close', title=f"{ticker} Stock Prices",
                        line_shape='linear',
                        color_discrete_sequence=['#5AB834'])
            st.plotly_chart(fig)
        else:
            st.error("No data available for the selected ticker.")

        if df.empty:
            st.error("No data available for the selected parameters. Please try different inputs.")
        else:
            df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
            df.set_index('timestamp', inplace=True)
            st.dataframe(df)

            # Use the function
            excel_filename = f"{ticker}_stock_data_{from_date}_to_{to_date}.xlsx"
            st.success("Data fetched successfully.")
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                st.download_button(
                    label="Download Excel File",
                    data=df.to_excel(excel_filename),
                    file_name=excel_filename,
                    mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
                )


    # Tab 2: Financial Statements
    with tab2:
        st.header("Financial Statements")

        _, _, income_statement, cash_flow, balance_sheet = fetch_data(ticker, from_date, to_date, multiplier, timespan)

        # Display Income Statement and Cash Flow
        if not income_statement.empty:
            st.subheader("Income Statement")
            st.dataframe(income_statement)
            # Download button for Income Statement
            income_output_filename = f"{ticker}_income_statement.xlsx"
            income_statement.to_excel(income_output_filename)
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                st.download_button(
                    label="Download Income Statement",
                    data=open(income_output_filename, 'rb').read(),
                    file_name=income_output_filename
                )
        else:
            st.error("No income statement data available.")

        if not cash_flow.empty:
            st.subheader("Cash Flow Statement")
            st.dataframe(cash_flow)
            # Download button for Cash Flow
            cash_flow_output_filename = f"{ticker}_cash_flow.xlsx"
            cash_flow.to_excel(cash_flow_output_filename)
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                st.download_button(
                    label="Download Cash Flow Statement",
                    data=open(cash_flow_output_filename, 'rb').read(),
                    file_name=cash_flow_output_filename
                )
        else:
            st.error("No cash flow data available.")

        # Display Balance Sheet
        if not balance_sheet.empty:
            st.subheader("Balance Sheet")
            st.dataframe(balance_sheet)
            # Download button for Balance Sheet
            balance_sheet_output_filename = f"{ticker}_balance_sheet.xlsx"
            balance_sheet.to_excel(balance_sheet_output_filename)
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                st.download_button(
                    label="Download Balance Sheet",
                    data=open(balance_sheet_output_filename, 'rb').read(),
                    file_name=balance_sheet_output_filename
                )
        else:
            st.error("No balance sheet data available.")

    # Tab 3: Stock Analysis
    with tab3:
        st.header("Stock Analysis")
        subtab1, subtab2 = st.tabs(["Stock Comparison", "Gap Analysis"])

        # Sub-tab 1: Stock Comparison
        with subtab1:
            st.subheader("Stock Comparison")


            # User inputs for stock comparison
            st.markdown('<div class="input-container">', unsafe_allow_html=True)
            col1, col2 = st.columns(2)

            with col1:
                ticker1 = st.text_input("Enter First Ticker Symbol (e.g., AAPL):", value="AAPL").upper()
                multiplier1 = st.number_input("Enter Multiplier for First Ticker (e.g., 1 for minute data):", min_value=1, value=1, key='multiplier1')
                timespan1 = st.selectbox("Select Timespan for First Ticker:",
                                        options=["second", "minute", "hour", "day", "week", "month", "quarter", "year"],
                                        index=0, key='timespan1')
                from_date1 = st.date_input("Start Date for First Ticker:", value=pd.to_datetime("2024-01-01"), key='from_date1')
                to_date1 = st.date_input("End Date for First Ticker:", value=pd.to_datetime("2024-09-30"), key='to_date1')

            with col2:
                ticker2 = st.text_input("Enter Second Ticker Symbol (e.g., MSFT):", value="MSFT").upper()
                multiplier2 = st.number_input("Enter Multiplier for Second Ticker (e.g., 1 for minute data):", min_value=1, value=1, key='multiplier2')
                timespan2 = st.selectbox("Select Timespan for Second Ticker:",
                                        options=["second", "minute", "hour", "day", "week", "month", "quarter", "year"],
                                        index=0, key='timespan2')
                from_date2 = st.date_input("Start Date for Second Ticker:", value=pd.to_datetime("2024-01-01"), key='from_date2')
                to_date2 = st.date_input("End Date for Second Ticker:", value=pd.to_datetime("2024-09-30"), key='to_date2')

            st.markdown('</div>', unsafe_allow_html=True)

            # Fetch data for both tickers
            df1, data1, _, _, _ = fetch_data(ticker1, from_date1, to_date1, multiplier1, timespan1)
            df2, data2, _, _, _ = fetch_data(ticker2, from_date2, to_date2, multiplier2, timespan2)

            if not data1.empty and not data2.empty:
                fig1 = px.line(data1, x=data1.index, y='Close', title=f"{ticker1} Stock Prices",
                            line_shape='linear',
                            color_discrete_sequence=['#FF7F0E'])
                fig2 = px.line(data2, x=data2.index, y='Close', title=f"{ticker2} Stock Prices",
                            line_shape='linear',
                            color_discrete_sequence=['#1F77B4'])

                st.subheader(f"Comparison of {ticker1} and {ticker2}")
                col1, col2 = st.columns(2)

                with col1:
                    st.plotly_chart(fig1)

                with col2:
                    st.plotly_chart(fig2)

                comparison_df = pd.DataFrame({
                    'Metrics': ['Highest Open Value', 'Lowest Close Value'],
                    f'{ticker1}': [data1['Open'].max(), data1['Close'].min()],
                    f'{ticker2}': [data2['Open'].max(), data2['Close'].min()]
                })

                st.subheader("Comparison Summary")
                st.dataframe(comparison_df)

            else:
                st.error("No data available for one or both tickers.")


        # Sub-tab 2: Gap Analysis
        # Helper function to fetch gap data
        # def fetch_gap_data(ticker, from_date, to_date):
        #     try:
        #         stock = yf.Ticker(ticker)
        #         data = stock.history(start=from_date, end=to_date)
        #         return data
        #     except Exception as e:
        #         st.error(f"An error occurred: {e}")
        #         return pd.DataFrame()


        # Function to add colored KPI symbols for Gap %
        def add_kpi_symbols(row):
            if row['Gap %'] > 0:
                return f"<span style='color: green;'>▲ {row['Gap %']:.2f}%</span>"
            elif row['Gap %'] < 0:
                return f"<span style='color: red;'>🔻 {row['Gap %']:.2f}%</span>"
            else:
                return f"<span>➖ {row['Gap %']:.2f}%</span>"


        # Sub-tab 2: Gap Analysis
        with subtab2:
            st.markdown("<h2 style='text-align:center;'>Gap Analysis</h2>", unsafe_allow_html=True)

            # User inputs for gap analysis
            gap_ticker = st.text_input("Enter Ticker Symbol for Gap Analysis:", value="AAPL").upper()
            gap_from_date = st.date_input("Start Date for Gap Analysis:", value=pd.to_datetime("2024-01-01"))
            gap_to_date = st.date_input("End Date for Gap Analysis:", value=pd.to_datetime("2024-09-30"))

            gap_data = fetch_gap_data(gap_ticker, gap_from_date, gap_to_date)

            if not gap_data.empty:
                # Calculate weekly high, low, opening, closing, and volume
                gap_data['Week'] = gap_data.index.to_period('W')
                weekly_data = gap_data.groupby('Week').agg(
                    Highest_in_week=('High', 'max'),
                    Lowest_in_week=('Low', 'min'),
                    Opening_week=('Open', 'first'),
                    Closing_week=('Close', 'last'),
                    Volume=('Volume', 'sum')
                ).reset_index()



                # Calculate the week start and end dates
                weekly_data['Week Start'] = weekly_data['Week'].apply(lambda x: x.start_time.strftime('%Y-%m-%d'))
                weekly_data['Week End'] = weekly_data['Week'].apply(
                    lambda x: (x.end_time - pd.Timedelta(days=2)).strftime('%Y-%m-%d'))
                weekly_data['Week Range'] = weekly_data['Week Start'] + ' - ' + weekly_data['Week End']

                # Add a "Week Number" column that shows Week 1, Week 2, etc.
                weekly_data['Week Number'] = 'Week ' + (weekly_data.index + 1).astype(str)

                # Calculate gap and gap percentage
                weekly_data['Gap'] = weekly_data['Closing_week'].shift(-2) - weekly_data['Opening_week']
                weekly_data['Gap %'] = (weekly_data['Gap'] / weekly_data['Opening_week'].shift(-1)) * 100

                # Add KPI symbols column
                weekly_data['Gap % with KPI'] = weekly_data.apply(add_kpi_symbols, axis=1)

                # Select only the relevant columns, including "Week Range"
                display_data = weekly_data[
                    ['Week Number', 'Week Range', 'Gap % with KPI', 'Highest_in_week', 'Lowest_in_week', 'Opening_week', 'Closing_week',
                    'Volume']]

                # Set custom style to prevent wrapping and center-align the table
                st.write("""
                <style>
                .table-container {
                    width: auto;
                    max-width: 100%;
                    margin: auto;
                    text-align: center;
                    white-space: nowrap;
                    overflow-x: auto;
                }
                .table-container table {
                    margin: auto;
                }
                .summary-heading {
                    margin: 0; /* Remove margin from the heading */
                }
                .summary-table-container {
                    display: flex;
                    justify-content: center;
                    align-items: center;
                    width: 100%;
                    margin: 0; /* Remove margin from the table container */
                }
                .summary-table {
                    width: auto;
                    max-width: 80%; /* Adjust as needed */
                    border-collapse: collapse;
                    text-align: center;
                }
                .summary-table th, .summary-table td {
                    border: 2px solid #ddd;
                    padding: 10px;
                }
                .summary-table th {
                    background-color: #f2f2f2;
                    color: #333;
                }
                .summary-table td {
                    background-color: #f9f9f9;
                }
                </style>
                """, unsafe_allow_html=True)

                # Display the table with custom style
                st.write('<div class="table-container">' + display_data.to_html(index=False, escape=False) + '</div>',
                        unsafe_allow_html=True)

                # Calculate Gap Analysis Summary
                highest_gap_row = weekly_data.loc[weekly_data['Gap %'].idxmax()]  # Find the row with the highest gap %

                # Create a summary DataFrame
                summary_df = pd.DataFrame({
                    'Metrics': ['Week Number', 'Highest in Week', 'Lowest in Week', 'Opening in Week', 'Closing in Week',
                                'Volume', 'Highest Gap %'],
                    'Value': [
                        highest_gap_row['Week Number'],
                        f"{highest_gap_row['Highest_in_week']:.2f}",
                        f"{highest_gap_row['Lowest_in_week']:.2f}",
                        f"{highest_gap_row['Opening_week']:.2f}",
                        f"{highest_gap_row['Closing_week']:.2f}",
                        f"{highest_gap_row['Volume']:,}",
                        highest_gap_row['Gap % with KPI']
                    ]
                })
                if not gap_data.empty:
                    gap_data['Gap'] = gap_data['Close'] - gap_data['Close'].shift(1)
                    gap_data.dropna(inplace=True)

                    st.subheader("Gap Analysis Data")
                    st.dataframe(gap_data[['Open', 'Close', 'Gap']])

                    # Graph for Gap Analysis
                    fig = px.line(gap_data, x=gap_data.index, y='Gap', title=f"{gap_ticker} Gap Analysis",
                                line_shape='linear', color_discrete_sequence=['#FF6347'])
                    st.plotly_chart(fig)

                # Display the summary DataFrame with st.write and HTML for KPI symbols
                st.subheader("Gap Analysis Summary")
                st.write('<div class="summary-heading"></div>', unsafe_allow_html=True)
                st.write(
                    '<div class="summary-table-container"><table class="summary-table">' + summary_df.to_html(index=False,
                                                                                                            escape=False) + '</table></div>',
                    unsafe_allow_html=True)

            else:
                st.error("No data available for the selected ticker and date range.")

    if st.button("⬅️ Back"):
        st.session_state.page = "home"

    # Footer
    st.markdown('<div class="footer">Powered by Naf-Byte (Nafay Ur Rehman)</div>', unsafe_allow_html=True)



# ---------- Navigation ----------
if "page" not in st.session_state:
    st.session_state.page = "home"

if st.session_state.page == "home":
    show_home()
elif st.session_state.page == "yahoo":
    show_yahoo()
elif st.session_state.page == "polygon":
    show_polygon()

# ---------- Footer ----------
st.markdown('<div class="footer">Powered by Naf-Byte (Nafay Ur Rehman)</div>', unsafe_allow_html=True)

# # import streamlit as st
# # from polygon import RESTClient
# # import pandas as pd
# # import plotly.express as px
# # import yfinance as yf
# #
# #
# # # Set page configuration at the very top of the script
# # # st.set_page_config(page_title="Naf-YFinance - Stock Data Fetcher", layout="wide")
# # # Correctly set the page configuration as the very first Streamlit command
# # st.set_page_config(
# #     page_title="Naf-YFinance - Stock Data Fetcher",
# #     page_icon="📈",
# #     layout="wide",
# #     initial_sidebar_state="expanded"
# # )
# # # st.set_page_config(page_title="Naf-YFinance - Stock Data Fetcher", layout="wide", page_icon="📈")
# #
# # # Initialize the Polygon REST client
# # API_KEY = 'y6LU1NRQtO2ogTHRIcMMxQoI2whgMPeG'  # Replace with your actual API key
# # client = RESTClient(API_KEY)
# #
# # # Custom CSS for a modern UI with black background
# # st.markdown(
# #     """
# #     <style>
# #     .main {
# #         background-color: #000000;
# #         padding: 20px;
# #         border-radius: 10px;
# #         box-shadow: 0px 0px 15px rgba(0, 0, 0, 0.1);
# #         font-family: 'Arial', sans-serif;
# #         color: #FFFFFF;
# #         text-align: center;
# #     }
# #     .stButton>button {
# #         background-color: #5A189A;
# #         color: #FFFFFF;
# #         font-size: 16px;
# #         padding: 10px 20px;
# #         border: none;
# #         border-radius: 5px;
# #         cursor: pointer;
# #     }
# #     .stButton>button:hover {
# #         background-color: #9D4EDD;
# #     }
# #     .stTextInput>div>div>input {
# #         background-color: #E5E5E5;
# #         color: #333333;
# #         border: 1px solid #CCCCCC;
# #         border-radius: 5px;
# #         padding: 10px;
# #     }
# #     .green-container {
# #         background-color: #DFF2BF;
# #         padding: 10px;
# #         border-radius: 5px;
# #         color: #4F8A10;
# #         font-weight: bold;
# #         margin-bottom: 15px;
# #     }
# #     h1 {
# #         font-size: 28px;
# #         margin-bottom: 10px;
# #         margin-top: 0;  /* Removed extra padding from top */
# #     }
# #     .tagline {
# #         font-size: 18px;
# #         color: #DDDDDD;
# #         margin-bottom: 10px;
# #     }
# #     .footer {
# #         position: fixed;
# #         bottom: 0;
# #         width: 100%;
# #         text-align: center;
# #         color: #DDDDDD;
# #         padding: 10px;
# #         font-size: 14px;
# #     }
# #     </style>
# #     """, unsafe_allow_html=True
# # )
# #
# # # App Title and Tagline
# # st.markdown("<h1>Naf-YFinance - Stock Data Fetcher 📈</h1>", unsafe_allow_html=True)
# # st.markdown('<p class="tagline">Download data from any stock company from symbol</p>', unsafe_allow_html=True)
# #
# # # Sidebar for User Input
# # st.sidebar.header("User Input")
# # ticker = st.sidebar.text_input("Enter Ticker Symbol (e.g., AAPL):", value="AAPL").upper()
# # multiplier = st.sidebar.number_input("Enter Multiplier (e.g., 1 for minute data):", min_value=1, value=1)
# # timespan = st.sidebar.selectbox("Select Timespan:",
# #                                 options=["second", "minute", "hour", "day", "week", "month", "quarter", "year"],
# #                                 index=0)
# # from_date = st.sidebar.date_input("Start Date:", value=pd.to_datetime("2014-01-01"))
# # to_date = st.sidebar.date_input("End Date:", value=pd.to_datetime("2024-01-01"))
# #
# #
# # # Function to fetch stock data and financials
# # def fetch_data():
# #     try:
# #         # Fetch aggregate data based on user input
# #         aggs = client.get_aggs(
# #             ticker=ticker,
# #             multiplier=multiplier,
# #             timespan=timespan,
# #             from_=from_date.strftime('%Y-%m-%d'),
# #             to=to_date.strftime('%Y-%m-%d')
# #         )
# #         df = pd.DataFrame(aggs)
# #
# #         # Download data using yfinance for visualization
# #         stock = yf.Ticker(ticker)
# #         data = stock.history(start=from_date, end=to_date)
# #
# #         # Fetch financial data
# #         income_statement = stock.financials
# #         cash_flow = stock.cashflow
# #         balance_sheet = stock.balance_sheet  # Fetch balance sheet
# #
# #         return df, data, income_statement, cash_flow, balance_sheet
# #
# #     except Exception as e:
# #         st.error(f"An error occurred: {e}")
# #         return pd.DataFrame(), pd.DataFrame(), pd.DataFrame(), pd.DataFrame(), pd.DataFrame()
# #
# #
# # # Fetch the data
# # df, data, income_statement, cash_flow, balance_sheet = fetch_data()
# #
# # # Create tabs for different sections
# # tab1, tab2, tab3 = st.tabs(["Stock Data", "Financial Statements", "Stock Analysis"])
# #
# # # Tab 1: Stock Data
# # with tab1:
# #     st.header("Stock Data")
# #     if not data.empty:
# #         fig = px.line(data, x=data.index, y='Close', title=f"{ticker} Stock Prices",
# #                       line_shape='linear',
# #                       color_discrete_sequence=['#5AB834'])
# #         st.plotly_chart(fig)
# #     else:
# #         st.error("No data available for the selected ticker.")
# #
# #     if df.empty:
# #         st.error("No data available for the selected parameters. Please try different inputs.")
# #     else:
# #         df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
# #         st.dataframe(df)
# #
# #         # Download button for Excel file
# #         output_filename = f"{ticker}_stock_data_{from_date}_to_{to_date}.xlsx"
# #         df.to_excel(output_filename, index=False)
# #         st.success(f"Data fetched successfully and saved to '{output_filename}'.")
# #         st.download_button(label="Download Excel File", data=open(output_filename, 'rb').read(),
# #                            file_name=output_filename)
# #
# # # Tab 2: Financial Statements
# # with tab2:
# #     st.header("Financial Statements")
# #
# #     # Display Income Statement and Cash Flow
# #     if not income_statement.empty:
# #         st.subheader("Income Statement")
# #         st.dataframe(income_statement)
# #         # Download button for Income Statement
# #         income_output_filename = f"{ticker}_income_statement.xlsx"
# #         income_statement.to_excel(income_output_filename)
# #         st.download_button(label="Download Income Statement", data=open(income_output_filename, 'rb').read(),
# #                            file_name=income_output_filename)
# #     else:
# #         st.error("No income statement data available.")
# #
# #     if not cash_flow.empty:
# #         st.subheader("Cash Flow Statement")
# #         st.dataframe(cash_flow)
# #         # Download button for Cash Flow
# #         cash_flow_output_filename = f"{ticker}_cash_flow.xlsx"
# #         cash_flow.to_excel(cash_flow_output_filename)
# #         st.download_button(label="Download Cash Flow Statement", data=open(cash_flow_output_filename, 'rb').read(),
# #                            file_name=cash_flow_output_filename)
# #     else:
# #         st.error("No cash flow data available.")
# #
# #     # Display Balance Sheet
# #     if not balance_sheet.empty:
# #         st.subheader("Balance Sheet")
# #         st.dataframe(balance_sheet)
# #         # Download button for Balance Sheet
# #         balance_sheet_output_filename = f"{ticker}_balance_sheet.xlsx"
# #         balance_sheet.to_excel(balance_sheet_output_filename)
# #         st.download_button(label="Download Balance Sheet", data=open(balance_sheet_output_filename, 'rb').read(),
# #                            file_name=balance_sheet_output_filename)
# #     else:
# #         st.error("No balance sheet data available.")
# #
# # # Import necessary libraries
# # import numpy as np
# #
# # # Tab 3: Stock Analysis
# # with tab3:
# #     st.header("Stock Analysis")
# #     st.write("Analyzing stock movements around earnings dates...")
# #
# #     # Check if data is available
# #     if not data.empty:
# #         # Ensure the 'Date' column is a datetime object
# #         data.index = pd.to_datetime(data.index)
# #
# #         # Split date and time into separate columns
# #         data['Date'] = data.index.date
# #         data['Time'] = data.index.time
# #
# #         # Get actual earnings dates using yfinance
# #         stock_info = yf.Ticker(ticker)
# #         earnings_dates = stock_info.earnings_dates.index
# #
# #         if len(earnings_dates) > 0:
# #             st.write("Earnings Dates:", earnings_dates)
# #
# #             # Analyze gap ups after earnings
# #             gap_up_days = []
# #             profit_loss_data = []
# #
# #             for earnings_date in earnings_dates:
# #                 if earnings_date in data['Date'].values:
# #                     day_after_earnings = earnings_date + pd.Timedelta(days=1)
# #                     if day_after_earnings in data['Date'].values:
# #                         previous_close = data.loc[data['Date'] == earnings_date, 'Close'].iloc[-1]
# #                         day_after_data = data[data['Date'] == day_after_earnings]
# #
# #                         # Check for gap up
# #                         if not day_after_data.empty and day_after_data['Open'].iloc[0] > previous_close:
# #                             gap_up_days.append(day_after_earnings)
# #                             st.write(f"Gap Up detected on: {day_after_earnings}")
# #
# #                             # Calculate Profit or Loss based on Open/Close
# #                             open_close_profit_loss = day_after_data['Close'].iloc[-1] - day_after_data['Open'].iloc[0]
# #
# #                             # Calculate Profit or Loss based on High/Low
# #                             high_low_profit_loss = day_after_data['High'].max() - day_after_data['Low'].min()
# #
# #                             # Append to profit_loss_data list
# #                             profit_loss_data.append({
# #                                 'Date': day_after_earnings,
# #                                 'Open/Close Profit/Loss': open_close_profit_loss,
# #                                 'High/Low Profit/Loss': high_low_profit_loss
# #                             })
# #
# #             # Convert profit_loss_data to a DataFrame and display it
# #             profit_loss_df = pd.DataFrame(profit_loss_data)
# #             st.write("Profit/Loss Analysis:")
# #             st.dataframe(profit_loss_df)
# #
# #         else:
# #             st.write("No earnings dates available for the selected ticker.")
# #
# #     else:
# #         st.write("No data available for stock analysis.")
# #
# # # Footer text
# # st.markdown('<div class="footer">Powered by Naf-Byte (Nafay Ur Rehman)</div>', unsafe_allow_html=True)

# # import streamlit as st
# # from polygon import RESTClient
# # import pandas as pd
# # import plotly.express as px
# # import yfinance as yf
# #
# # # Initialize the Polygon REST client
# # API_KEY = 'y6LU1NRQtO2ogTHRIcMMxQoI2whgMPeG'  # Replace with your actual API key
# # client = RESTClient(API_KEY)
# #
# # # Set page configuration
# # st.set_page_config(page_title="Naf-YFinance - Stock Data Fetcher", layout="wide", page_icon="📈")
# #
# # # Custom CSS for a modern UI with black background
# # st.markdown(
# #     """
# #     <style>
# #     .main {
# #         background-color: #000000;
# #         padding: 20px;
# #         border-radius: 10px;
# #         box-shadow: 0px 0px 15px rgba(0, 0, 0, 0.1);
# #         font-family: 'Arial', sans-serif;
# #         color: #FFFFFF;
# #         text-align: center;
# #     }
# #     .stButton>button {
# #         background-color: #5A189A;
# #         color: #FFFFFF;
# #         font-size: 16px;
# #         padding: 10px 20px;
# #         border: none;
# #         border-radius: 5px;
# #         cursor: pointer;
# #     }
# #     .stButton>button:hover {
# #         background-color: #9D4EDD;
# #     }
# #     .stTextInput>div>div>input {
# #         background-color: #E5E5E5;
# #         color: #333333;
# #         border: 1px solid #CCCCCC;
# #         border-radius: 5px;
# #         padding: 10px;
# #     }
# #     .green-container {
# #         background-color: #DFF2BF;
# #         padding: 10px;
# #         border-radius: 5px;
# #         color: #4F8A10;
# #         font-weight: bold;
# #         margin-bottom: 15px;
# #     }
# #     h1 {
# #         font-size: 28px;
# #         margin-bottom: 10px;
# #         margin-top: 0;  /* Removed extra padding from top */
# #     }
# #     .tagline {
# #         font-size: 18px;
# #         color: #DDDDDD;
# #         margin-bottom: 10px;
# #     }
# #     .footer {
# #         position: fixed;
# #         bottom: 0;
# #         width: 100%;
# #         text-align: center;
# #         color: #DDDDDD;
# #         padding: 10px;
# #         font-size: 14px;
# #     }
# #     </style>
# #     """, unsafe_allow_html=True
# # )
# #
# # # App Title and Tagline
# # st.markdown("<h1>Naf-YFinance - Stock Data Fetcher 📈</h1>", unsafe_allow_html=True)
# # st.markdown('<p class="tagline">Download data from any stock company from symbol</p>', unsafe_allow_html=True)
# #
# # # Sidebar for User Input
# # st.sidebar.header("User Input")
# # ticker = st.sidebar.text_input("Enter Ticker Symbol (e.g., AAPL):", value="AAPL").upper()
# # multiplier = st.sidebar.number_input("Enter Multiplier (e.g., 1 for minute data):", min_value=1, value=1)
# # timespan = st.sidebar.selectbox("Select Timespan:",
# #                                 options=["second", "minute", "hour", "day", "week", "month", "quarter", "year"],
# #                                 index=0)
# # from_date = st.sidebar.date_input("Start Date:", value=pd.to_datetime("2014-01-01"))
# # to_date = st.sidebar.date_input("End Date:", value=pd.to_datetime("2024-01-01"))
# #
# #
# # # Function to fetch stock data and financials
# # def fetch_data():
# #     try:
# #         # Fetch aggregate data based on user input
# #         aggs = client.get_aggs(
# #             ticker=ticker,
# #             multiplier=multiplier,
# #             timespan=timespan,
# #             from_=from_date.strftime('%Y-%m-%d'),
# #             to=to_date.strftime('%Y-%m-%d')
# #         )
# #         df = pd.DataFrame(aggs)
# #
# #         # Download data using yfinance for visualization
# #         stock = yf.Ticker(ticker)
# #         data = stock.history(start=from_date, end=to_date)
# #
# #         # Fetch financial data
# #         income_statement = stock.financials
# #         cash_flow = stock.cashflow
# #         balance_sheet = stock.balance_sheet  # Fetch balance sheet
# #
# #         return df, data, income_statement, cash_flow, balance_sheet
# #
# #     except Exception as e:
# #         st.error(f"An error occurred: {e}")
# #         return pd.DataFrame(), pd.DataFrame(), pd.DataFrame(), pd.DataFrame(), pd.DataFrame()
# #
# #
# # # Fetch the data
# # df, data, income_statement, cash_flow, balance_sheet = fetch_data()
# #
# # # Create tabs for different sections
# # tab1, tab2, tab3 = st.tabs(["Stock Data", "Financial Statements", "Stock Analysis"])
# #
# # # Tab 1: Stock Data
# # with tab1:
# #     st.header("Stock Data")
# #     if not data.empty:
# #         fig = px.line(data, x=data.index, y='Close', title=f"{ticker} Stock Prices",
# #                       line_shape='linear',
# #                       color_discrete_sequence=['#5AB834'])
# #         st.plotly_chart(fig)
# #     else:
# #         st.error("No data available for the selected ticker.")
# #
# #     if df.empty:
# #         st.error("No data available for the selected parameters. Please try different inputs.")
# #     else:
# #         df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
# #         st.dataframe(df)
# #
# #         # Download button for Excel file
# #         output_filename = f"{ticker}_stock_data_{from_date}_to_{to_date}.xlsx"
# #         df.to_excel(output_filename, index=False)
# #         st.success(f"Data fetched successfully and saved to '{output_filename}'.")
# #         st.download_button(label="Download Excel File", data=open(output_filename, 'rb').read(),
# #                            file_name=output_filename)
# #
# # # Tab 2: Financial Statements
# # with tab2:
# #     st.header("Financial Statements")
# #
# #     # Display Income Statement and Cash Flow
# #     if not income_statement.empty:
# #         st.subheader("Income Statement")
# #         st.dataframe(income_statement)
# #         # Download button for Income Statement
# #         income_output_filename = f"{ticker}_income_statement.xlsx"
# #         income_statement.to_excel(income_output_filename)
# #         st.download_button(label="Download Income Statement", data=open(income_output_filename, 'rb').read(),
# #                            file_name=income_output_filename)
# #     else:
# #         st.error("No income statement data available.")
# #
# #     if not cash_flow.empty:
# #         st.subheader("Cash Flow Statement")
# #         st.dataframe(cash_flow)
# #         # Download button for Cash Flow
# #         cash_flow_output_filename = f"{ticker}_cash_flow.xlsx"
# #         cash_flow.to_excel(cash_flow_output_filename)
# #         st.download_button(label="Download Cash Flow Statement", data=open(cash_flow_output_filename, 'rb').read(),
# #                            file_name=cash_flow_output_filename)
# #     else:
# #         st.error("No cash flow data available.")
# #
# #     # Display Balance Sheet
# #     if not balance_sheet.empty:
# #         st.subheader("Balance Sheet")
# #         st.dataframe(balance_sheet)
# #         # Download button for Balance Sheet
# #         balance_sheet_output_filename = f"{ticker}_balance_sheet.xlsx"
# #         balance_sheet.to_excel(balance_sheet_output_filename)
# #         st.download_button(label="Download Balance Sheet", data=open(balance_sheet_output_filename, 'rb').read(),
# #                            file_name=balance_sheet_output_filename)
# #     else:
# #         st.error("No balance sheet data available.")
# #
# # # Import necessary libraries
# # import numpy as np
# #
# # # Tab 3: Stock Analysis
# # with tab3:
# #     st.header("Stock Analysis")
# #     st.write("Analyzing stock movements around earnings dates...")
# #
# #     # Check if data is available
# #     if not data.empty:
# #         # Ensure the 'Date' column is a datetime object
# #         data.index = pd.to_datetime(data.index)
# #
# #         # Split date and time into separate columns
# #         data['Date'] = data.index.date
# #         data['Time'] = data.index.time
# #
# #         # Display the High and Low price charts
# #         st.subheader("High and Low Price Analysis")
# #
# #         # Plot High Prices
# #         fig_high = px.line(data, x=data.index, y='High', title=f"{ticker} High Prices Over Time",
# #                            line_shape='linear', color_discrete_sequence=['#F39C12'])
# #         st.plotly_chart(fig_high)
# #
# #         # Plot Low Prices
# #         fig_low = px.line(data, x=data.index, y='Low', title=f"{ticker} Low Prices Over Time",
# #                           line_shape='linear', color_discrete_sequence=['#2980B9'])
# #         st.plotly_chart(fig_low)
# #
# #         # Get actual earnings dates using yfinance
# #         stock_info = yf.Ticker(ticker)
# #         earnings_dates = stock_info.earnings_dates.index
# #
# #         if len(earnings_dates) > 0:
# #             st.write("Earnings Dates:", earnings_dates)
# #
# #             # Analyze gap ups after earnings
# #             gap_up_days = []
# #             profit_loss_data = []
# #
# #             for earnings_date in earnings_dates:
# #                 if earnings_date in data['Date'].values:
# #                     day_after_earnings = earnings_date + pd.Timedelta(days=1)
# #                     if day_after_earnings in data['Date'].values:
# #                         previous_close = data.loc[data['Date'] == earnings_date, 'Close'].iloc[-1]
# #                         day_after_data = data[data['Date'] == day_after_earnings]
# #
# #                         # Check for gap up
# #                         if not day_after_data.empty and day_after_data['Open'].iloc[0] > previous_close:
# #                             gap_up_days.append(day_after_earnings)
# #                             st.write(f"Gap Up detected on: {day_after_earnings}")
# #
# #                             # Calculate Profit or Loss based on Open/Close
# #                             open_close_profit_loss = day_after_data['Close'].iloc[-1] - day_after_data['Open'].iloc[0]
# #
# #                             # Calculate Profit or Loss based on High/Low
# #                             high_low_profit_loss = day_after_data['High'].max() - day_after_data['Low'].min()
# #
# #                             # Append to profit_loss_data list
# #                             profit_loss_data.append({
# #                                 'Date': day_after_earnings,
# #                                 'Open-Close P/L': open_close_profit_loss,
# #                                 'High-Low P/L': high_low_profit_loss
# #                             })
# #
# #             # Convert profit_loss_data to DataFrame for visualization
# #             profit_loss_df = pd.DataFrame(profit_loss_data)
# #
# #             # Display the Profit and Loss Graph
# #             if not profit_loss_df.empty:
# #                 st.write("Profit and Loss Analysis for Gap-Up Days")
# #
# #                 # Plot Profit and Loss Graph
# #                 fig1 = px.line(profit_loss_df, x='Date', y='Open-Close P/L',
# #                                title="Open-Close Profit/Loss on Gap-Up Days",
# #                                line_shape='linear',
# #                                color_discrete_sequence=['red'])
# #                 st.plotly_chart(fig1)
# #
# #                 # Plot High and Low Gap Graph
# #                 fig2 = px.line(profit_loss_df, x='Date', y='High-Low P/L',
# #                                title="High-Low Gap on Gap-Up Days",
# #                                line_shape='linear',
# #                                color_discrete_sequence=['red'])
# #                 st.plotly_chart(fig2)
# #             else:
# #                 st.info("No profit/loss data available for gap-up days.")
# #
# #             # Calculate statistics for gap-up days
# #             lower_close_count = 0
# #             higher_close_count = 0
# #
# #             for day in gap_up_days:
# #                 day_data = data[data['Date'] == day]
# #                 previous_close = data.loc[data['Date'] == (day - pd.Timedelta(days=1)), 'Close'].iloc[-1]
# #
# #                 # Check for closing lower than previous day's close
# #                 if day_data['Close'].iloc[-1] < previous_close:
# #                     lower_close_count += 1
# #
# #                 # Check for closing higher than opening price
# #                 if day_data['Close'].iloc[-1] > day_data['Open'].iloc[0]:
# #                     higher_close_count += 1
# #
# #             # Display the results
# #             st.write(f"Number of times stock closed lower than the previous day's close after a gap up: {lower_close_count}")
# #             st.write(f"Number of times stock closed higher than its opening price after a gap up: {higher_close_count}")
# #
# #             # Calculate the reversal percentages
# #             if len(gap_up_days) > 0:
# #                 lower_close_percentage = (lower_close_count / len(gap_up_days)) * 100
# #                 higher_close_percentage = (higher_close_count / len(gap_up_days)) * 100
# #
# #                 st.write(f"Percentage of gap-ups that closed lower: {lower_close_percentage:.2f}%")
# #                 st.write(f"Percentage of gap-ups that closed higher: {higher_close_percentage:.2f}%")
# #             else:
# #                 st.info("No gap-ups detected after earnings during the selected period.")
# #         else:
# #             st.error("No earnings dates found for this ticker.")
# #     else:
# #         st.error("Not enough stock data available for analysis.")
# #
# # # Footer text
# # st.markdown('<div class="footer">Powered by Naf-Byte (Nafay Ur Rehman)</div>', unsafe_allow_html=True)
# # import streamlit as st
# # from polygon import RESTClient
# # import pandas as pd
# # import plotly.graph_objects as go
# # import yfinance as yf
# #
# # # Initialize the Polygon REST client
# # API_KEY = 'y6LU1NRQtO2ogTHRIcMMxQoI2whgMPeG'  # Replace with your actual API key
# # client = RESTClient(API_KEY)
# #
# # # Set page configuration
# # st.set_page_config(page_title="Naf-YFinance - Stock Data Fetcher", layout="wide", page_icon="📈")
# #
# # # Custom CSS for a modern UI with black background
# # st.markdown(
# #     """
# #     <style>
# #     .main {
# #         background-color: #000000;
# #         padding: 20px;
# #         border-radius: 10px;
# #         box-shadow: 0px 0px 15px rgba(0, 0, 0, 0.1);
# #         font-family: 'Arial', sans-serif;
# #         color: #FFFFFF;
# #         text-align: center;
# #     }
# #     .stButton>button {
# #         background-color: #5A189A;
# #         color: #FFFFFF;
# #         font-size: 16px;
# #         padding: 10px 20px;
# #         border: none;
# #         border-radius: 5px;
# #         cursor: pointer;
# #     }
# #     .stButton>button:hover {
# #         background-color: #9D4EDD;
# #     }
# #     .stTextInput>div>div>input {
# #         background-color: #E5E5E5;
# #         color: #333333;
# #         border: 1px solid #CCCCCC;
# #         border-radius: 5px;
# #         padding: 10px;
# #     }
# #     .green-container {
# #         background-color: #DFF2BF;
# #         padding: 10px;
# #         border-radius: 5px;
# #         color: #4F8A10;
# #         font-weight: bold;
# #         margin-bottom: 15px;
# #     }
# #     h1 {
# #         font-size: 28px;
# #         margin-bottom: 10px;
# #         margin-top: 0;  /* Removed extra padding from top */
# #     }
# #     .tagline {
# #         font-size: 18px;
# #         color: #DDDDDD;
# #         margin-bottom: 10px;
# #     }
# #     .footer {
# #         position: fixed;
# #         bottom: 0;
# #         width: 100%;
# #         text-align: center;
# #         color: #DDDDDD;
# #         padding: 10px;
# #         font-size: 14px;
# #     }
# #     </style>
# #     """, unsafe_allow_html=True
# # )
# #
# # # App Title and Tagline
# # st.markdown("<h1>Naf-YFinance - Stock Data Fetcher 📈</h1>", unsafe_allow_html=True)
# # st.markdown('<p class="tagline">Download data from any stock company from symbol</p>', unsafe_allow_html=True)
# #
# # # Sidebar for User Input
# # st.sidebar.header("User Input")
# # ticker = st.sidebar.text_input("Enter Ticker Symbol (e.g., AAPL):", value="AAPL").upper()
# # multiplier = st.sidebar.number_input("Enter Multiplier (e.g., 1 for minute data):", min_value=1, value=1)
# # timespan = st.sidebar.selectbox("Select Timespan:",
# #                                 options=["second", "minute", "hour", "day", "week", "month", "quarter", "year"],
# #                                 index=0)
# # from_date = st.sidebar.date_input("Start Date:", value=pd.to_datetime("2014-01-01"))
# # to_date = st.sidebar.date_input("End Date:", value=pd.to_datetime("2024-01-01"))
# #
# #
# # # Function to fetch stock data and financials
# # def fetch_data():
# #     try:
# #         # Fetch aggregate data based on user input
# #         aggs = client.get_aggs(
# #             ticker=ticker,
# #             multiplier=multiplier,
# #             timespan=timespan,
# #             from_=from_date.strftime('%Y-%m-%d'),
# #             to=to_date.strftime('%Y-%m-%d')
# #         )
# #         df = pd.DataFrame(aggs)
# #
# #         # Download data using yfinance for visualization
# #         stock = yf.Ticker(ticker)
# #         data = stock.history(start=from_date, end=to_date)
# #
# #         # Fetch financial data
# #         income_statement = stock.financials
# #         cash_flow = stock.cashflow
# #         balance_sheet = stock.balance_sheet  # Fetch balance sheet
# #
# #         return df, data, income_statement, cash_flow, balance_sheet
# #
# #     except Exception as e:
# #         st.error(f"An error occurred: {e}")
# #         return pd.DataFrame(), pd.DataFrame(), pd.DataFrame(), pd.DataFrame(), pd.DataFrame()
# #
# #
# # # Fetch the data
# # df, data, income_statement, cash_flow, balance_sheet = fetch_data()
# #
# # # Create tabs for different sections
# # tab1, tab2, tab3 = st.tabs(["Stock Data", "Financial Statements", "Stock Analysis"])
# #
# # # Tab 1: Stock Data
# # with tab1:
# #     st.header("Stock Data")
# #     if not data.empty:
# #         fig = go.Figure()
# #
# #         # Add High Prices line
# #         fig.add_trace(
# #             go.Scatter(x=data.index, y=data['High'], mode='lines', name='High Prices', line=dict(color='green')))
# #
# #         # Add Low Prices line
# #         fig.add_trace(go.Scatter(x=data.index, y=data['Low'], mode='lines', name='Low Prices', line=dict(color='red')))
# #
# #         fig.update_layout(title=f"{ticker} High and Low Stock Prices", xaxis_title="Date", yaxis_title="Price")
# #         st.plotly_chart(fig)
# #     else:
# #         st.error("No data available for the selected ticker.")
# #
# #     if df.empty:
# #         st.error("No data available for the selected parameters. Please try different inputs.")
# #     else:
# #         df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
# #         st.dataframe(df)
# #
# #         # Download button for Excel file
# #         output_filename = f"{ticker}_stock_data_{from_date}_to_{to_date}.xlsx"
# #         df.to_excel(output_filename, index=False)
# #         st.success(f"Data fetched successfully and saved to '{output_filename}'.")
# #         st.download_button(label="Download Excel File", data=open(output_filename, 'rb').read(),
# #                            file_name=output_filename)
# #
# # # Tab 2: Financial Statements
# # with tab2:
# #     st.header("Financial Statements")
# #
# #     # Display Income Statement and Cash Flow
# #     if not income_statement.empty:
# #         st.subheader("Income Statement")
# #         st.dataframe(income_statement)
# #         # Download button for Income Statement
# #         income_output_filename = f"{ticker}_income_statement.xlsx"
# #         income_statement.to_excel(income_output_filename)
# #         st.download_button(label="Download Income Statement", data=open(income_output_filename, 'rb').read(),
# #                            file_name=income_output_filename)
# #     else:
# #         st.error("No income statement data available.")
# #
# #     if not cash_flow.empty:
# #         st.subheader("Cash Flow Statement")
# #         st.dataframe(cash_flow)
# #         # Download button for Cash Flow
# #         cash_flow_output_filename = f"{ticker}_cash_flow.xlsx"
# #         cash_flow.to_excel(cash_flow_output_filename)
# #         st.download_button(label="Download Cash Flow Statement", data=open(cash_flow_output_filename, 'rb').read(),
# #                            file_name=cash_flow_output_filename)
# #     else:
# #         st.error("No cash flow data available.")
# #
# #     # Display Balance Sheet
# #     if not balance_sheet.empty:
# #         st.subheader("Balance Sheet")
# #         st.dataframe(balance_sheet)
# #         # Download button for Balance Sheet
# #         balance_sheet_output_filename = f"{ticker}_balance_sheet.xlsx"
# #         balance_sheet.to_excel(balance_sheet_output_filename)
# #         st.download_button(label="Download Balance Sheet", data=open(balance_sheet_output_filename, 'rb').read(),
# #                            file_name=balance_sheet_output_filename)
# #     else:
# #         st.error("No balance sheet data available.")
# #
# # # Tab 3: Stock Analysis
# # with tab3:
# #     st.header("Stock Analysis")
# #     st.write("Analyzing stock movements around earnings dates...")
# #
# #     # Check if data is available
# #     if not data.empty:
# #         # Ensure the 'Date' column is a datetime object
# #         data.index = pd.to_datetime(data.index)
# #
# #         # Split date and time into separate columns
# #         data['Date'] = data.index.date
# #         data['Time'] = data.index.time
# #
# #         # Display the High and Low price charts
# #         st.subheader("High and Low Price Analysis")
# #
# #         # Combine High and Low Prices in one chart
# #         fig_combined = go.Figure()
# #         fig_combined.add_trace(
# #             go.Scatter(x=data.index, y=data['High'], mode='lines', name='High', line=dict(color='green')))
# #         fig_combined.add_trace(
# #             go.Scatter(x=data.index, y=data['Low'], mode='lines', name='Low', line=dict(color='red')))
# #         fig_combined.update_layout(title=f"{ticker} High and Low Stock Prices", xaxis_title="Date", yaxis_title="Price")
# #         st.plotly_chart(fig_combined)
# #
# #         # Other analysis code here...
# #         # (Rest of your tab3 code)

# # import streamlit as st
# # from polygon import RESTClient
# # import pandas as pd
# # import plotly.graph_objects as go
# # import yfinance as yf
# #
# # # Initialize the Polygon REST client
# # API_KEY = 'y6LU1NRQtO2ogTHRIcMMxQoI2whgMPeG'  # Replace with your actual API key
# # client = RESTClient(API_KEY)
# #
# # # Set page configuration
# # st.set_page_config(page_title="Naf-YFinance - Stock Data Fetcher", layout="wide", page_icon="📈")
# #
# # # Custom CSS for a modern UI with black background
# # st.markdown(
# #     """
# #     <style>
# #     .main {
# #         background-color: #000000;
# #         padding: 20px;
# #         border-radius: 10px;
# #         box-shadow: 0px 0px 15px rgba(0, 0, 0, 0.1);
# #         font-family: 'Arial', sans-serif;
# #         color: #FFFFFF;
# #         text-align: center;
# #     }
# #     .stButton>button {
# #         background-color: #5A189A;
# #         color: #FFFFFF;
# #         font-size: 16px;
# #         padding: 10px 20px;
# #         border: none;
# #         border-radius: 5px;
# #         cursor: pointer;
# #     }
# #     .stButton>button:hover {
# #         background-color: #9D4EDD;
# #     }
# #     .stTextInput>div>div>input {
# #         background-color: #E5E5E5;
# #         color: #333333;
# #         border: 1px solid #CCCCCC;
# #         border-radius: 5px;
# #         padding: 10px;
# #     }
# #     .green-container {
# #         background-color: #DFF2BF;
# #         padding: 10px;
# #         border-radius: 5px;
# #         color: #4F8A10;
# #         font-weight: bold;
# #         margin-bottom: 15px;
# #     }
# #     h1 {
# #         font-size: 28px;
# #         margin-bottom: 10px;
# #         margin-top: 0;  /* Removed extra padding from top */
# #     }
# #     .tagline {
# #         font-size: 18px;
# #         color: #DDDDDD;
# #         margin-bottom: 10px;
# #     }
# #     .footer {
# #         position: fixed;
# #         bottom: 0;
# #         width: 100%;
# #         text-align: center;
# #         color: #DDDDDD;
# #         padding: 10px;
# #         font-size: 14px;
# #     }
# #     </style>
# #     """, unsafe_allow_html=True
# # )
# #
# # # App Title and Tagline
# # st.markdown("<h1>Naf-YFinance - Stock Data Fetcher 📈</h1>", unsafe_allow_html=True)
# # st.markdown('<p class="tagline">Download data from any stock company from symbol</p>', unsafe_allow_html=True)
# #
# # # Sidebar for User Input
# # st.sidebar.header("User Input")
# # ticker = st.sidebar.text_input("Enter Ticker Symbol (e.g., AAPL):", value="AAPL").upper()
# # multiplier = st.sidebar.number_input("Enter Multiplier (e.g., 1 for minute data):", min_value=1, value=1)
# # timespan = st.sidebar.selectbox("Select Timespan:",
# #                                 options=["second", "minute", "hour", "day", "week", "month", "quarter", "year"],
# #                                 index=0)
# # from_date = st.sidebar.date_input("Start Date:", value=pd.to_datetime("2014-01-01"))
# # to_date = st.sidebar.date_input("End Date:", value=pd.to_datetime("2024-01-01"))
# #
# #
# # # Function to fetch stock data and financials
# # def fetch_data():
# #     try:
# #         # Fetch aggregate data based on user input
# #         aggs = client.get_aggs(
# #             ticker=ticker,
# #             multiplier=multiplier,
# #             timespan=timespan,
# #             from_=from_date.strftime('%Y-%m-%d'),
# #             to=to_date.strftime('%Y-%m-%d')
# #         )
# #         df = pd.DataFrame(aggs)
# #
# #         # Download data using yfinance for visualization
# #         stock = yf.Ticker(ticker)
# #         data = stock.history(start=from_date, end=to_date)
# #
# #         # Fetch financial data
# #         income_statement = stock.financials
# #         cash_flow = stock.cashflow
# #         balance_sheet = stock.balance_sheet  # Fetch balance sheet
# #
# #         return df, data, income_statement, cash_flow, balance_sheet
# #
# #     except Exception as e:
# #         st.error(f"An error occurred: {e}")
# #         return pd.DataFrame(), pd.DataFrame(), pd.DataFrame(), pd.DataFrame(), pd.DataFrame()
# #
# #
# # # Fetch the data
# # df, data, income_statement, cash_flow, balance_sheet = fetch_data()
# #
# # # Create tabs for different sections
# # tab1, tab2, tab3 = st.tabs(["Stock Data", "Financial Statements", "Stock Analysis"])
# #
# # # Tab 1: Stock Data
# # with tab1:
# #     st.header("Stock Data")
# #     if not data.empty:
# #         fig = go.Figure()
# #
# #         # Add High Prices line
# #         fig.add_trace(
# #             go.Scatter(x=data.index, y=data['High'], mode='lines', name='High Prices', line=dict(color='green')))
# #
# #         # Add Low Prices line
# #         fig.add_trace(go.Scatter(x=data.index, y=data['Low'], mode='lines', name='Low Prices', line=dict(color='red')))
# #
# #         fig.update_layout(title=f"{ticker} High and Low Stock Prices", xaxis_title="Date", yaxis_title="Price")
# #         st.plotly_chart(fig)
# #     else:
# #         st.error("No data available for the selected ticker.")
# #
# #     if df.empty:
# #         st.error("No data available for the selected parameters. Please try different inputs.")
# #     else:
# #         df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
# #         st.dataframe(df)
# #
# #         # Download button for Excel file
# #         output_filename = f"{ticker}_stock_data_{from_date}_to_{to_date}.xlsx"
# #         df.to_excel(output_filename, index=False)
# #         st.success(f"Data fetched successfully and saved to '{output_filename}'.")
# #         st.download_button(label="Download Excel File", data=open(output_filename, 'rb').read(),
# #                            file_name=output_filename)
# #
# # # Tab 2: Financial Statements
# # with tab2:
# #     st.header("Financial Statements")
# #
# #     # Display Income Statement and Cash Flow
# #     if not income_statement.empty:
# #         st.subheader("Income Statement")
# #         st.dataframe(income_statement)
# #         # Download button for Income Statement
# #         income_output_filename = f"{ticker}_income_statement.xlsx"
# #         income_statement.to_excel(income_output_filename)
# #         st.download_button(label="Download Income Statement", data=open(income_output_filename, 'rb').read(),
# #                            file_name=income_output_filename)
# #     else:
# #         st.error("No income statement data available.")
# #
# #     if not cash_flow.empty:
# #         st.subheader("Cash Flow Statement")
# #         st.dataframe(cash_flow)
# #         # Download button for Cash Flow
# #         cash_flow_output_filename = f"{ticker}_cash_flow.xlsx"
# #         cash_flow.to_excel(cash_flow_output_filename)
# #         st.download_button(label="Download Cash Flow Statement", data=open(cash_flow_output_filename, 'rb').read(),
# #                            file_name=cash_flow_output_filename)
# #     else:
# #         st.error("No cash flow data available.")
# #
# #     # Display Balance Sheet
# #     if not balance_sheet.empty:
# #         st.subheader("Balance Sheet")
# #         st.dataframe(balance_sheet)
# #         # Download button for Balance Sheet
# #         balance_sheet_output_filename = f"{ticker}_balance_sheet.xlsx"
# #         balance_sheet.to_excel(balance_sheet_output_filename)
# #         st.download_button(label="Download Balance Sheet", data=open(balance_sheet_output_filename, 'rb').read(),
# #                            file_name=balance_sheet_output_filename)
# #     else:
# #         st.error("No balance sheet data available.")
# #
# # # Tab 3: Stock Analysis
# # with tab3:
# #     st.header("Stock Analysis")
# #     st.write("Analyzing stock movements around earnings dates...")
# #
# #     # Check if data is available
# #     if not data.empty:
# #         # Ensure the 'Date' column is a datetime object
# #         data.index = pd.to_datetime(data.index)
# #
# #         # Split date and time into separate columns
# #         data['Date'] = data.index.date
# #         data['Time'] = data.index.time
# #
# #         # Display the High and Low price charts
# #         st.subheader("High and Low Price Analysis")
# #
# #         # Combine High and Low Prices in one chart
# #         fig_combined = go.Figure()
# #         fig_combined.add_trace(
# #             go.Scatter(x=data.index, y=data['High'], mode='lines', name='High', line=dict(color='green')))
# #         fig_combined.add_trace(
# #             go.Scatter(x=data.index, y=data['Low'], mode='lines', name='Low', line=dict(color='red')))
# #         fig_combined.update_layout(title=f"{ticker} High and Low Stock Prices", xaxis_title="Date", yaxis_title="Price")
# #         st.plotly_chart(fig_combined)
# #
# #         # Calculate Highest Opening and Lowest Closing
# #         highest_opening = data['Open'].max()
# #         lowest_closing = data['Close'].min()
# #
# #         # Display the highest opening and lowest closing prices
# #         st.subheader("Highest Opening and Lowest Closing Prices")
# #         st.write(f"Highest Opening Price: {highest_opening:.2f}")
# #         st.write(f"Lowest Closing Price: {lowest_closing:.2f}")
# #
# #         # Create a bar chart for highest opening and lowest closing prices
# #         fig_analysis = go.Figure()
# #         fig_analysis.add_trace(go.Bar(x=['Highest Opening', 'Lowest Closing'],
# #                                       y=[highest_opening, lowest_closing],
# #                                       marker_color=['blue', 'red']))
# #         fig_analysis.update_layout(title="Highest Opening and Lowest Closing Prices",
# #                                    xaxis_title="Type",
# #                                    yaxis_title="Price",
# #                                    xaxis=dict(tickvals=[0, 1], ticktext=['Highest Opening', 'Lowest Closing']))
# #
# #         st.plotly_chart(fig_analysis)
# # import streamlit as st
# # from polygon import RESTClient
# # import pandas as pd
# # import plotly.graph_objects as go
# # import yfinance as yf
# #
# # # Initialize the Polygon REST client
# # API_KEY = 'y6LU1NRQtO2ogTHRIcMMxQoI2whgMPeG'  # Replace with your actual API key
# # client = RESTClient(API_KEY)
# #
# # # Set page configuration
# # st.set_page_config(page_title="Naf-YFinance - Stock Data Fetcher", layout="wide", page_icon="📈")
# #
# # # Custom CSS for a modern UI with black background
# # st.markdown(
# #     """
# #     <style>
# #     .main {
# #         background-color: #000000;
# #         padding: 20px;
# #         border-radius: 10px;
# #         box-shadow: 0px 0px 15px rgba(0, 0, 0, 0.1);
# #         font-family: 'Arial', sans-serif;
# #         color: #FFFFFF;
# #         text-align: center;
# #     }
# #     .stButton>button {
# #         background-color: #5A189A;
# #         color: #FFFFFF;
# #         font-size: 16px;
# #         padding: 10px 20px;
# #         border: none;
# #         border-radius: 5px;
# #         cursor: pointer;
# #     }
# #     .stButton>button:hover {
# #         background-color: #9D4EDD;
# #     }
# #     .stTextInput>div>div>input {
# #         background-color: #E5E5E5;
# #         color: #333333;
# #         border: 1px solid #CCCCCC;
# #         border-radius: 5px;
# #         padding: 10px;
# #     }
# #     .green-container {
# #         background-color: #DFF2BF;
# #         padding: 10px;
# #         border-radius: 5px;
# #         color: #4F8A10;
# #         font-weight: bold;
# #         margin-bottom: 15px;
# #     }
# #     h1 {
# #         font-size: 28px;
# #         margin-bottom: 10px;
# #         margin-top: 0;  /* Removed extra padding from top */
# #     }
# #     .tagline {
# #         font-size: 18px;
# #         color: #DDDDDD;
# #         margin-bottom: 10px;
# #     }
# #     .footer {
# #         position: fixed;
# #         bottom: 0;
# #         width: 100%;
# #         text-align: center;
# #         color: #DDDDDD;
# #         padding: 10px;
# #         font-size: 14px;
# #     }
# #     </style>
# #     """, unsafe_allow_html=True
# # )
# #
# # # App Title and Tagline
# # st.markdown("<h1>Naf-YFinance - Stock Data Fetcher 📈</h1>", unsafe_allow_html=True)
# # st.markdown('<p class="tagline">Download data from any stock company from symbol</p>', unsafe_allow_html=True)
# #
# # # Sidebar for User Input
# # st.sidebar.header("User Input")
# # ticker = st.sidebar.text_input("Enter Ticker Symbol (e.g., AAPL):", value="AAPL").upper()
# # multiplier = st.sidebar.number_input("Enter Multiplier (e.g., 1 for minute data):", min_value=1, value=1)
# # timespan = st.sidebar.selectbox("Select Timespan:",
# #                                 options=["second", "minute", "hour", "day", "week", "month", "quarter", "year"],
# #                                 index=0)
# # from_date = st.sidebar.date_input("Start Date:", value=pd.to_datetime("2014-01-01"))
# # to_date = st.sidebar.date_input("End Date:", value=pd.to_datetime("2024-01-01"))
# #
# #
# # @st.cache_data(persist=True)
# # def fetch_data():
# #     try:
# #         # Fetch aggregate data based on user input
# #         aggs = client.get_aggs(
# #             ticker=ticker,
# #             multiplier=multiplier,
# #             timespan=timespan,
# #             from_=from_date.strftime('%Y-%m-%d'),
# #             to=to_date.strftime('%Y-%m-%d')
# #         )
# #         df = pd.DataFrame(aggs)
# #
# #         # Download data using yfinance for visualization
# #         stock = yf.Ticker(ticker)
# #         data = stock.history(start=from_date, end=to_date)
# #
# #         # Fetch financial data
# #         income_statement = stock.financials
# #         cash_flow = stock.cashflow
# #         balance_sheet = stock.balance_sheet  # Fetch balance sheet
# #
# #         return df, data, income_statement, cash_flow, balance_sheet
# #
# #     except Exception as e:
# #         st.error(f"An error occurred: {e}")
# #         return pd.DataFrame(), pd.DataFrame(), pd.DataFrame(), pd.DataFrame(), pd.DataFrame()
# #
# #
# # # Fetch the data
# # df, data, income_statement, cash_flow, balance_sheet = fetch_data()
# #
# # # Create tabs for different sections
# # tab1, tab2, tab3 = st.tabs(["Stock Data", "Financial Statements", "Stock Analysis"])
# #
# # # Tab 1: Stock Data
# # with tab1:
# #     st.header("Stock Data")
# #     if not data.empty:
# #         fig = go.Figure()
# #
# #         # Add High Prices line
# #         fig.add_trace(
# #             go.Scatter(x=data.index, y=data['High'], mode='lines', name='High Prices', line=dict(color='green')))
# #
# #         # Add Low Prices line
# #         fig.add_trace(go.Scatter(x=data.index, y=data['Low'], mode='lines', name='Low Prices', line=dict(color='red')))
# #
# #         fig.update_layout(title=f"{ticker} High and Low Stock Prices", xaxis_title="Date", yaxis_title="Price")
# #         st.plotly_chart(fig)
# #     else:
# #         st.error("No data available for the selected ticker.")
# #
# #     if df.empty:
# #         st.error("No data available for the selected parameters. Please try different inputs.")
# #     else:
# #         df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
# #         st.dataframe(df)
# #
# #         # Download button for Excel file
# #         output_filename = f"{ticker}_stock_data_{from_date}_to_{to_date}.xlsx"
# #         df.to_excel(output_filename, index=False)
# #         st.success(f"Data fetched successfully and saved to '{output_filename}'.")
# #         st.download_button(label="Download Excel File", data=open(output_filename, 'rb').read(),
# #                            file_name=output_filename)
# #
# # # Tab 2: Financial Statements
# # with tab2:
# #     st.header("Financial Statements")
# #
# #     # Display Income Statement and Cash Flow
# #     if not income_statement.empty:
# #         st.subheader("Income Statement")
# #         st.dataframe(income_statement)
# #         # Download button for Income Statement
# #         income_output_filename = f"{ticker}_income_statement.xlsx"
# #         income_statement.to_excel(income_output_filename)
# #         st.download_button(label="Download Income Statement", data=open(income_output_filename, 'rb').read(),
# #                            file_name=income_output_filename)
# #     else:
# #         st.error("No income statement data available.")
# #
# #     if not cash_flow.empty:
# #         st.subheader("Cash Flow Statement")
# #         st.dataframe(cash_flow)
# #         # Download button for Cash Flow
# #         cash_flow_output_filename = f"{ticker}_cash_flow.xlsx"
# #         cash_flow.to_excel(cash_flow_output_filename)
# #         st.download_button(label="Download Cash Flow Statement", data=open(cash_flow_output_filename, 'rb').read(),
# #                            file_name=cash_flow_output_filename)
# #     else:
# #         st.error("No cash flow data available.")
# #
# #     # Display Balance Sheet
# #     if not balance_sheet.empty:
# #         st.subheader("Balance Sheet")
# #         st.dataframe(balance_sheet)
# #         # Download button for Balance Sheet
# #         balance_sheet_output_filename = f"{ticker}_balance_sheet.xlsx"
# #         balance_sheet.to_excel(balance_sheet_output_filename)
# #         st.download_button(label="Download Balance Sheet", data=open(balance_sheet_output_filename, 'rb').read(),
# #                            file_name=balance_sheet_output_filename)
# #     else:
# #         st.error("No balance sheet data available.")
# #
# # # Tab 3: Stock Analysis
# # with tab3:
# #     st.header("Stock Analysis")
# #     st.write("Analyzing stock movements around earnings dates...")
# #
# #     # Check if data is available
# #     if not data.empty:
# #         # Ensure the 'Date' column is a datetime object
# #         data.index = pd.to_datetime(data.index)
# #
# #         # Split date and time into separate columns
# #         data['Date'] = data.index.date
# #         data['Time'] = data.index.time
# #
# #         # Display the High and Low price charts
# #         st.subheader("High and Low Price Analysis")
# #
# #         # Combine High and Low Prices in one chart
# #         fig_combined = go.Figure()
# #         fig_combined.add_trace(
# #             go.Scatter(x=data.index, y=data['High'], mode='lines', name='High', line=dict(color='green')))
# #         fig_combined.add_trace(
# #             go.Scatter(x=data.index, y=data['Low'], mode='lines', name='Low', line=dict(color='red')))
# #         fig_combined.update_layout(title=f"{ticker} High and Low Prices Over Time", xaxis_title="Date",
# #                                    yaxis_title="Price")
# #         st.plotly_chart(fig_combined)
# #
# #         # Calculate highest opening price and lowest closing price
# #         highest_opening = data['Open'].max()
# #         lowest_closing = data['Close'].min()
# #
# #         # Display the highest opening and lowest closing prices
# #         st.write(f"Highest Opening Price: {highest_opening:.2f}")
# #         st.write(f"Lowest Closing Price: {lowest_closing:.2f}")
# #
# #         # Create a bar chart for highest opening and lowest closing prices
# #         fig_analysis = go.Figure()
# #         fig_analysis.add_trace(go.Bar(x=['Highest Opening', 'Lowest Closing'],
# #                                       y=[highest_opening, lowest_closing],
# #                                       marker_color=['blue', 'red']))
# #         fig_analysis.update_layout(title="Highest Opening and Lowest Closing Prices",
# #                                    xaxis_title="Type",
# #                                    yaxis_title="Price",
# #                                    xaxis=dict(tickvals=[0, 1], ticktext=['Highest Opening', 'Lowest Closing']))
# #
# #         st.plotly_chart(fig_analysis)
# #     else:
# #         st.error("No data available for the selected ticker.")
# #
# # # Footer
# # st.markdown('<div class="footer">Powered by Naf-Byte (Nafay Ur Rehman)</div>', unsafe_allow_html=True)
# # import streamlit as st
# # from polygon import RESTClient
# # import pandas as pd
# # import plotly.express as px
# # import yfinance as yf
# #
# # # Initialize the Polygon REST client
# # API_KEY = 'y6LU1NRQtO2ogTHRIcMMxQoI2whgMPeG'  # Replace with your actual API key
# # client = RESTClient(API_KEY)
# #
# # # Set page configuration
# # st.set_page_config(page_title="Naf-YFinance - Stock Data Fetcher", layout="wide", page_icon="📈")
# #
# # # Custom CSS for a modern UI with black background
# # st.markdown(
# #     """
# #     <style>
# #     .main {
# #         background-color: #000000;
# #         padding: 20px;
# #         border-radius: 10px;
# #         box-shadow: 0px 0px 15px rgba(0, 0, 0, 0.1);
# #         font-family: 'Arial', sans-serif;
# #         color: #FFFFFF;
# #         text-align: center;
# #     }
# #     .stButton>button {
# #         background-color: #5A189A;
# #         color: #FFFFFF;
# #         font-size: 16px;
# #         padding: 10px 20px;
# #         border: none;
# #         border-radius: 5px;
# #         cursor: pointer;
# #     }
# #     .stButton>button:hover {
# #         background-color: #9D4EDD;
# #     }
# #     .stTextInput>div>div>input {
# #         background-color: #E5E5E5;
# #         color: #333333;
# #         border: 1px solid #CCCCCC;
# #         border-radius: 5px;
# #         padding: 10px;
# #     }
# #     .green-container {
# #         background-color: #DFF2BF;
# #         padding: 10px;
# #         border-radius: 5px;
# #         color: #4F8A10;
# #         font-weight: bold;
# #         margin-bottom: 15px;
# #     }
# #     h1 {
# #         font-size: 28px;
# #         margin-bottom: 10px;
# #         margin-top: 0;  /* Removed extra padding from top */
# #     }
# #     .tagline {
# #         font-size: 18px;
# #         color: #DDDDDD;
# #         margin-bottom: 10px;
# #     }
# #     .footer {
# #         position: fixed;
# #         bottom: 0;
# #         width: 100%;
# #         text-align: center;
# #         color: #DDDDDD;
# #         padding: 10px;
# #         font-size: 14px;
# #     }
# #     </style>
# #     """, unsafe_allow_html=True
# # )
# #
# # # App Title and Tagline
# # st.markdown("<h1>Naf-YFinance - Stock Data Fetcher 📈</h1>", unsafe_allow_html=True)
# # st.markdown('<p class="tagline">Download data from any stock company from symbol</p>', unsafe_allow_html=True)
# #
# # # Sidebar for User Input
# # st.sidebar.header("User Input")
# # ticker = st.sidebar.text_input("Enter Ticker Symbol (e.g., AAPL):", value="AAPL").upper()
# # multiplier = st.sidebar.number_input("Enter Multiplier (e.g., 1 for minute data):", min_value=1, value=1)
# # timespan = st.sidebar.selectbox("Select Timespan:",
# #                                 options=["second", "minute", "hour", "day", "week", "month", "quarter", "year"],
# #                                 index=0)
# # from_date = st.sidebar.date_input("Start Date:", value=pd.to_datetime("2014-01-01"))
# # to_date = st.sidebar.date_input("End Date:", value=pd.to_datetime("2024-01-01"))
# #
# #
# # # Function to fetch stock data and financials
# # def fetch_data():
# #     try:
# #         # Fetch aggregate data based on user input
# #         aggs = client.get_aggs(
# #             ticker=ticker,
# #             multiplier=multiplier,
# #             timespan=timespan,
# #             from_=from_date.strftime('%Y-%m-%d'),
# #             to=to_date.strftime('%Y-%m-%d')
# #         )
# #         df = pd.DataFrame(aggs)
# #
# #         # Download data using yfinance for visualization
# #         stock = yf.Ticker(ticker)
# #         data = stock.history(start=from_date, end=to_date)
# #
# #         # Fetch financial data
# #         income_statement = stock.financials
# #         cash_flow = stock.cashflow
# #         balance_sheet = stock.balance_sheet  # Fetch balance sheet
# #
# #         return df, data, income_statement, cash_flow, balance_sheet
# #
# #     except Exception as e:
# #         st.error(f"An error occurred: {e}")
# #         return pd.DataFrame(), pd.DataFrame(), pd.DataFrame(), pd.DataFrame(), pd.DataFrame()
# #
# #
# # # Fetch the data
# # df, data, income_statement, cash_flow, balance_sheet = fetch_data()
# #
# # # Create tabs for different sections
# # tab1, tab2, tab3 = st.tabs(["Stock Data", "Financial Statements", "Stock Analysis"])
# #
# # # Tab 1: Stock Data
# # with tab1:
# #     st.header("Stock Data")
# #     if not data.empty:
# #         fig = px.line(data, x=data.index, y='Close', title=f"{ticker} Stock Prices",
# #                       line_shape='linear',
# #                       color_discrete_sequence=['#5AB834'])
# #         st.plotly_chart(fig)
# #     else:
# #         st.error("No data available for the selected ticker.")
# #
# #     if df.empty:
# #         st.error("No data available for the selected parameters. Please try different inputs.")
# #     else:
# #         df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
# #         st.dataframe(df)
# #
# #         # Download button for Excel file
# #         output_filename = f"{ticker}_stock_data_{from_date}_to_{to_date}.xlsx"
# #         df.to_excel(output_filename, index=False)
# #         st.success(f"Data fetched successfully and saved to '{output_filename}'.")
# #         st.download_button(label="Download Excel File", data=open(output_filename, 'rb').read(),
# #                            file_name=output_filename)
# #
# # # Tab 2: Financial Statements
# # with tab2:
# #     st.header("Financial Statements")
# #
# #     # Display Income Statement and Cash Flow
# #     if not income_statement.empty:
# #         st.subheader("Income Statement")
# #         st.dataframe(income_statement)
# #         # Download button for Income Statement
# #         income_output_filename = f"{ticker}_income_statement.xlsx"
# #         income_statement.to_excel(income_output_filename)
# #         st.download_button(label="Download Income Statement", data=open(income_output_filename, 'rb').read(),
# #                            file_name=income_output_filename)
# #     else:
# #         st.error("No income statement data available.")
# #
# #     if not cash_flow.empty:
# #         st.subheader("Cash Flow Statement")
# #         st.dataframe(cash_flow)
# #         # Download button for Cash Flow
# #         cash_flow_output_filename = f"{ticker}_cash_flow.xlsx"
# #         cash_flow.to_excel(cash_flow_output_filename)
# #         st.download_button(label="Download Cash Flow Statement", data=open(cash_flow_output_filename, 'rb').read(),
# #                            file_name=cash_flow_output_filename)
# #     else:
# #         st.error("No cash flow data available.")
# #
# #     # Display Balance Sheet
# #     if not balance_sheet.empty:
# #         st.subheader("Balance Sheet")
# #         st.dataframe(balance_sheet)
# #         # Download button for Balance Sheet
# #         balance_sheet_output_filename = f"{ticker}_balance_sheet.xlsx"
# #         balance_sheet.to_excel(balance_sheet_output_filename)
# #         st.download_button(label="Download Balance Sheet", data=open(balance_sheet_output_filename, 'rb').read(),
# #                            file_name=balance_sheet_output_filename)
# #     else:
# #         st.error("No balance sheet data available.")
# #
# # # Tab 3: Stock Analysis
# # with tab3:
# #     st.header("Stock Analysis")
# #     st.write("Analyzing stock movements...")
# #
# #     # Check if data is available
# #     if not data.empty:
# #         # Ensure the 'Date' column is a datetime object
# #         data.index = pd.to_datetime(data.index)
# #
# #         # Split date and time into separate columns
# #         data['Date'] = data.index.date
# #         data['Time'] = data.index.time
# #
# #         # Display the High and Low price charts
# #         st.subheader("High and Low Price Analysis")
# #
# #         # Plot High Prices and Low Prices on the same graph
# #         fig_high_low = px.line(data, x=data.index, y=['High', 'Low'],
# #                                title=f"{ticker} High and Low Prices Over Time",
# #                                line_shape='linear',
# #                                color_discrete_map={'High': '#F39C12', 'Low': '#2980B9'})
# #         st.plotly_chart(fig_high_low)
# #
# #         # Calculate Highest Opening and Lowest Closing
# #         highest_opening = data['Open'].max()
# #         lowest_closing = data['Close'].min()
# #
# #         # Display the highest opening and lowest closing in a new chart
# #         st.subheader("Highest Opening and Lowest Closing")
# #
# #         # Create a DataFrame for plotting
# #         analysis_df = pd.DataFrame({
# #             'Metric': ['Highest Opening', 'Lowest Closing'],
# #             'Value': [highest_opening, lowest_closing]
# #         })
# #
# #         # Plot the highest opening and lowest closing
# #         fig_open_close = px.bar(analysis_df, x='Metric', y='Value',
# #                                 title=f"{ticker} Highest Opening and Lowest Closing",
# #                                 color='Metric',
# #                                 color_discrete_map={'Highest Opening': '#5AB834', 'Lowest Closing': '#FF4C4C'})
# #         st.plotly_chart(fig_open_close)
# #
# #         # Display a table with the selected information
# #         st.subheader("Summary Table")

# # import streamlit as st
# # from polygon import RESTClient
# # import pandas as pd
# # import plotly.express as px
# # import yfinance as yf
# #
# # # Initialize the Polygon REST client
# # API_KEY = 'y6LU1NRQtO2ogTHRIcMMxQoI2whgMPeG'  # Replace with your actual API key
# # client = RESTClient(API_KEY)
# #
# # # Set page configuration
# # st.set_page_config(page_title="Naf-YFinance - Stock Data Fetcher", layout="wide", page_icon="📈")
# #
# # # Custom CSS for a modern UI with black background
# # st.markdown(
# #     """
# #     <style>
# #     .main {
# #         background-color: #000000;
# #         padding: 20px;
# #         border-radius: 10px;
# #         box-shadow: 0px 0px 15px rgba(0, 0, 0, 0.1);
# #         font-family: 'Arial', sans-serif;
# #         color: #FFFFFF;
# #         text-align: center;
# #     }
# #     .stButton>button {
# #         background-color: #5A189A;
# #         color: #FFFFFF;
# #         font-size: 16px;
# #         padding: 10px 20px;
# #         border: none;
# #         border-radius: 5px;
# #         cursor: pointer;
# #     }
# #     .stButton>button:hover {
# #         background-color: #9D4EDD;
# #     }
# #     .stTextInput>div>div>input {
# #         background-color: #E5E5E5;
# #         color: #333333;
# #         border: 1px solid #CCCCCC;
# #         border-radius: 5px;
# #         padding: 10px;
# #     }
# #     .green-container {
# #         background-color: #DFF2BF;
# #         padding: 10px;
# #         border-radius: 5px;
# #         color: #4F8A10;
# #         font-weight: bold;
# #         margin-bottom: 15px;
# #     }
# #     h1 {
# #         font-size: 28px;
# #         margin-bottom: 10px;
# #         margin-top: 0;  /* Removed extra padding from top */
# #     }
# #     .tagline {
# #         font-size: 18px;
# #         color: #DDDDDD;
# #         margin-bottom: 10px;
# #     }
# #     .footer {
# #         position: fixed;
# #         bottom: 0;
# #         width: 100%;
# #         text-align: center;
# #         color: #DDDDDD;
# #         padding: 10px;
# #         font-size: 14px;
# #     }
# #     </style>
# #     """, unsafe_allow_html=True
# # )
# #
# # # App Title and Tagline
# # st.markdown("<h1>Naf-YFinance - Stock Data Fetcher 📈</h1>", unsafe_allow_html=True)
# # st.markdown('<p class="tagline">Download data from any stock company from symbol</p>', unsafe_allow_html=True)
# #
# # # Sidebar for User Input
# # st.sidebar.header("User Input")
# # ticker = st.sidebar.text_input("Enter Ticker Symbol (e.g., AAPL):", value="AAPL").upper()
# # multiplier = st.sidebar.number_input("Enter Multiplier (e.g., 1 for minute data):", min_value=1, value=1)
# # timespan = st.sidebar.selectbox("Select Timespan:",
# #                                 options=["second", "minute", "hour", "day", "week", "month", "quarter", "year"],
# #                                 index=0)
# # from_date = st.sidebar.date_input("Start Date:", value=pd.to_datetime("2014-01-01"))
# # to_date = st.sidebar.date_input("End Date:", value=pd.to_datetime("2024-01-01"))
# #
# # # Function to fetch stock data and financials
# # def fetch_data():
# #     try:
# #         # Fetch aggregate data based on user input
# #         aggs = client.get_aggs(
# #             ticker=ticker,
# #             multiplier=multiplier,
# #             timespan=timespan,
# #             from_=from_date.strftime('%Y-%m-%d'),
# #             to=to_date.strftime('%Y-%m-%d')
# #         )
# #         df = pd.DataFrame(aggs)
# #
# #         # Download data using yfinance for visualization
# #         stock = yf.Ticker(ticker)
# #         data = stock.history(start=from_date, end=to_date)
# #
# #         # Fetch financial data
# #         income_statement = stock.financials
# #         cash_flow = stock.cashflow
# #         balance_sheet = stock.balance_sheet  # Fetch balance sheet
# #
# #         return df, data, income_statement, cash_flow, balance_sheet
# #
# #     except Exception as e:
# #         st.error(f"An error occurred: {e}")
# #         return pd.DataFrame(), pd.DataFrame(), pd.DataFrame(), pd.DataFrame(), pd.DataFrame()
# #
# # # Fetch the data
# # df, data, income_statement, cash_flow, balance_sheet = fetch_data()
# #
# # # Create tabs for different sections
# # tab1, tab2, tab3 = st.tabs(["Stock Data", "Financial Statements", "Stock Analysis"])
# #
# # # Tab 1: Stock Data
# # with tab1:
# #     st.header("Stock Data")
# #     if not data.empty:
# #         fig = px.line(data, x=data.index, y='Close', title=f"{ticker} Stock Prices",
# #                       line_shape='linear',
# #                       color_discrete_sequence=['#5AB834'])
# #         st.plotly_chart(fig)
# #     else:
# #         st.error("No data available for the selected ticker.")
# #
# #     if df.empty:
# #         st.error("No data available for the selected parameters. Please try different inputs.")
# #     else:
# #         df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
# #         st.dataframe(df)
# #
# #         # Download button for Excel file
# #         output_filename = f"{ticker}_stock_data_{from_date}_to_{to_date}.xlsx"
# #         df.to_excel(output_filename, index=False)
# #         st.success(f"Data fetched successfully and saved to '{output_filename}'.")
# #         st.download_button(label="Download Excel File", data=open(output_filename, 'rb').read(),
# #                            file_name=output_filename)
# #
# # # Tab 2: Financial Statements
# # with tab2:
# #     st.header("Financial Statements")
# #
# #     # Display Income Statement and Cash Flow
# #     if not income_statement.empty:
# #         st.subheader("Income Statement")
# #         st.dataframe(income_statement)
# #         # Download button for Income Statement
# #         income_output_filename = f"{ticker}_income_statement.xlsx"
# #         income_statement.to_excel(income_output_filename)
# #         st.download_button(label="Download Income Statement", data=open(income_output_filename, 'rb').read(),
# #                            file_name=income_output_filename)
# #     else:
# #         st.error("No income statement data available.")
# #
# #     if not cash_flow.empty:
# #         st.subheader("Cash Flow Statement")
# #         st.dataframe(cash_flow)
# #         # Download button for Cash Flow
# #         cash_flow_output_filename = f"{ticker}_cash_flow.xlsx"
# #         cash_flow.to_excel(cash_flow_output_filename)
# #         st.download_button(label="Download Cash Flow Statement", data=open(cash_flow_output_filename, 'rb').read(),
# #                            file_name=cash_flow_output_filename)
# #     else:
# #         st.error("No cash flow data available.")
# #
# #     # Display Balance Sheet
# #     if not balance_sheet.empty:
# #         st.subheader("Balance Sheet")
# #         st.dataframe(balance_sheet)
# #         # Download button for Balance Sheet
# #         balance_sheet_output_filename = f"{ticker}_balance_sheet.xlsx"
# #         balance_sheet.to_excel(balance_sheet_output_filename)
# #         st.download_button(label="Download Balance Sheet", data=open(balance_sheet_output_filename, 'rb').read(),
# #                            file_name=balance_sheet_output_filename)
# #     else:
# #         st.error("No balance sheet data available.")
# #
# # # Tab 3: Stock Analysis
# # with tab3:
# #     st.header("Stock Analysis")
# #     st.write("Analyzing stock movements...")
# #
# #     # Check if data is available
# #     if not data.empty:
# #         # Ensure the 'Date' column is a datetime object
# #         data.index = pd.to_datetime(data.index)
# #
# #         # Split date and time into separate columns
# #         data['Date'] = data.index.date
# #         data['Time'] = data.index.time
# #
# #         # Display the High and Low price charts
# #         st.subheader("High and Low Price Analysis")
# #
# #         # Plot High Prices and Low Prices on the same graph
# #         fig_high_low = px.line(data, x=data.index, y=['High', 'Low'],
# #                               title=f"{ticker} High and Low Prices Over Time",
# #                               line_shape='linear',
# #                               color_discrete_map={'High': '#F39C12', 'Low': '#2980B9'})
# #         st.plotly_chart(fig_high_low)
# #
# #         # Calculate Highest Opening and Lowest Closing
# #         highest_opening = data['Open'].max()
# #         lowest_closing = data['Close'].min()
# #
# #         # Display the highest opening and lowest closing in a new chart
# #         st.subheader("Highest Opening and Lowest Closing")
# #
# #         # Create a DataFrame for plotting
# #         analysis_df = pd.DataFrame({
# #             'Metric': ['Highest Opening', 'Lowest Closing'],
# #             'Value': [highest_opening, lowest_closing]
# #         })
# #
# #         # Plot the highest opening and lowest closing
# #         fig_open_close = px.bar(analysis_df, x='Metric', y='Value',
# #                                title=f"{ticker} Highest Opening and Lowest Closing",
# #                                color='Metric',
# #                                color_discrete_map={'Highest Opening': '#5AB834', 'Lowest Closing': '#FF0000'})
# #         st.plotly_chart(fig_open_close)
# #
# #         # Display a table with the selected information
# #         st.subheader("Summary Table")
# #         summary_data = {
# #             'Ticker Name': [ticker],
# #             'Date Range': [f"{from_date} to {to_date}"],
# #             'Highest Opening': [highest_opening],
# #             'Lowest Closing': [lowest_closing]
# #         }
# #         summary_df = pd.DataFrame(summary_data)
# #         st.dataframe(summary_df)
# #
# #     else:
# #         st.error("No data available for the selected parameters.")
# # import streamlit as st
# # from polygon import RESTClient
# # import pandas as pd
# # import plotly.express as px
# # import yfinance as yf
# #
# # # Initialize the Polygon REST client
# # API_KEY = 'y6LU1NRQtO2ogTHRIcMMxQoI2whgMPeG'  # Replace with your actual API key
# # client = RESTClient(API_KEY)
# #
# # # Set page configuration
# # st.set_page_config(page_title="Naf-YFinance - Stock Data Fetcher", layout="wide", page_icon="📈")
# #
# # # Custom CSS for a modern UI with black background
# # st.markdown(
# #     """
# #     <style>
# #     .main {
# #         background-color: #000000;
# #         padding: 20px;
# #         border-radius: 10px;
# #         box-shadow: 0px 0px 15px rgba(0, 0, 0, 0.1);
# #         font-family: 'Arial', sans-serif;
# #         color: #FFFFFF;
# #         text-align: center;
# #     }
# #     .stButton>button {
# #         background-color: #5A189A;
# #         color: #FFFFFF;
# #         font-size: 16px;
# #         padding: 10px 20px;
# #         border: none;
# #         border-radius: 5px;
# #         cursor: pointer;
# #     }
# #     .stButton>button:hover {
# #         background-color: #9D4EDD;
# #     }
# #     .stTextInput>div>div>input {
# #         background-color: #E5E5E5;
# #         color: #333333;
# #         border: 1px solid #CCCCCC;
# #         border-radius: 5px;
# #         padding: 10px;
# #     }
# #     .green-container {
# #         background-color: #DFF2BF;
# #         padding: 10px;
# #         border-radius: 5px;
# #         color: #4F8A10;
# #         font-weight: bold;
# #         margin-bottom: 15px;
# #     }
# #     h1 {
# #         font-size: 28px;
# #         margin-bottom: 10px;
# #         margin-top: 0;  /* Removed extra padding from top */
# #     }
# #     .tagline {
# #         font-size: 18px;
# #         color: #DDDDDD;
# #         margin-bottom: 10px;
# #     }
# #     .footer {
# #         position: fixed;
# #         bottom: 0;
# #         width: 100%;
# #         text-align: center;
# #         color: #DDDDDD;
# #         padding: 10px;
# #         font-size: 14px;
# #     }
# #     </style>
# #     """, unsafe_allow_html=True
# # )
# #
# # # App Title and Tagline
# # st.markdown("<h1>Naf-YFinance - Stock Data Fetcher 📈</h1>", unsafe_allow_html=True)
# # st.markdown('<p class="tagline">Download data from any stock company from symbol</p>', unsafe_allow_html=True)
# #
# # # Sidebar for User Input
# # st.sidebar.header("User Input")
# # ticker = st.sidebar.text_input("Enter Ticker Symbol (e.g., AAPL):", value="AAPL").upper()
# # multiplier = st.sidebar.number_input("Enter Multiplier (e.g., 1 for minute data):", min_value=1, value=1)
# # timespan = st.sidebar.selectbox("Select Timespan:",
# #                                 options=["second", "minute", "hour", "day", "week", "month", "quarter", "year"],
# #                                 index=0)
# # from_date = st.sidebar.date_input("Start Date:", value=pd.to_datetime("2014-01-01"))
# # to_date = st.sidebar.date_input("End Date:", value=pd.to_datetime("2024-01-01"))
# #
# # # Function to fetch stock data and financials
# # def fetch_data():
# #     try:
# #         # Fetch aggregate data based on user input
# #         aggs = client.get_aggs(
# #             ticker=ticker,
# #             multiplier=multiplier,
# #             timespan=timespan,
# #             from_=from_date.strftime('%Y-%m-%d'),
# #             to=to_date.strftime('%Y-%m-%d')
# #         )
# #         df = pd.DataFrame(aggs)
# #
# #         # Download data using yfinance for visualization
# #         stock = yf.Ticker(ticker)
# #         data = stock.history(start=from_date, end=to_date)
# #
# #         # Fetch financial data
# #         income_statement = stock.financials
# #         cash_flow = stock.cashflow
# #         balance_sheet = stock.balance_sheet  # Fetch balance sheet
# #
# #         return df, data, income_statement, cash_flow, balance_sheet
# #
# #     except Exception as e:
# #         st.error(f"An error occurred: {e}")
# #         return pd.DataFrame(), pd.DataFrame(), pd.DataFrame(), pd.DataFrame(), pd.DataFrame()
# #
# # # Fetch the data
# # df, data, income_statement, cash_flow, balance_sheet = fetch_data()
# #
# # # Create tabs for different sections
# # tab1, tab2, tab3 = st.tabs(["Stock Data", "Financial Statements", "Stock Analysis"])
# #
# # # Tab 1: Stock Data
# # with tab1:
# #     st.header("Stock Data")
# #     if not data.empty:
# #         fig = px.line(data, x=data.index, y='Close', title=f"{ticker} Stock Prices",
# #                       line_shape='linear',
# #                       color_discrete_sequence=['#5AB834'])
# #         st.plotly_chart(fig)
# #     else:
# #         st.error("No data available for the selected ticker.")
# #
# #     if df.empty:
# #         st.error("No data available for the selected parameters. Please try different inputs.")
# #     else:
# #         df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
# #         df.set_index('timestamp', inplace=True)
# #         st.dataframe(df)
# #
# #         # Download button for Excel file
# #         output_filename = f"{ticker}_stock_data_{from_date}_to_{to_date}.xlsx"
# #         df.to_excel(output_filename, index=True)
# #         st.success(f"Data fetched successfully and saved to '{output_filename}'.")
# #         st.download_button(label="Download Excel File", data=open(output_filename, 'rb').read(),
# #                            file_name=output_filename)
# #
# # # Tab 2: Financial Statements
# # with tab2:
# #     st.header("Financial Statements")
# #
# #     # Display Income Statement and Cash Flow
# #     if not income_statement.empty:
# #         st.subheader("Income Statement")
# #         st.dataframe(income_statement)
# #         # Download button for Income Statement
# #         income_output_filename = f"{ticker}_income_statement.xlsx"
# #         income_statement.to_excel(income_output_filename)
# #         st.download_button(label="Download Income Statement", data=open(income_output_filename, 'rb').read(),
# #                            file_name=income_output_filename)
# #     else:
# #         st.error("No income statement data available.")
# #
# #     if not cash_flow.empty:
# #         st.subheader("Cash Flow Statement")
# #         st.dataframe(cash_flow)
# #         # Download button for Cash Flow
# #         cash_flow_output_filename = f"{ticker}_cash_flow.xlsx"
# #         cash_flow.to_excel(cash_flow_output_filename)
# #         st.download_button(label="Download Cash Flow Statement", data=open(cash_flow_output_filename, 'rb').read(),
# #                            file_name=cash_flow_output_filename)
# #     else:
# #         st.error("No cash flow data available.")
# #
# #     # Display Balance Sheet
# #     if not balance_sheet.empty:
# #         st.subheader("Balance Sheet")
# #         st.dataframe(balance_sheet)
# #         # Download button for Balance Sheet
# #         balance_sheet_output_filename = f"{ticker}_balance_sheet.xlsx"
# #         balance_sheet.to_excel(balance_sheet_output_filename)
# #         st.download_button(label="Download Balance Sheet", data=open(balance_sheet_output_filename, 'rb').read(),
# #                            file_name=balance_sheet_output_filename)
# #     else:
# #         st.error("No balance sheet data available.")
# #
# # # Tab 3: Stock Analysis
# # with tab3:
# #     st.header("Stock Analysis")
# #     st.write("Analyzing stock movements...")
# #
# #     # Check if data is available
# #     if not data.empty:
# #         # Ensure the 'Date' column is a datetime object
# #         data.index = pd.to_datetime(data.index)
# #
# #         # Split date and time into separate columns
# #         data['Date'] = data.index.date
# #         data['Time'] = data.index.time
# #
# #         # Display the High and Low price charts
# #         st.subheader("High and Low Price Analysis")
# #
# #         # Plot High Prices and Low Prices on the same graph
# #         fig_high_low = px.line(data, x=data.index, y=['High', 'Low'],
# #                               title=f"{ticker} High and Low Prices Over Time",
# #                               line_shape='linear',
# #                               color_discrete_map={'High': '#F39C12', 'Low': '#2980B9'})
# #         st.plotly_chart(fig_high_low)
# #
# #         # Calculate Highest Opening and Lowest Closing
# #         highest_opening = data['Open'].max()
# #         lowest_closing = data['Close'].min()
# #
# #         # Display the highest opening and lowest closing in a new chart
# #         st.subheader("Highest Opening and Lowest Closing")
# #
# #         # Create a DataFrame for plotting
# #         analysis_df = pd.DataFrame({
# #             'Metric': ['Highest Opening', 'Lowest Closing'],
# #             'Value': [highest_opening, lowest_closing]
# #         })
# #
# #         # Plot the highest opening and lowest closing
# #         fig_open_close = px.bar(analysis_df, x='Metric', y='Value',
# #                                title=f"{ticker} Highest Opening and Lowest Closing",
# #                                color='Metric',
# #                                color_discrete_map={'Highest Opening': '#5AB834', 'Lowest Closing': '#FF0000'})
# #         st.plotly_chart(fig_open_close)
# #
# #         # Display a table with the selected information
# #         st.subheader("Summary")
# #         summary_data = {
# #             'Ticker Name': [ticker],
# #             'Date Range': [f"{from_date} to {to_date}"],
# #             'Highest Opening': [highest_opening],
# #             'Lowest Closing': [lowest_closing]
# #         }
# #         summary_df = pd.DataFrame(summary_data)
# #         st.dataframe(summary_df)
# #
# #     else:
# #         st.error("No data available for the selected parameters.")
# # import streamlit as st
# # from polygon import RESTClient
# # import pandas as pd
# # import plotly.express as px
# # import yfinance as yf
# #
# # # Initialize the Polygon REST client
# # API_KEY = 'y6LU1NRQtO2ogTHRIcMMxQoI2whgMPeG'  # Replace with your actual API key
# # client = RESTClient(API_KEY)
# #
# # # Set page configuration
# # st.set_page_config(page_title="Naf-YFinance - Stock Data Fetcher", layout="wide", page_icon="📈")
# #
# # # Custom CSS for a modern UI with black background
# # st.markdown(
# #     """
# #     <style>
# #     .main {
# #         background-color: #000000;
# #         padding: 20px;
# #         border-radius: 10px;
# #         box-shadow: 0px 0px 15px rgba(0, 0, 0, 0.1);
# #         font-family: 'Arial', sans-serif;
# #         color: #FFFFFF;
# #         text-align: center;
# #     }
# #     .stButton>button {
# #         background-color: #5A189A;
# #         color: #FFFFFF;
# #         font-size: 16px;
# #         padding: 10px 20px;
# #         border: none;
# #         border-radius: 5px;
# #         cursor: pointer;
# #     }
# #     .stButton>button:hover {
# #         background-color: #9D4EDD;
# #     }
# #     .stTextInput>div>div>input {
# #         background-color: #E5E5E5;
# #         color: #333333;
# #         border: 1px solid #CCCCCC;
# #         border-radius: 5px;
# #         padding: 10px;
# #     }
# #     .green-container {
# #         background-color: #DFF2BF;
# #         padding: 10px;
# #         border-radius: 5px;
# #         color: #4F8A10;
# #         font-weight: bold;
# #         margin-bottom: 15px;
# #     }
# #     h1 {
# #         font-size: 28px;
# #         margin-bottom: 10px;
# #         margin-top: 0;  /* Removed extra padding from top */
# #     }
# #     .tagline {
# #         font-size: 18px;
# #         color: #DDDDDD;
# #         margin-bottom: 10px;
# #     }
# #     .footer {
# #         position: fixed;
# #         bottom: 0;
# #         width: 100%;
# #         text-align: center;
# #         color: #DDDDDD;
# #         padding: 10px;
# #         font-size: 14px;
# #     }
# #     </style>
# #     """, unsafe_allow_html=True
# # )
# #
# # # App Title and Tagline
# # st.markdown("<h1>Naf-YFinance - Stock Data Fetcher 📈</h1>", unsafe_allow_html=True)
# # st.markdown('<p class="tagline">Download data from any stock company from symbol</p>', unsafe_allow_html=True)
# #
# # # Sidebar for User Input
# # st.sidebar.header("User Input")
# # ticker = st.sidebar.text_input("Enter Ticker Symbol (e.g., AAPL):", value="AAPL").upper()
# # multiplier = st.sidebar.number_input("Enter Multiplier (e.g., 1 for minute data):", min_value=1, value=1)
# # timespan = st.sidebar.selectbox("Select Timespan:",
# #                                 options=["second", "minute", "hour", "day", "week", "month", "quarter", "year"],
# #                                 index=0)
# # from_date = st.sidebar.date_input("Start Date:", value=pd.to_datetime("2014-01-01"))
# # to_date = st.sidebar.date_input("End Date:", value=pd.to_datetime("2024-01-01"))
# #
# #
# # # Function to fetch stock data and financials
# # def fetch_data(ticker, from_date, to_date, multiplier, timespan):
# #     try:
# #         # Fetch aggregate data based on user input
# #         aggs = client.get_aggs(
# #             ticker=ticker,
# #             multiplier=multiplier,
# #             timespan=timespan,
# #             from_=from_date.strftime('%Y-%m-%d'),
# #             to=to_date.strftime('%Y-%m-%d')
# #         )
# #         df = pd.DataFrame(aggs)
# #
# #         # Download data using yfinance for visualization
# #         stock = yf.Ticker(ticker)
# #         data = stock.history(start=from_date, end=to_date)
# #
# #         # Fetch financial data
# #         income_statement = stock.financials
# #         cash_flow = stock.cashflow
# #         balance_sheet = stock.balance_sheet  # Fetch balance sheet
# #
# #         return df, data, income_statement, cash_flow, balance_sheet
# #
# #     except Exception as e:
# #         st.error(f"An error occurred: {e}")
# #         return pd.DataFrame(), pd.DataFrame(), pd.DataFrame(), pd.DataFrame(), pd.DataFrame()
# # # Helper function to fetch data
# # def fetch_gap_data(ticker, from_date, to_date):
# #     try:
# #         stock = yf.Ticker(ticker)
# #         data = stock.history(start=from_date, end=to_date)
# #         return data
# #     except Exception as e:
# #         st.error(f"An error occurred: {e}")
# #         return pd.DataFrame()
# #
# #
# # # Main app
# # st.title("Stock Analysis App")
# #
# # # Create tabs for different sections
# # tab1, tab2, tab3 = st.tabs(["Stock Data", "Financial Statements", "Stock Analysis"])
# #
# # # Tab 1: Stock Data
# # with tab1:
# #     st.header("Stock Data")
# #     df, data, _, _, _ = fetch_data(ticker, from_date, to_date, multiplier, timespan)
# #
# #     if not data.empty:
# #         fig = px.line(data, x=data.index, y='Close', title=f"{ticker} Stock Prices",
# #                       line_shape='linear',
# #                       color_discrete_sequence=['#5AB834'])
# #         st.plotly_chart(fig)
# #     else:
# #         st.error("No data available for the selected ticker.")
# #
# #     if df.empty:
# #         st.error("No data available for the selected parameters. Please try different inputs.")
# #     else:
# #         df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
# #         df.set_index('timestamp', inplace=True)
# #         st.dataframe(df)
# #
# #         # Download button for Excel file
# #         output_filename = f"{ticker}_stock_data_{from_date}_to_{to_date}.xlsx"
# #         df.to_excel(output_filename, index=True)
# #         st.success(f"Data fetched successfully and saved to '{output_filename}'.")
# #         st.download_button(label="Download Excel File", data=open(output_filename, 'rb').read(),
# #                            file_name=output_filename)
# #
# # # Tab 2: Financial Statements
# # with tab2:
# #     st.header("Financial Statements")
# #     _, _, income_statement, cash_flow, balance_sheet = fetch_data(ticker, from_date, to_date, multiplier, timespan)
# #
# #     # Display Income Statement and Cash Flow
# #     if not income_statement.empty:
# #         st.subheader("Income Statement")
# #         st.dataframe(income_statement)
# #         # Download button for Income Statement
# #         income_output_filename = f"{ticker}_income_statement.xlsx"
# #         income_statement.to_excel(income_output_filename)
# #         st.download_button(label="Download Income Statement", data=open(income_output_filename, 'rb').read(),
# #                            file_name=income_output_filename)
# #     else:
# #         st.error("No income statement data available.")
# #
# #     if not cash_flow.empty:
# #         st.subheader("Cash Flow Statement")
# #         st.dataframe(cash_flow)
# #         # Download button for Cash Flow
# #         cash_flow_output_filename = f"{ticker}_cash_flow.xlsx"
# #         cash_flow.to_excel(cash_flow_output_filename)
# #         st.download_button(label="Download Cash Flow Statement", data=open(cash_flow_output_filename, 'rb').read(),
# #                            file_name=cash_flow_output_filename)
# #     else:
# #         st.error("No cash flow data available.")
# #
# #     # Display Balance Sheet
# #     if not balance_sheet.empty:
# #         st.subheader("Balance Sheet")
# #         st.dataframe(balance_sheet)
# #         # Download button for Balance Sheet
# #         balance_sheet_output_filename = f"{ticker}_balance_sheet.xlsx"
# #         balance_sheet.to_excel(balance_sheet_output_filename)
# #         st.download_button(label="Download Balance Sheet", data=open(balance_sheet_output_filename, 'rb').read(),
# #                            file_name=balance_sheet_output_filename)
# #     else:
# #         st.error("No balance sheet data available.")
# #
# # # Tab 3: Stock Analysis
# # with tab3:
# #     st.header("Stock Analysis")
# #     subtab1, subtab2 = st.tabs(["Stock Comparison", "Gap Analysis"])
# #
# #     # Sub-tab 1: Stock Comparison
# #     with subtab1:
# #         st.header("Stock Comparison")
# #
# #         # User inputs for stock comparison
# #         ticker1 = st.text_input("Enter First Ticker Symbol (e.g., AAPL):", value="AAPL").upper()
# #         ticker2 = st.text_input("Enter Second Ticker Symbol (e.g., MSFT):", value="MSFT").upper()
# #
# #         multiplier1 = st.number_input("Enter Multiplier for First Ticker (e.g., 1 for minute data):", min_value=1,
# #                                       value=1, key='multiplier1')
# #         multiplier2 = st.number_input("Enter Multiplier for Second Ticker (e.g., 1 for minute data):", min_value=1,
# #                                       value=1, key='multiplier2')
# #
# #         timespan1 = st.selectbox("Select Timespan for First Ticker:",
# #                                  options=["second", "minute", "hour", "day", "week", "month", "quarter", "year"],
# #                                  index=0, key='timespan1')
# #         timespan2 = st.selectbox("Select Timespan for Second Ticker:",
# #                                  options=["second", "minute", "hour", "day", "week", "month", "quarter", "year"],
# #                                  index=0, key='timespan2')
# #
# #         from_date1 = st.date_input("Start Date for First Ticker:", value=pd.to_datetime("2022-01-01"), key='from_date1')
# #         to_date1 = st.date_input("End Date for First Ticker:", value=pd.to_datetime("2024-01-01"), key='to_date1')
# #
# #         from_date2 = st.date_input("Start Date for Second Ticker:", value=pd.to_datetime("2022-01-01"),
# #                                    key='from_date2')
# #         to_date2 = st.date_input("End Date for Second Ticker:", value=pd.to_datetime("2024-01-01"), key='to_date2')
# #
# #
# #         def fetch_comparison_data(ticker, from_date, to_date, multiplier, timespan):
# #             try:
# #                 aggs = client.get_aggs(
# #                     ticker=ticker,
# #                     multiplier=multiplier,
# #                     timespan=timespan,
# #                     from_=from_date.strftime('%Y-%m-%d'),
# #                     to=to_date.strftime('%Y-%m-%d')
# #                 )
# #                 df = pd.DataFrame(aggs)
# #                 df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
# #                 df.set_index('timestamp', inplace=True)
# #                 return df
# #             except Exception as e:
# #                 st.error(f"An error occurred: {e}")
# #                 return pd.DataFrame()
# #
# #
# #         df1 = fetch_comparison_data(ticker1, from_date1, to_date1, multiplier1, timespan1)
# #         df2 = fetch_comparison_data(ticker2, from_date2, to_date2, multiplier2, timespan2)
# #
# #         if not df1.empty and not df2.empty:
# #             # Plot data comparison
# #             fig1 = px.line(df1, x=df1.index, y=['high', 'low'], title=f"{ticker1} Stock Prices Comparison",
# #                            line_shape='linear',
# #                            color_discrete_sequence=['#FF0000', '#00FF00'])
# #             fig2 = px.line(df2, x=df2.index, y=['high', 'low'], title=f"{ticker2} Stock Prices Comparison",
# #                            line_shape='linear',
# #                            color_discrete_sequence=['#FF0000', '#00FF00'])
# #
# #             st.plotly_chart(fig1, use_container_width=True)
# #             st.plotly_chart(fig2, use_container_width=True)
# #
# #             # Summary table
# #             summary_data = {
# #                 'Ticker': [ticker1, ticker2],
# #                 'Highest Opening': [df1['high'].max(), df2['high'].max()],
# #                 'Lowest Closing': [df1['close'].min(), df2['close'].min()]
# #             }
# #             summary_df = pd.DataFrame(summary_data)
# #             st.dataframe(summary_df)
# #
# #         else:
# #             st.error("No data available for one or both of the tickers.")
# #
# #     # Sub-tab 2: Gap Analysis
# #     # Sub-tab 2: Gap Analysis
# #     with subtab2:
# #         st.header("Gap Analysis")
# #
# #         ticker_gap = st.text_input("Enter Ticker Symbol for Gap Analysis (e.g., AAPL):", value="AAPL").upper()
# #         from_date_gap = st.date_input("Start Date:", value=pd.to_datetime("2022-01-01"), key='from_date_gap')
# #         to_date_gap = st.date_input("End Date:", value=pd.to_datetime("2024-01-01"), key='to_date_gap')
# #
# #
# #         def fetch_gap_data(ticker, from_date, to_date):
# #             try:
# #                 stock = yf.Ticker(ticker)
# #                 data = stock.history(start=from_date, end=to_date)
# #                 return data
# #             except Exception as e:
# #                 st.error(f"An error occurred: {e}")
# #                 return pd.DataFrame()
# #
# #
# #         gap_data = fetch_gap_data(ticker_gap, from_date_gap, to_date_gap)
# #
# #         if not gap_data.empty:
# #             # Add a 'Week' column with start of week date
# #             gap_data['Week'] = gap_data.index.to_period('W').to_timestamp()
# #
# #             # Aggregate data by week and compute average closing price
# #             weekly_data = gap_data.groupby('Week').agg({'Close': 'mean'}).reset_index()
# #
# #             # Add a 'Next Week' column
# #             weekly_data['Next Week'] = weekly_data['Week'] + pd.DateOffset(weeks=1)
# #
# #             # Ensure both columns are in the same time zone
# #             weekly_data['Next Week'] = pd.to_datetime(weekly_data['Next Week']).dt.tz_localize(None)
# #             gap_data.index = pd.to_datetime(gap_data.index).dt.tz_localize(None)
# #
# #             # Merge with original data to get the closing price of the next week
# #             weekly_data = weekly_data.merge(gap_data[['Close']], left_on='Next Week', right_index=True,
# #                                             suffixes=('', '_Next'))
# #
# #             # Plotting
# #             fig_gap = px.line(weekly_data, x='Week', y=['Close', 'Close_Next'],
# #                               title=f"{ticker_gap} Weekly Gap Analysis",
# #                               labels={'value': 'Stock Price', 'Week': 'Week'},
# #                               color_discrete_sequence=['#FF0000', '#00FF00'])
# #             st.plotly_chart(fig_gap, use_container_width=True)
# #
# #             # Summary table
# #             gap_summary_data = {
# #                 'Week': weekly_data['Week'],
# #                 'Average Price': weekly_data['Close'],
# #                 'Price Next Week': weekly_data['Close_Next']
# #             }
# #             gap_summary_df = pd.DataFrame(gap_summary_data)
# #             st.dataframe(gap_summary_df)
# #
# #         else:
# #             st.error("No data available for the selected ticker and date range.")
# #
# # # Footer
# # st.markdown('<div class="footer">Powered by Naf-Byte (Nafay Ur Rehman)</div>', unsafe_allow_html=True)
# # import streamlit as st
# # from polygon import RESTClient
# # import pandas as pd
# # import plotly.express as px
# # import yfinance as yf
# #
# # # Initialize the Polygon REST client
# # API_KEY = 'y6LU1NRQtO2ogTHRIcMMxQoI2whgMPeG'  # Replace with your actual API key
# # client = RESTClient(API_KEY)
# #
# # # Set page configuration
# # st.set_page_config(page_title="Naf-YFinance - Stock Data Fetcher", layout="wide", page_icon="📈")
# #
# # # Custom CSS for a modern UI with black background
# # st.markdown(
# #     """
# #     <style>
# #     .main {
# #         background-color: #000000;
# #         padding: 20px;
# #         border-radius: 10px;
# #         box-shadow: 0px 0px 15px rgba(0, 0, 0, 0.1);
# #         font-family: 'Arial', sans-serif;
# #         color: #FFFFFF;
# #         text-align: center;
# #     }
# #     .stButton>button {
# #         background-color: #5A189A;
# #         color: #FFFFFF;
# #         font-size: 16px;
# #         padding: 10px 20px;
# #         border: none;
# #         border-radius: 5px;
# #         cursor: pointer;
# #     }
# #     .stButton>button:hover {
# #         background-color: #9D4EDD;
# #     }
# #     .stTextInput>div>div>input {
# #         background-color: #E5E5E5;
# #         color: #333333;
# #         border: 1px solid #CCCCCC;
# #         border-radius: 5px;
# #         padding: 10px;
# #     }
# #     .green-container {
# #         background-color: #DFF2BF;
# #         padding: 10px;
# #         border-radius: 5px;
# #         color: #4F8A10;
# #         font-weight: bold;
# #         margin-bottom: 15px;
# #     }
# #     h1 {
# #         font-size: 28px;
# #         margin-bottom: 10px;
# #         margin-top: 0;  /* Removed extra padding from top */
# #     }
# #     .tagline {
# #         font-size: 18px;
# #         color: #DDDDDD;
# #         margin-bottom: 10px;
# #     }
# #     .footer {
# #         position: fixed;
# #         bottom: 0;
# #         width: 100%;
# #         text-align: center;
# #         color: #DDDDDD;
# #         padding: 10px;
# #         font-size: 14px;
# #     }
# #     </style>
# #     """, unsafe_allow_html=True
# # )
# #
# # # App Title and Tagline
# # st.markdown("<h1>Naf-YFinance - Stock Data Fetcher 📈</h1>", unsafe_allow_html=True)
# # st.markdown('<p class="tagline">Download data from any stock company from symbol</p>', unsafe_allow_html=True)
# #
# # # Sidebar for User Input
# # st.sidebar.header("User Input")
# # ticker = st.sidebar.text_input("Enter Ticker Symbol (e.g., AAPL):", value="AAPL").upper()
# # multiplier = st.sidebar.number_input("Enter Multiplier (e.g., 1 for minute data):", min_value=1, value=1)
# # timespan = st.sidebar.selectbox("Select Timespan:",
# #                                 options=["second", "minute", "hour", "day", "week", "month", "quarter", "year"],
# #                                 index=0)
# # from_date = st.sidebar.date_input("Start Date:", value=pd.to_datetime("2014-01-01"))
# # to_date = st.sidebar.date_input("End Date:", value=pd.to_datetime("2024-01-01"))
# #
# #
# # # Function to fetch stock data and financials
# # def fetch_data(ticker, from_date, to_date, multiplier, timespan):
# #     try:
# #         # Fetch aggregate data based on user input
# #         aggs = client.get_aggs(
# #             ticker=ticker,
# #             multiplier=multiplier,
# #             timespan=timespan,
# #             from_=from_date.strftime('%Y-%m-%d'),
# #             to=to_date.strftime('%Y-%m-%d')
# #         )
# #         df = pd.DataFrame(aggs)
# #
# #         # Download data using yfinance for visualization
# #         stock = yf.Ticker(ticker)
# #         data = stock.history(start=from_date, end=to_date)
# #
# #         # Fetch financial data
# #         income_statement = stock.financials
# #         cash_flow = stock.cashflow
# #         balance_sheet = stock.balance_sheet  # Fetch balance sheet
# #
# #         return df, data, income_statement, cash_flow, balance_sheet
# #
# #     except Exception as e:
# #         st.error(f"An error occurred: {e}")
# #         return pd.DataFrame(), pd.DataFrame(), pd.DataFrame(), pd.DataFrame(), pd.DataFrame()
# #
# #
# # # Helper function to fetch data
# # def fetch_gap_data(ticker, from_date, to_date):
# #     try:
# #         stock = yf.Ticker(ticker)
# #         data = stock.history(start=from_date, end=to_date)
# #         return data
# #     except Exception as e:
# #         st.error(f"An error occurred: {e}")
# #         return pd.DataFrame()
# #
# #
# # # Main app
# # st.title("Stock Analysis App")
# #
# # # Create tabs for different sections
# # tab1, tab2, tab3 = st.tabs(["Stock Data", "Financial Statements", "Stock Analysis"])
# #
# # # Tab 1: Stock Data
# # with tab1:
# #     st.header("Stock Data")
# #     df, data, _, _, _ = fetch_data(ticker, from_date, to_date, multiplier, timespan)
# #
# #     if not data.empty:
# #         fig = px.line(data, x=data.index, y='Close', title=f"{ticker} Stock Prices",
# #                       line_shape='linear',
# #                       color_discrete_sequence=['#5AB834'])
# #         st.plotly_chart(fig)
# #     else:
# #         st.error("No data available for the selected ticker.")
# #
# #     if df.empty:
# #         st.error("No data available for the selected parameters. Please try different inputs.")
# #     else:
# #         df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
# #         df.set_index('timestamp', inplace=True)
# #         st.dataframe(df)
# #
# #         # Download button for Excel file
# #         output_filename = f"{ticker}_stock_data_{from_date}_to_{to_date}.xlsx"
# #         df.to_excel(output_filename, index=True)
# #         st.success(f"Data fetched successfully and saved to '{output_filename}'.")
# #         st.download_button(label="Download Excel File", data=open(output_filename, 'rb').read(),
# #                            file_name=output_filename)
# #
# # # Tab 2: Financial Statements
# # with tab2:
# #     st.header("Financial Statements")
# #     _, _, income_statement, cash_flow, balance_sheet = fetch_data(ticker, from_date, to_date, multiplier, timespan)
# #
# #     # Display Income Statement and Cash Flow
# #     if not income_statement.empty:
# #         st.subheader("Income Statement")
# #         st.dataframe(income_statement)
# #         # Download button for Income Statement
# #         income_output_filename = f"{ticker}_income_statement.xlsx"
# #         income_statement.to_excel(income_output_filename)
# #         st.download_button(label="Download Income Statement", data=open(income_output_filename, 'rb').read(),
# #                            file_name=income_output_filename)
# #     else:
# #         st.error("No income statement data available.")
# #
# #     if not cash_flow.empty:
# #         st.subheader("Cash Flow Statement")
# #         st.dataframe(cash_flow)
# #         # Download button for Cash Flow
# #         cash_flow_output_filename = f"{ticker}_cash_flow.xlsx"
# #         cash_flow.to_excel(cash_flow_output_filename)
# #         st.download_button(label="Download Cash Flow Statement", data=open(cash_flow_output_filename, 'rb').read(),
# #                            file_name=cash_flow_output_filename)
# #     else:
# #         st.error("No cash flow data available.")
# #
# #     # Display Balance Sheet
# #     if not balance_sheet.empty:
# #         st.subheader("Balance Sheet")
# #         st.dataframe(balance_sheet)
# #         # Download button for Balance Sheet
# #         balance_sheet_output_filename = f"{ticker}_balance_sheet.xlsx"
# #         balance_sheet.to_excel(balance_sheet_output_filename)
# #         st.download_button(label="Download Balance Sheet", data=open(balance_sheet_output_filename, 'rb').read(),
# #                            file_name=balance_sheet_output_filename)
# #     else:
# #         st.error("No balance sheet data available.")
# #
# # # Tab 3: Stock Analysis
# # with tab3:
# #     st.header("Stock Analysis")
# #     subtab1, subtab2 = st.tabs(["Stock Comparison", "Gap Analysis"])
# #
# #     # Sub-tab 1: Stock Comparison
# #     with subtab1:
# #         st.header("Stock Comparison")
# #
# #         # User inputs for stock comparison
# #         ticker1 = st.text_input("Enter First Ticker Symbol (e.g., AAPL):", value="AAPL").upper()
# #         ticker2 = st.text_input("Enter Second Ticker Symbol (e.g., MSFT):", value="MSFT").upper()
# #
# #         multiplier1 = st.number_input("Enter Multiplier for First Ticker (e.g., 1 for minute data):", min_value=1,
# #                                       value=1, key='multiplier1')
# #         multiplier2 = st.number_input("Enter Multiplier for Second Ticker (e.g., 1 for minute data):", min_value=1,
# #                                       value=1, key='multiplier2')
# #
# #         timespan1 = st.selectbox("Select Timespan for First Ticker:",
# #                                  options=["second", "minute", "hour", "day", "week", "month", "quarter", "year"],
# #                                  index=0, key='timespan1')
# #         timespan2 = st.selectbox("Select Timespan for Second Ticker:",
# #                                  options=["second", "minute", "hour", "day", "week", "month", "quarter", "year"],
# #                                  index=0, key='timespan2')
# #
# #         from_date1 = st.date_input("Start Date for First Ticker:", value=pd.to_datetime("2014-01-01"), key='from_date1')
# #         to_date1 = st.date_input("End Date for First Ticker:", value=pd.to_datetime("2024-01-01"), key='to_date1')
# #
# #         from_date2 = st.date_input("Start Date for Second Ticker:", value=pd.to_datetime("2014-01-01"),
# #                                    key='from_date2')
# #         to_date2 = st.date_input("End Date for Second Ticker:", value=pd.to_datetime("2024-01-01"), key='to_date2')
# #
# #         if ticker1 and ticker2:
# #             df1, data1, _, _, _ = fetch_data(ticker1, from_date1, to_date1, multiplier1, timespan1)
# #             df2, data2, _, _, _ = fetch_data(ticker2, from_date2, to_date2, multiplier2, timespan2)
# #
# #             col1, col2 = st.columns(2)
# #
# #             # Display data for first stock
# #             with col1:
# #                 st.subheader(f"{ticker1} Data")
# #                 if not data1.empty:
# #                     fig1 = px.line(data1, x=data1.index, y='Close', title=f"{ticker1} Stock Prices",
# #                                    line_shape='linear', color_discrete_sequence=['#1f77b4'])
# #                     st.plotly_chart(fig1)
# #                     st.dataframe(data1)
# #
# #                 if df1.empty:
# #                     st.error(f"No data available for {ticker1}.")
# #                 else:
# #                     st.dataframe(df1)
# #                     output_filename1 = f"{ticker1}_comparison_data.xlsx"
# #                     df1.to_excel(output_filename1)
# #                     st.download_button(label=f"Download {ticker1} Data", data=open(output_filename1, 'rb').read(),
# #                                        file_name=output_filename1)
# #
# #             # Display data for second stock
# #             with col2:
# #                 st.subheader(f"{ticker2} Data")
# #                 if not data2.empty:
# #                     fig2 = px.line(data2, x=data2.index, y='Close', title=f"{ticker2} Stock Prices",
# #                                    line_shape='linear', color_discrete_sequence=['#ff7f0e'])
# #                     st.plotly_chart(fig2)
# #                     st.dataframe(data2)
# #
# #                 if df2.empty:
# #                     st.error(f"No data available for {ticker2}.")
# #                 else:
# #                     st.dataframe(df2)
# #                     output_filename2 = f"{ticker2}_comparison_data.xlsx"
# #                     df2.to_excel(output_filename2)
# #                     st.download_button(label=f"Download {ticker2} Data", data=open(output_filename2, 'rb').read(),
# #                                        file_name=output_filename2)
# #
# #             # Plot comparison graphs
# #             if not data1.empty and not data2.empty:
# #                 fig_comparison = px.line(data1, x=data1.index, y='Close',
# #                                          title=f"Comparison of {ticker1} and {ticker2}",
# #                                          line_shape='linear', color_discrete_sequence=['#1f77b4'])
# #                 fig_comparison.add_scatter(x=data2.index, y=data2['Close'], mode='lines', name=ticker2,
# #                                            line=dict(color='#ff7f0e'))
# #                 st.plotly_chart(fig_comparison)
# #
# #     # Sub-tab 2: Gap Analysis
# #     with subtab2:
# #         st.header("Gap Analysis")
# #
# #         # User input for gap analysis
# #         gap_ticker = st.text_input("Enter Ticker Symbol for Gap Analysis:", value="AAPL").upper()
# #         gap_from_date = st.date_input("Start Date for Gap Analysis:", value=pd.to_datetime("2014-01-01"),
# #                                       key='gap_from_date')
# #         gap_to_date = st.date_input("End Date for Gap Analysis:", value=pd.to_datetime("2024-01-01"), key='gap_to_date')
# #
# #         if gap_ticker:
# #             gap_data = fetch_gap_data(gap_ticker, gap_from_date, gap_to_date)
# #             if not gap_data.empty:
# #                 # Calculate weekly average prices
# #                 gap_data['Week'] = gap_data.index.to_period('W').apply(lambda r: r.start_time)
# #                 weekly_avg = gap_data.groupby('Week').agg({'Close': 'mean'}).reset_index()
# #
# #                 # Calculate gaps
# #                 weekly_avg['Gap'] = weekly_avg['Close'].diff()
# #                 fig_gap = px.line(weekly_avg, x='Week', y=['Close', 'Gap'],
# #                                   title=f"Weekly Average and Gap Analysis for {gap_ticker}",
# #                                   labels={'value': 'Price', 'Week': 'Date'},
# #                                   color_discrete_sequence=['#1f77b4', '#ff7f0e'])
# #                 st.plotly_chart(fig_gap)
# #             else:
# #                 st.error("No data available for gap analysis.")
# #
# # # Footer
# # st.markdown('<div class="footer">Powered by Naf-Byte (Nafay Ur Rehman)</div>', unsafe_allow_html=True)
# # import streamlit as st
# # from polygon import RESTClient
# # import pandas as pd
# # import plotly.express as px
# # import yfinance as yf
# #
# # # Initialize the Polygon REST client
# # API_KEY = 'y6LU1NRQtO2ogTHRIcMMxQoI2whgMPeG'  # Replace with your actual API key
# # client = RESTClient(API_KEY)
# #
# # # Set page configuration
# # st.set_page_config(page_title="Naf-YFinance - Stock Data Fetcher", layout="wide", page_icon="📈")
# #
# # # Custom CSS for a modern UI with black background
# # st.markdown(
# #     """
# #     <style>
# #     .main {
# #         background-color: #000000;
# #         padding: 20px;
# #         border-radius: 10px;
# #         box-shadow: 0px 0px 15px rgba(0, 0, 0, 0.1);
# #         font-family: 'Arial', sans-serif;
# #         color: #FFFFFF;
# #         text-align: center;
# #     }
# #     .stButton>button {
# #         background-color: #5A189A;
# #         color: #FFFFFF;
# #         font-size: 16px;
# #         padding: 10px 20px;
# #         border: none;
# #         border-radius: 5px;
# #         cursor: pointer;
# #     }
# #     .stButton>button:hover {
# #         background-color: #9D4EDD;
# #     }
# #     .stTextInput>div>div>input {
# #         background-color: #E5E5E5;
# #         color: #333333;
# #         border: 1px solid #CCCCCC;
# #         border-radius: 5px;
# #         padding: 10px;
# #     }
# #     .green-container {
# #         background-color: #DFF2BF;
# #         padding: 10px;
# #         border-radius: 5px;
# #         color: #4F8A10;
# #         font-weight: bold;
# #         margin-bottom: 15px;
# #     }
# #     h1 {
# #         font-size: 28px;
# #         margin-bottom: 10px;
# #         margin-top: 0;  /* Removed extra padding from top */
# #     }
# #     .tagline {
# #         font-size: 18px;
# #         color: #DDDDDD;
# #         margin-bottom: 10px;
# #     }
# #     .footer {
# #         position: fixed;
# #         bottom: 0;
# #         width: 100%;
# #         text-align: center;
# #         color: #DDDDDD;
# #         padding: 10px;
# #         font-size: 14px;
# #     }
# #     </style>
# #     """, unsafe_allow_html=True
# # )
# #
# # # App Title and Tagline
# # st.markdown("<h1>Naf-YFinance - Stock Data Fetcher 📈</h1>", unsafe_allow_html=True)
# # st.markdown('<p class="tagline">Download data from any stock company from symbol</p>', unsafe_allow_html=True)
# #
# # # Sidebar for User Input
# # st.sidebar.header("User Input")
# # ticker = st.sidebar.text_input("Enter Ticker Symbol (e.g., AAPL):", value="AAPL").upper()
# # multiplier = st.sidebar.number_input("Enter Multiplier (e.g., 1 for minute data):", min_value=1, value=1)
# # timespan = st.sidebar.selectbox("Select Timespan:",
# #                                 options=["second", "minute", "hour", "day", "week", "month", "quarter", "year"],
# #                                 index=0)
# # from_date = st.sidebar.date_input("Start Date:", value=pd.to_datetime("2014-01-01"))
# # to_date = st.sidebar.date_input("End Date:", value=pd.to_datetime("2024-01-01"))
# #
# #
# # # Function to fetch stock data and financials
# # def fetch_data(ticker, from_date, to_date, multiplier, timespan):
# #     try:
# #         # Fetch aggregate data based on user input
# #         aggs = client.get_aggs(
# #             ticker=ticker,
# #             multiplier=multiplier,
# #             timespan=timespan,
# #             from_=from_date.strftime('%Y-%m-%d'),
# #             to=to_date.strftime('%Y-%m-%d')
# #         )
# #         df = pd.DataFrame(aggs)
# #
# #         # Download data using yfinance for visualization
# #         stock = yf.Ticker(ticker)
# #         data = stock.history(start=from_date, end=to_date)
# #
# #         # Fetch financial data
# #         income_statement = stock.financials
# #         cash_flow = stock.cashflow
# #         balance_sheet = stock.balance_sheet  # Fetch balance sheet
# #
# #         return df, data, income_statement, cash_flow, balance_sheet
# #
# #     except Exception as e:
# #         st.error(f"An error occurred: {e}")
# #         return pd.DataFrame(), pd.DataFrame(), pd.DataFrame(), pd.DataFrame(), pd.DataFrame()
# #
# #
# # # Helper function to fetch data
# # def fetch_gap_data(ticker, from_date, to_date):
# #     try:
# #         stock = yf.Ticker(ticker)
# #         data = stock.history(start=from_date, end=to_date)
# #         return data
# #     except Exception as e:
# #         st.error(f"An error occurred: {e}")
# #         return pd.DataFrame()
# #
# #
# # # Main app
# # st.title("Stock Analysis App")
# #
# # # Create tabs for different sections
# # tab1, tab2, tab3 = st.tabs(["Stock Data", "Financial Statements", "Stock Analysis"])
# #
# # # Tab 1: Stock Data
# # with tab1:
# #     st.header("Stock Data")
# #     df, data, _, _, _ = fetch_data(ticker, from_date, to_date, multiplier, timespan)
# #
# #     if not data.empty:
# #         fig = px.line(data, x=data.index, y='Close', title=f"{ticker} Stock Prices",
# #                       line_shape='linear',
# #                       color_discrete_sequence=['#5AB834'])
# #         st.plotly_chart(fig)
# #     else:
# #         st.error("No data available for the selected ticker.")
# #
# #     if df.empty:
# #         st.error("No data available for the selected parameters. Please try different inputs.")
# #     else:
# #         df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
# #         df.set_index('timestamp', inplace=True)
# #         st.dataframe(df)
# #
# #         # Download button for Excel file
# #         output_filename = f"{ticker}_stock_data_{from_date}_to_{to_date}.xlsx"
# #         df.to_excel(output_filename, index=True)
# #         st.success(f"Data fetched successfully and saved to '{output_filename}'.")
# #         st.download_button(label="Download Excel File", data=open(output_filename, 'rb').read(),
# #                            file_name=output_filename)
# #
# # # Tab 2: Financial Statements
# # with tab2:
# #     st.header("Financial Statements")
# #     _, _, income_statement, cash_flow, balance_sheet = fetch_data(ticker, from_date, to_date, multiplier, timespan)
# #
# #     # Display Income Statement and Cash Flow
# #     if not income_statement.empty:
# #         st.subheader("Income Statement")
# #         st.dataframe(income_statement)
# #         # Download button for Income Statement
# #         income_output_filename = f"{ticker}_income_statement.xlsx"
# #         income_statement.to_excel(income_output_filename)
# #         st.download_button(label="Download Income Statement", data=open(income_output_filename, 'rb').read(),
# #                            file_name=income_output_filename)
# #     else:
# #         st.error("No income statement data available.")
# #
# #     if not cash_flow.empty:
# #         st.subheader("Cash Flow Statement")
# #         st.dataframe(cash_flow)
# #         # Download button for Cash Flow
# #         cash_flow_output_filename = f"{ticker}_cash_flow.xlsx"
# #         cash_flow.to_excel(cash_flow_output_filename)
# #         st.download_button(label="Download Cash Flow Statement", data=open(cash_flow_output_filename, 'rb').read(),
# #                            file_name=cash_flow_output_filename)
# #     else:
# #         st.error("No cash flow data available.")
# #
# #     # Display Balance Sheet
# #     if not balance_sheet.empty:
# #         st.subheader("Balance Sheet")
# #         st.dataframe(balance_sheet)
# #         # Download button for Balance Sheet
# #         balance_sheet_output_filename = f"{ticker}_balance_sheet.xlsx"
# #         balance_sheet.to_excel(balance_sheet_output_filename)
# #         st.download_button(label="Download Balance Sheet", data=open(balance_sheet_output_filename, 'rb').read(),
# #                            file_name=balance_sheet_output_filename)
# #     else:
# #         st.error("No balance sheet data available.")
# #
# # # Tab 3: Stock Analysis
# # with tab3:
# #     st.header("Stock Analysis")
# #     subtab1, subtab2 = st.tabs(["Stock Comparison", "Gap Analysis"])
# #
# #     # Sub-tab 1: Stock Comparison
# #     with subtab1:
# #         st.header("Stock Comparison")
# #
# #         # Create columns for user inputs
# #         col1, col2 = st.columns(2)
# #
# #         with col1:
# #             st.subheader("Stock 1")
# #             ticker1 = st.text_input("Enter First Ticker Symbol (e.g., AAPL):", value="AAPL").upper()
# #             multiplier1 = st.number_input("Enter Multiplier for First Ticker (e.g., 1 for minute data):", min_value=1,
# #                                           value=1, key='multiplier1')
# #             timespan1 = st.selectbox("Select Timespan for First Ticker:",
# #                                      options=["second", "minute", "hour", "day", "week", "month", "quarter", "year"],
# #                                      index=0, key='timespan1')
# #             from_date1 = st.date_input("Start Date for First Ticker:", value=pd.to_datetime("2014-01-01"),
# #                                        key='from_date1')
# #             to_date1 = st.date_input("End Date for First Ticker:", value=pd.to_datetime("2024-01-01"), key='to_date1')
# #
# #         with col2:
# #             st.subheader("Stock 2")
# #             ticker2 = st.text_input("Enter Second Ticker Symbol (e.g., MSFT):", value="MSFT").upper()
# #             multiplier2 = st.number_input("Enter Multiplier for Second Ticker (e.g., 1 for minute data):", min_value=1,
# #                                           value=1, key='multiplier2')
# #             timespan2 = st.selectbox("Select Timespan for Second Ticker:",
# #                                      options=["second", "minute", "hour", "day", "week", "month", "quarter", "year"],
# #                                      index=0, key='timespan2')
# #             from_date2 = st.date_input("Start Date for Second Ticker:", value=pd.to_datetime("2014-01-01"),
# #                                        key='from_date2')
# #             to_date2 = st.date_input("End Date for Second Ticker:", value=pd.to_datetime("2024-01-01"), key='to_date2')
# #
# #         if ticker1 and ticker2:
# #             df1, data1, _, _, _ = fetch_data(ticker1, from_date1, to_date1, multiplier1, timespan1)
# #             df2, data2, _, _, _ = fetch_data(ticker2, from_date2, to_date2, multiplier2, timespan2)
# #
# #             col1, col2 = st.columns(2)
# #
# #             # Display data for first stock
# #             with col1:
# #                 st.subheader(f"{ticker1} Data")
# #                 if not data1.empty:
# #                     fig1 = px.line(data1, x=data1.index, y='Close', title=f"{ticker1} Stock Prices",
# #                                    line_shape='linear', color_discrete_sequence=['#1f77b4'])
# #                     st.plotly_chart(fig1)
# #                     st.dataframe(data1)
# #
# #                 if df1.empty:
# #                     st.error(f"No data available for {ticker1}.")
# #                 else:
# #                     st.dataframe(df1)
# #                     output_filename1 = f"{ticker1}_comparison_data.xlsx"
# #                     df1.to_excel(output_filename1)
# #                     st.download_button(label=f"Download {ticker1} Data", data=open(output_filename1, 'rb').read(),
# #                                        file_name=output_filename1)
# #
# #             # Display data for second stock
# #             with col2:
# #                 st.subheader(f"{ticker2} Data")
# #                 if not data2.empty:
# #                     fig2 = px.line(data2, x=data2.index, y='Close', title=f"{ticker2} Stock Prices",
# #                                    line_shape='linear', color_discrete_sequence=['#ff7f0e'])
# #                     st.plotly_chart(fig2)
# #                     st.dataframe(data2)
# #
# #                 if df2.empty:
# #                     st.error(f"No data available for {ticker2}.")
# #                 else:
# #                     st.dataframe(df2)
# #                     output_filename2 = f"{ticker2}_comparison_data.xlsx"
# #                     df2.to_excel(output_filename2)
# #                     st.download_button(label=f"Download {ticker2} Data", data=open(output_filename2, 'rb').read(),
# #                                        file_name=output_filename2)
# #
# #             # Plot comparison graphs
# #             if not data1.empty and not data2.empty:
# #                 fig_comparison = px.line(data1, x=data1.index, y='Close',
# #                                          title=f"Comparison of {ticker1} and {ticker2}",
# #                                          line_shape='linear', color_discrete_sequence=['#1f77b4'])
# #                 fig_comparison.add_scatter(x=data2.index, y=data2['Close'], mode='lines', name=ticker2,
# #                                            line=dict(color='#ff7f0e'))
# #                 st.plotly_chart(fig_comparison)
# #
# #     # Sub-tab 2: Gap Analysis
# #     with subtab2:
# #         st.header("Gap Analysis")
# #
# #         # User input for gap analysis
# #         gap_ticker = st.text_input("Enter Ticker Symbol for Gap Analysis:", value="AAPL").upper()
# #         gap_from_date = st.date_input("Start Date for Gap Analysis:", value=pd.to_datetime("2014-01-01"),
# #                                       key='gap_from_date')
# #         gap_to_date = st.date_input("End Date for Gap Analysis:", value=pd.to_datetime("2024-01-01"), key='gap_to_date')
# #
# #         if gap_ticker:
# #             gap_data = fetch_gap_data(gap_ticker, gap_from_date, gap_to_date)
# #             if not gap_data.empty:
# #                 # Convert index to weekly periods and extract start time
# #                 gap_data['Week'] = gap_data.index.to_period('W').start_time
# #                 weekly_avg = gap_data.groupby('Week').agg({'Close': 'mean'}).reset_index()
# #
# #                 # Calculate gaps
# #                 weekly_avg['Gap'] = weekly_avg['Close'].diff()
# #                 fig_gap = px.line(weekly_avg, x='Week', y=['Close', 'Gap'],
# #                                   title=f"Weekly Average and Gap Analysis for {gap_ticker}",
# #                                   labels={'value': 'Price', 'Week': 'Date'},
# #                                   color_discrete_sequence=['#1f77b4', '#ff7f0e'])
# #                 st.plotly_chart(fig_gap)
# #             else:
# #                 st.error("No data available for gap analysis.")
# #
# # # Footer
# # st.markdown('<div class="footer">Powered by Naf-Byte (Nafay Ur Rehman)</div>', unsafe_allow_html=True)
# # import streamlit as st
# # from polygon import RESTClient
# # import pandas as pd
# # import plotly.express as px
# # import yfinance as yf
# #
# # # Initialize the Polygon REST client
# # API_KEY = 'y6LU1NRQtO2ogTHRIcMMxQoI2whgMPeG'  # Replace with your actual API key
# # client = RESTClient(API_KEY)
# #
# # # Set page configuration
# # st.set_page_config(page_title="Naf-YFinance - Stock Data Fetcher", layout="wide", page_icon="📈")
# #
# # # Custom CSS for a modern UI with black background
# # st.markdown(
# #     """
# #     <style>
# #     .main {
# #         background-color: #000000;
# #         padding: 20px;
# #         border-radius: 10px;
# #         box-shadow: 0px 0px 15px rgba(0, 0, 0, 0.1);
# #         font-family: 'Arial', sans-serif;
# #         color: #FFFFFF;
# #         text-align: center;
# #     }
# #     .stButton>button {
# #         background-color: #5A189A;
# #         color: #FFFFFF;
# #         font-size: 16px;
# #         padding: 10px 20px;
# #         border: none;
# #         border-radius: 5px;
# #         cursor: pointer;
# #     }
# #     .stButton>button:hover {
# #         background-color: #9D4EDD;
# #     }
# #     .stTextInput>div>div>input {
# #         background-color: #E5E5E5;
# #         color: #333333;
# #         border: 1px solid #CCCCCC;
# #         border-radius: 5px;
# #         padding: 10px;
# #     }
# #     .green-container {
# #         background-color: #DFF2BF;
# #         padding: 10px;
# #         border-radius: 5px;
# #         color: #4F8A10;
# #         font-weight: bold;
# #         margin-bottom: 15px;
# #     }
# #     h1 {
# #         font-size: 28px;
# #         margin-bottom: 10px;
# #         margin-top: 0;  /* Removed extra padding from top */
# #     }
# #     .tagline {
# #         font-size: 18px;
# #         color: #DDDDDD;
# #         margin-bottom: 10px;
# #     }
# #     .footer {
# #         position: fixed;
# #         bottom: 0;
# #         width: 100%;
# #         text-align: center;
# #         color: #DDDDDD;
# #         padding: 10px;
# #         font-size: 14px;
# #     }
# #     </style>
# #     """, unsafe_allow_html=True
# # )
# #
# # # App Title and Tagline
# # st.markdown("<h1>Naf-YFinance - Stock Data Fetcher 📈</h1>", unsafe_allow_html=True)
# # st.markdown('<p class="tagline">Download data from any stock company from symbol</p>', unsafe_allow_html=True)
# #
# # # Sidebar for User Input
# # st.sidebar.header("User Input")
# # ticker = st.sidebar.text_input("Enter Ticker Symbol (e.g., AAPL):", value="AAPL").upper()
# # multiplier = st.sidebar.number_input("Enter Multiplier (e.g., 1 for minute data):", min_value=1, value=1)
# # timespan = st.sidebar.selectbox("Select Timespan:",
# #                                 options=["second", "minute", "hour", "day", "week", "month", "quarter", "year"],
# #                                 index=0)
# # from_date = st.sidebar.date_input("Start Date:", value=pd.to_datetime("2014-01-01"))
# # to_date = st.sidebar.date_input("End Date:", value=pd.to_datetime("2024-01-01"))
# #
# #
# # # Function to fetch stock data and financials
# # def fetch_data(ticker, from_date, to_date, multiplier, timespan):
# #     try:
# #         # Fetch aggregate data based on user input
# #         aggs = client.get_aggs(
# #             ticker=ticker,
# #             multiplier=multiplier,
# #             timespan=timespan,
# #             from_=from_date.strftime('%Y-%m-%d'),
# #             to=to_date.strftime('%Y-%m-%d')
# #         )
# #         df = pd.DataFrame(aggs)
# #
# #         # Download data using yfinance for visualization
# #         stock = yf.Ticker(ticker)
# #         data = stock.history(start=from_date, end=to_date)
# #
# #         # Fetch financial data
# #         income_statement = stock.financials
# #         cash_flow = stock.cashflow
# #         balance_sheet = stock.balance_sheet  # Fetch balance sheet
# #
# #         return df, data, income_statement, cash_flow, balance_sheet
# #
# #     except Exception as e:
# #         st.error(f"An error occurred: {e}")
# #         return pd.DataFrame(), pd.DataFrame(), pd.DataFrame(), pd.DataFrame(), pd.DataFrame()
# # # Helper function to fetch data
# # def fetch_gap_data(ticker, from_date, to_date):
# #     try:
# #         stock = yf.Ticker(ticker)
# #         data = stock.history(start=from_date, end=to_date)
# #         return data
# #     except Exception as e:
# #         st.error(f"An error occurred: {e}")
# #         return pd.DataFrame()
# #
# #
# # # Main app
# # st.title("Stock Analysis App")
# #
# # # Create tabs for different sections
# # tab1, tab2, tab3 = st.tabs(["Stock Data", "Financial Statements", "Stock Analysis"])
# #
# # # Tab 1: Stock Data
# # with tab1:
# #     st.header("Stock Data")
# #     df, data, _, _, _ = fetch_data(ticker, from_date, to_date, multiplier, timespan)
# #
# #     if not data.empty:
# #         fig = px.line(data, x=data.index, y='Close', title=f"{ticker} Stock Prices",
# #                       line_shape='linear',
# #                       color_discrete_sequence=['#5AB834'])
# #         st.plotly_chart(fig)
# #     else:
# #         st.error("No data available for the selected ticker.")
# #
# #     if df.empty:
# #         st.error("No data available for the selected parameters. Please try different inputs.")
# #     else:
# #         df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
# #         df.set_index('timestamp', inplace=True)
# #         st.dataframe(df)
# #
# #         # Download button for Excel file
# #         output_filename = f"{ticker}_stock_data_{from_date}_to_{to_date}.xlsx"
# #         df.to_excel(output_filename, index=True)
# #         st.success(f"Data fetched successfully and saved to '{output_filename}'.")
# #         st.download_button(label="Download Excel File", data=open(output_filename, 'rb').read(),
# #                            file_name=output_filename)
# #
# # # Tab 2: Financial Statements
# # with tab2:
# #     st.header("Financial Statements")
# #     _, _, income_statement, cash_flow, balance_sheet = fetch_data(ticker, from_date, to_date, multiplier, timespan)
# #
# #     # Display Income Statement and Cash Flow
# #     if not income_statement.empty:
# #         st.subheader("Income Statement")
# #         st.dataframe(income_statement)
# #         # Download button for Income Statement
# #         income_output_filename = f"{ticker}_income_statement.xlsx"
# #         income_statement.to_excel(income_output_filename)
# #         st.download_button(label="Download Income Statement", data=open(income_output_filename, 'rb').read(),
# #                            file_name=income_output_filename)
# #     else:
# #         st.error("No income statement data available.")
# #
# #     if not cash_flow.empty:
# #         st.subheader("Cash Flow Statement")
# #         st.dataframe(cash_flow)
# #         # Download button for Cash Flow
# #         cash_flow_output_filename = f"{ticker}_cash_flow.xlsx"
# #         cash_flow.to_excel(cash_flow_output_filename)
# #         st.download_button(label="Download Cash Flow Statement", data=open(cash_flow_output_filename, 'rb').read(),
# #                            file_name=cash_flow_output_filename)
# #     else:
# #         st.error("No cash flow data available.")
# #
# #     # Display Balance Sheet
# #     if not balance_sheet.empty:
# #         st.subheader("Balance Sheet")
# #         st.dataframe(balance_sheet)
# #         # Download button for Balance Sheet
# #         balance_sheet_output_filename = f"{ticker}_balance_sheet.xlsx"
# #         balance_sheet.to_excel(balance_sheet_output_filename)
# #         st.download_button(label="Download Balance Sheet", data=open(balance_sheet_output_filename, 'rb').read(),
# #                            file_name=balance_sheet_output_filename)
# #     else:
# #         st.error("No balance sheet data available.")
# #
# # # Tab 3: Stock Analysis
# # with tab3:
# #     st.header("Stock Analysis")
# #     subtab1, subtab2 = st.tabs(["Stock Comparison", "Gap Analysis"])
# #
# #     # Sub-tab 1: Stock Comparison
# #     with subtab1:
# #         st.header("Stock Comparison")
# #
# #         # User inputs for stock comparison
# #         ticker1 = st.text_input("Enter First Ticker Symbol (e.g., AAPL):", value="AAPL").upper()
# #         ticker2 = st.text_input("Enter Second Ticker Symbol (e.g., MSFT):", value="MSFT").upper()
# #
# #         multiplier1 = st.number_input("Enter Multiplier for First Ticker (e.g., 1 for minute data):", min_value=1,
# #                                       value=1, key='multiplier1')
# #         multiplier2 = st.number_input("Enter Multiplier for Second Ticker (e.g., 1 for minute data):", min_value=1,
# #                                       value=1, key='multiplier2')
# #
# #         timespan1 = st.selectbox("Select Timespan for First Ticker:",
# #                                  options=["second", "minute", "hour", "day", "week", "month", "quarter", "year"],
# #                                  index=0, key='timespan1')
# #         timespan2 = st.selectbox("Select Timespan for Second Ticker:",
# #                                  options=["second", "minute", "hour", "day", "week", "month", "quarter", "year"],
# #                                  index=0, key='timespan2')
# #
# #         from_date1 = st.date_input("Start Date for First Ticker:", value=pd.to_datetime("2014-01-01"), key='from_date1')
# #         to_date1 = st.date_input("End Date for First Ticker:", value=pd.to_datetime("2024-01-01"), key='to_date1')
# #
# #         from_date2 = st.date_input("Start Date for Second Ticker:", value=pd.to_datetime("2014-01-01"), key='from_date2')
# #         to_date2 = st.date_input("End Date for Second Ticker:", value=pd.to_datetime("2024-01-01"), key='to_date2')
# #
# #         if ticker1 and ticker2:
# #             df1, data1, _, _, _ = fetch_data(ticker1, from_date1, to_date1, multiplier1, timespan1)
# #             df2, data2, _, _, _ = fetch_data(ticker2, from_date2, to_date2, multiplier2, timespan2)
# #
# #             if not data1.empty and not data2.empty:
# #                 # Create comparison figures
# #                 fig1 = px.line(data1, x=data1.index, y='Close', title=f"{ticker1} Stock Prices",
# #                                line_shape='linear', color_discrete_sequence=['#5AB834'])
# #                 fig2 = px.line(data2, x=data2.index, y='Close', title=f"{ticker2} Stock Prices",
# #                                line_shape='linear', color_discrete_sequence=['#FF5733'])
# #
# #                 col1, col2 = st.columns(2)
# #                 with col1:
# #                     st.plotly_chart(fig1)
# #                     st.write(f"**{ticker1} Summary**")
# #                     st.write(f"Highest Closing Price: ${data1['Close'].max():.2f}")
# #                     st.write(f"Lowest Closing Price: ${data1['Close'].min():.2f}")
# #                 with col2:
# #                     st.plotly_chart(fig2)
# #                     st.write(f"**{ticker2} Summary**")
# #                     st.write(f"Highest Closing Price: ${data2['Close'].max():.2f}")
# #                     st.write(f"Lowest Closing Price: ${data2['Close'].min():.2f}")
# #
# #                 # Summary table comparison
# #                 summary_data = {
# #                     "Ticker": [ticker1, ticker2],
# #                     "Highest Closing Price": [data1['Close'].max(), data2['Close'].max()],
# #                     "Lowest Closing Price": [data1['Close'].min(), data2['Close'].min()]
# #                 }
# #                 summary_df = pd.DataFrame(summary_data)
# #                 st.subheader("Comparison Summary")
# #                 st.dataframe(summary_df)
# #             else:
# #                 st.error("No data available for one or both of the tickers.")
# #
# #     # Sub-tab 2: Gap Analysis
# #     with subtab2:
# #         st.header("Gap Analysis")
# #
# #         # User input for gap analysis
# #         gap_ticker = st.text_input("Enter Ticker Symbol for Gap Analysis:", value="AAPL").upper()
# #         gap_from_date = st.date_input("Start Date for Gap Analysis:", value=pd.to_datetime("2014-01-01"), key='gap_from_date')
# #         gap_to_date = st.date_input("End Date for Gap Analysis:", value=pd.to_datetime("2024-01-01"), key='gap_to_date')
# #
# #         if gap_ticker:
# #             gap_data = fetch_gap_data(gap_ticker, gap_from_date, gap_to_date)
# #             if not gap_data.empty:
# #                 # Convert index to weekly periods and extract start time
# #                 gap_data['Week'] = gap_data.index.to_period('W').start_time
# #                 weekly_avg = gap_data.groupby('Week').agg({'Close': 'mean'}).reset_index()
# #
# #                 # Calculate gaps
# #                 weekly_avg['Gap'] = weekly_avg['Close'].diff()
# #                 fig_gap = px.line(weekly_avg, x='Week', y=['Close', 'Gap'], title=f"Weekly Average and Gap Analysis for {gap_ticker}",
# #                                   labels={'value': 'Price', 'Week': 'Date'},
# #                                   color_discrete_sequence=['#1f77b4', '#ff7f0e'])
# #                 st.plotly_chart(fig_gap)
# #
# #                 # Summary table for Gap Analysis
# #                 gap_summary_data = {
# #                     "Week": weekly_avg['Week'].astype(str),
# #                     "Average Price": weekly_avg['Close'],
# #                     "Gap": weekly_avg['Gap']
# #                 }
# #                 gap_summary_df = pd.DataFrame(gap_summary_data)
# #                 st.subheader("Gap Analysis Summary")
# #                 st.dataframe(gap_summary_df)
# #             else:
# #                 st.error("No data available for gap analysis.")
# #
# # # Footer
# # st.markdown('<div class="footer">Powered by Naf-Byte (Nafay Ur Rehman)</div>', unsafe_allow_html=True)
# # import streamlit as st
# # from polygon import RESTClient
# # import pandas as pd
# # import plotly.express as px
# # import yfinance as yf
# #
# # # Initialize the Polygon REST client
# # API_KEY = 'y6LU1NRQtO2ogTHRIcMMxQoI2whgMPeG'  # Replace with your actual API key
# # client = RESTClient(API_KEY)
# #
# # # Set page configuration
# # st.set_page_config(page_title="Naf-YFinance - Stock Data Fetcher", layout="wide", page_icon="📈")
# #
# # # Custom CSS for a modern UI with black background
# # st.markdown(
# #     """
# #     <style>
# #     .main {
# #         background-color: #000000;
# #         padding: 20px;
# #         border-radius: 10px;
# #         box-shadow: 0px 0px 15px rgba(0, 0, 0, 0.1);
# #         font-family: 'Arial', sans-serif;
# #         color: #FFFFFF;
# #         text-align: center;
# #     }
# #     .stButton>button {
# #         background-color: #5A189A;
# #         color: #FFFFFF;
# #         font-size: 16px;
# #         padding: 10px 20px;
# #         border: none;
# #         border-radius: 5px;
# #         cursor: pointer;
# #     }
# #     .stButton>button:hover {
# #         background-color: #9D4EDD;
# #     }
# #     .stTextInput>div>div>input {
# #         background-color: #E5E5E5;
# #         color: #333333;
# #         border: 1px solid #CCCCCC;
# #         border-radius: 5px;
# #         padding: 10px;
# #     }
# #     .input-container {
# #         display: flex;
# #         justify-content: center;
# #         align-items: center;
# #         gap: 20px;
# #         flex-wrap: wrap;
# #     }
# #     .input-container div {
# #         flex: 1;
# #         min-width: 200px;
# #     }
# #     .green-container {
# #         background-color: #DFF2BF;
# #         padding: 10px;
# #         border-radius: 5px;
# #         color: #4F8A10;
# #         font-weight: bold;
# #         margin-bottom: 15px;
# #     }
# #     h1 {
# #         font-size: 28px;
# #         margin-bottom: 10px;
# #         margin-top: 0;  /* Removed extra padding from top */
# #     }
# #     .tagline {
# #         font-size: 18px;
# #         color: #DDDDDD;
# #         margin-bottom: 10px;
# #     }
# #     .footer {
# #         position: fixed;
# #         bottom: 0;
# #         width: 100%;
# #         text-align: center;
# #         color: #DDDDDD;
# #         padding: 10px;
# #         font-size: 14px;
# #     }
# #     </style>
# #     """, unsafe_allow_html=True
# # )
# #
# # # App Title and Tagline
# # st.markdown("<h1>Naf-YFinance - Stock Data Fetcher 📈</h1>", unsafe_allow_html=True)
# # st.markdown('<p class="tagline">Download data from any stock company from symbol</p>', unsafe_allow_html=True)
# #
# # # Sidebar for User Input
# # st.sidebar.header("User Input")
# # ticker = st.sidebar.text_input("Enter Ticker Symbol (e.g., AAPL):", value="AAPL").upper()
# # multiplier = st.sidebar.number_input("Enter Multiplier (e.g., 1 for minute data):", min_value=1, value=1)
# # timespan = st.sidebar.selectbox("Select Timespan:",
# #                                 options=["second", "minute", "hour", "day", "week", "month", "quarter", "year"],
# #                                 index=0)
# # from_date = st.sidebar.date_input("Start Date:", value=pd.to_datetime("2014-01-01"))
# # to_date = st.sidebar.date_input("End Date:", value=pd.to_datetime("2024-01-01"))
# #
# # # Function to fetch stock data and financials
# # def fetch_data(ticker, from_date, to_date, multiplier, timespan):
# #     try:
# #         # Fetch aggregate data based on user input
# #         aggs = client.get_aggs(
# #             ticker=ticker,
# #             multiplier=multiplier,
# #             timespan=timespan,
# #             from_=from_date.strftime('%Y-%m-%d'),
# #             to=to_date.strftime('%Y-%m-%d')
# #         )
# #         df = pd.DataFrame(aggs)
# #
# #         # Download data using yfinance for visualization
# #         stock = yf.Ticker(ticker)
# #         data = stock.history(start=from_date, end=to_date)
# #
# #         # Fetch financial data
# #         income_statement = stock.financials
# #         cash_flow = stock.cashflow
# #         balance_sheet = stock.balance_sheet  # Fetch balance sheet
# #
# #         return df, data, income_statement, cash_flow, balance_sheet
# #
# #     except Exception as e:
# #         st.error(f"An error occurred: {e}")
# #         return pd.DataFrame(), pd.DataFrame(), pd.DataFrame(), pd.DataFrame(), pd.DataFrame()
# # # Helper function to fetch data
# # def fetch_gap_data(ticker, from_date, to_date):
# #     try:
# #         stock = yf.Ticker(ticker)
# #         data = stock.history(start=from_date, end=to_date)
# #         return data
# #     except Exception as e:
# #         st.error(f"An error occurred: {e}")
# #         return pd.DataFrame()
# #
# #
# # # Main app
# # st.title("Stock Analysis App")
# #
# # # Create tabs for different sections
# # tab1, tab2, tab3 = st.tabs(["Stock Data", "Financial Statements", "Stock Analysis"])
# #
# # # Tab 1: Stock Data
# # with tab1:
# #     st.header("Stock Data")
# #     df, data, _, _, _ = fetch_data(ticker, from_date, to_date, multiplier, timespan)
# #
# #     if not data.empty:
# #         fig = px.line(data, x=data.index, y='Close', title=f"{ticker} Stock Prices",
# #                       line_shape='linear',
# #                       color_discrete_sequence=['#5AB834'])
# #         st.plotly_chart(fig)
# #     else:
# #         st.error("No data available for the selected ticker.")
# #
# #     if df.empty:
# #         st.error("No data available for the selected parameters. Please try different inputs.")
# #     else:
# #         df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
# #         df.set_index('timestamp', inplace=True)
# #         st.dataframe(df)
# #
# #         # Download button for Excel file
# #         output_filename = f"{ticker}_stock_data_{from_date}_to_{to_date}.xlsx"
# #         df.to_excel(output_filename, index=True)
# #         st.success(f"Data fetched successfully and saved to '{output_filename}'.")
# #         st.download_button(label="Download Excel File", data=open(output_filename, 'rb').read(),
# #                            file_name=output_filename)
# #
# # # Tab 2: Financial Statements
# # with tab2:
# #     st.header("Financial Statements")
# #     _, _, income_statement, cash_flow, balance_sheet = fetch_data(ticker, from_date, to_date, multiplier, timespan)
# #
# #     # Display Income Statement and Cash Flow
# #     if not income_statement.empty:
# #         st.subheader("Income Statement")
# #         st.dataframe(income_statement)
# #         # Download button for Income Statement
# #         income_output_filename = f"{ticker}_income_statement.xlsx"
# #         income_statement.to_excel(income_output_filename)
# #         st.download_button(label="Download Income Statement", data=open(income_output_filename, 'rb').read(),
# #                            file_name=income_output_filename)
# #     else:
# #         st.error("No income statement data available.")
# #
# #     if not cash_flow.empty:
# #         st.subheader("Cash Flow Statement")
# #         st.dataframe(cash_flow)
# #         # Download button for Cash Flow
# #         cash_flow_output_filename = f"{ticker}_cash_flow.xlsx"
# #         cash_flow.to_excel(cash_flow_output_filename)
# #         st.download_button(label="Download Cash Flow Statement", data=open(cash_flow_output_filename, 'rb').read(),
# #                            file_name=cash_flow_output_filename)
# #     else:
# #         st.error("No cash flow data available.")
# #
# #     # Display Balance Sheet
# #     if not balance_sheet.empty:
# #         st.subheader("Balance Sheet")
# #         st.dataframe(balance_sheet)
# #         # Download button for Balance Sheet
# #         balance_sheet_output_filename = f"{ticker}_balance_sheet.xlsx"
# #         balance_sheet.to_excel(balance_sheet_output_filename)
# #         st.download_button(label="Download Balance Sheet", data=open(balance_sheet_output_filename, 'rb').read(),
# #                            file_name=balance_sheet_output_filename)
# #     else:
# #         st.error("No balance sheet data available.")
# #
# # # Tab 3: Stock Analysis
# # with tab3:
# #     st.header("Stock Analysis")
# #     subtab1, subtab2 = st.tabs(["Stock Comparison", "Gap Analysis"])
# #
# #     # Sub-tab 1: Stock Comparison
# #     with subtab1:
# #         st.header("Stock Comparison")
# #
# #         # User inputs for stock comparison
# #         st.markdown('<div class="input-container">', unsafe_allow_html=True)
# #         col1, col2 = st.columns(2)
# #
# #         with col1:
# #             ticker1 = st.text_input("Enter First Ticker Symbol (e.g., AAPL):", value="AAPL").upper()
# #             multiplier1 = st.number_input("Enter Multiplier for First Ticker (e.g., 1 for minute data):", min_value=1, value=1, key='multiplier1')
# #             timespan1 = st.selectbox("Select Timespan for First Ticker:",
# #                                      options=["second", "minute", "hour", "day", "week", "month", "quarter", "year"],
# #                                      index=0, key='timespan1')
# #             from_date1 = st.date_input("Start Date for First Ticker:", value=pd.to_datetime("2014-01-01"), key='from_date1')
# #             to_date1 = st.date_input("End Date for First Ticker:", value=pd.to_datetime("2024-01-01"), key='to_date1')
# #
# #         with col2:
# #             ticker2 = st.text_input("Enter Second Ticker Symbol (e.g., MSFT):", value="MSFT").upper()
# #             multiplier2 = st.number_input("Enter Multiplier for Second Ticker (e.g., 1 for minute data):", min_value=1, value=1, key='multiplier2')
# #             timespan2 = st.selectbox("Select Timespan for Second Ticker:",
# #                                      options=["second", "minute", "hour", "day", "week", "month", "quarter", "year"],
# #                                      index=0, key='timespan2')
# #             from_date2 = st.date_input("Start Date for Second Ticker:", value=pd.to_datetime("2014-01-01"), key='from_date2')
# #             to_date2 = st.date_input("End Date for Second Ticker:", value=pd.to_datetime("2024-01-01"), key='to_date2')
# #
# #         st.markdown('</div>', unsafe_allow_html=True)
# #
# #         if ticker1 and ticker2:
# #             df1, data1, _, _, _ = fetch_data(ticker1, from_date1, to_date1, multiplier1, timespan1)
# #             df2, data2, _, _, _ = fetch_data(ticker2, from_date2, to_date2, multiplier2, timespan2)
# #
# #             if not data1.empty and not data2.empty:
# #                 # Create comparison figures
# #                 fig1 = px.line(data1, x=data1.index, y='Close', title=f"{ticker1} Stock Prices",
# #                                line_shape='linear', color_discrete_sequence=['#5AB834'])
# #                 fig2 = px.line(data2, x=data2.index, y='Close', title=f"{ticker2} Stock Prices",
# #                                line_shape='linear', color_discrete_sequence=['#FF5733'])
# #
# #                 col1, col2 = st.columns(2)
# #                 with col1:
# #                     st.plotly_chart(fig1)
# #                     st.write(f"**{ticker1} Summary**")
# #                     st.write(f"Highest Closing Price: ${data1['Close'].max():.2f}")
# #                     st.write(f"Lowest Closing Price: ${data1['Close'].min():.2f}")
# #                 with col2:
# #                     st.plotly_chart(fig2)
# #                     st.write(f"**{ticker2} Summary**")
# #                     st.write(f"Highest Closing Price: ${data2['Close'].max():.2f}")
# #                     st.write(f"Lowest Closing Price: ${data2['Close'].min():.2f}")
# #
# #                 # Summary table comparison
# #                 summary_data = {
# #                     "Ticker": [ticker1, ticker2],
# #                     "Highest Closing Price": [data1['Close'].max(), data2['Close'].max()],
# #                     "Lowest Closing Price": [data1['Close'].min(), data2['Close'].min()]
# #                 }
# #                 summary_df = pd.DataFrame(summary_data)
# #                 st.subheader("Comparison Summary")
# #                 st.dataframe(summary_df)
# #             else:
# #                 st.error("No data available for one or both of the tickers.")
# #
# #     # Sub-tab 2: Gap Analysis
# #     with subtab2:
# #         st.header("Gap Analysis")
# #
# #         # User input for gap analysis with centered alignment
# #         st.markdown('<div class="input-container">', unsafe_allow_html=True)
# #         gap_ticker = st.text_input("Enter Ticker Symbol for Gap Analysis:", value="AAPL").upper()
# #         gap_from_date = st.date_input("Start Date for Gap Analysis:", value=pd.to_datetime("2014-01-01"), key='gap_from_date')
# #         gap_to_date = st.date_input("End Date for Gap Analysis:", value=pd.to_datetime("2024-01-01"), key='gap_to_date')
# #         st.markdown('</div>', unsafe_allow_html=True)
# #
# #         if gap_ticker:
# #             gap_data = fetch_gap_data(gap_ticker, gap_from_date, gap_to_date)
# #             if not gap_data.empty:
# #                 # Convert index to weekly periods and extract start time
# #                 gap_data['Week'] = gap_data.index.to_period('W').start_time
# #                 weekly_avg = gap_data.groupby('Week').agg({'Close': 'mean'}).reset_index()
# #
# #                 # Calculate gaps
# #                 weekly_avg['Gap'] = weekly_avg['Close'].diff()
# #                 fig_gap = px.line(weekly_avg, x='Week', y=['Close', 'Gap'], title=f"Weekly Average and Gap Analysis for {gap_ticker}",
# #                                   labels={'value': 'Price', 'Week': 'Date'},
# #                                   color_discrete_sequence=['#1f77b4', '#ff7f0e'])
# #                 st.plotly_chart(fig_gap)
# #
# #                 # Summary table for Gap Analysis
# #                 gap_summary_data = {
# #                     "Week": weekly_avg['Week'].astype(str),
# #                     "Average Price": weekly_avg['Close'],
# #                     "Gap": weekly_avg['Gap']
# #                 }
# #                 gap_summary_df = pd.DataFrame(gap_summary_data)
# #                 st.subheader("Gap Analysis Summary")
# #                 st.dataframe(gap_summary_df)
# #             else:
# #                 st.error("No data available for gap analysis.")
# #
# # # Footer
# # st.markdown('<div class="footer">Powered by Naf-Byte (Nafay Ur Rehman)</div>', unsafe_allow_html=True)
# import streamlit as st
# from polygon import RESTClient
# import pandas as pd
# import plotly.express as px
# import yfinance as yf
# import plotly.express as px
# import plotly.graph_objects as go
# from io import BytesIO
# import matplotlib.pyplot as plt
# import base64



# # Initialize the Polygon REST client
# API_KEY = 'y6LU1NRQtO2ogTHRIcMMxQoI2whgMPeG'  # Replace with your actual API key
# client = RESTClient(API_KEY)

# # Set page configuration
# st.set_page_config(page_title="Naf-YFinance - Stock Data Fetcher", layout="wide", page_icon="📈")



# # Custom CSS for a modern UI with black background
# st.markdown(
#     """
#     <style>
#     .main {
#         background-color: #000000;
#         padding: 20px;
#         border-radius: 10px;
#         box-shadow: 0px 0px 15px rgba(0, 0, 0, 0.1);
#         font-family: 'Arial', sans-serif;
#         color: #FFFFFF;
#         text-align: center;
#     }
#     .stButton>button {
#         background-color: #5A189A;
#         color: #FFFFFF;
#         font-size: 16px;
#         padding: 10px 20px;
#         border: none;
#         border-radius: 5px;
#         cursor: pointer;
#     }
#     .stButton>button:hover {
#         background-color: #9D4EDD;
#     }
#     .stTextInput>div>div>input {
#         background-color: #E5E5E5;
#         color: #333333;
#         border: 1px solid #CCCCCC;
#         border-radius: 5px;
#         padding: 10px;
#     }
#     .input-container {
#         display: flex;
#         justify-content: center;
#         align-items: center;
#         gap: 20px;
#         flex-wrap: wrap;
#     }
#     .input-container div {
#         flex: 1;
#         min-width: 200px;
#     }
#     .green-container {
#         background-color: #DFF2BF;
#         padding: 10px;
#         border-radius: 5px;
#         color: #4F8A10;
#         font-weight: bold;
#         margin-bottom: 15px;
#     }
#     h1 {
#         font-size: 36px;  /* Increased the size of the main heading */
#         margin-bottom: 10px;
#         margin-top: 0;  /* Removed extra padding from the top */
#     }
#     .tagline {
#         font-size: 18px;
#         color: #DDDDDD;
#         margin-bottom: 10px;
#     }
#     .footer {
#         position: fixed;
#         bottom: 0;
#         width: 100%;
#         text-align: center;
#         color: #DDDDDD;
#         padding: 10px;
#         font-size: 14px;
#     }
#     </style>
#     """, unsafe_allow_html=True
# )



# # App Title and Tagline
# st.markdown("<h1>Naf-FinTrack Engine📈</h1>", unsafe_allow_html=True)
# # Naf - YFinance - Track S & P - 500 Stock Data with no hustle
# # st.markdown("""
# # <h1><img src= "Naf-YFinance Tracker.png" style="width:30px; vertical-align:middle; margin-right:10px;"> Naf-YFinance - Stock Data Fetcher</h1>
# # """, unsafe_allow_html=True)
# st.markdown('<p class="tagline">Efficient Data Retrieval and Analysis for Investors with Advanced S&P-500 Stock Insights from Yahoo Finance 📈</p>', unsafe_allow_html=True)

# # Sidebar for User Input
# st.sidebar.header("User Input")
# ticker = st.sidebar.text_input("Enter Ticker Symbol (e.g., AAPL):", value="AAPL").upper()
# multiplier = st.sidebar.number_input("Enter Multiplier (e.g., 1 for minute data):", min_value=1, value=1)
# timespan = st.sidebar.selectbox("Select Timespan:",
#                                 options=["second", "minute", "hour", "day", "week", "month", "quarter", "year"],
#                                 index=0)
# from_date = st.sidebar.date_input("Start Date:", value=pd.to_datetime("2014-01-01"))
# to_date = st.sidebar.date_input("End Date:", value=pd.to_datetime("2024-01-01"))

# # Function to fetch stock data and financials
# def fetch_data(ticker, from_date, to_date, multiplier, timespan):
#     try:
#         # Fetch aggregate data based on user input
#         aggs = client.get_aggs(
#             ticker=ticker,
#             multiplier=multiplier,
#             timespan=timespan,
#             from_=from_date.strftime('%Y-%m-%d'),
#             to=to_date.strftime('%Y-%m-%d')
#         )
#         df = pd.DataFrame(aggs)

#         # Download data using yfinance for visualization
#         stock = yf.Ticker(ticker)
#         data = stock.history(start=from_date, end=to_date)

#         # Fetch financial data
#         income_statement = stock.financials
#         cash_flow = stock.cashflow
#         balance_sheet = stock.balance_sheet  # Fetch balance sheet

#         return df, data, income_statement, cash_flow, balance_sheet

#     except Exception as e:
#         st.error(f"An error occurred: {e}")
#         return pd.DataFrame(), pd.DataFrame(), pd.DataFrame(), pd.DataFrame(), pd.DataFrame()

# # Helper function to fetch data
# def fetch_gap_data(ticker, from_date, to_date):
#     try:
#         stock = yf.Ticker(ticker)
#         data = stock.history(start=from_date, end=to_date)
#         return data
#     except Exception as e:
#         st.error(f"An error occurred: {e}")
#         return pd.DataFrame()

# # Main app
# st.title("Stock Analysis App")

# # Create tabs for different sections
# tab1, tab2, tab3 = st.tabs(["Stock Data", "Financial Statements", "Stock Analysis"])

# # Tab 1: Stock Data
# with tab1:
#     st.header("Stock Data")
#     df, data, _, _, _ = fetch_data(ticker, from_date, to_date, multiplier, timespan)

#     if not data.empty:
#         fig = px.line(data, x=data.index, y='Close', title=f"{ticker} Stock Prices",
#                       line_shape='linear',
#                       color_discrete_sequence=['#5AB834'])
#         st.plotly_chart(fig)
#     else:
#         st.error("No data available for the selected ticker.")

#     if df.empty:
#         st.error("No data available for the selected parameters. Please try different inputs.")
#     else:
#         df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
#         df.set_index('timestamp', inplace=True)
#         st.dataframe(df)

#         # Download button for Excel file
#         output_filename = f"{ticker}_stock_data_{from_date}_to_{to_date}.xlsx"
#         df.to_excel(output_filename, index=True)
#         st.success(f"Data fetched successfully and saved to '{output_filename}'.")
#         st.download_button(label="Download Excel File", data=open(output_filename, 'rb').read(),
#                            file_name=output_filename)

# # Tab 2: Financial Statements
# with tab2:
#     st.header("Financial Statements")
#     _, _, income_statement, cash_flow, balance_sheet = fetch_data(ticker, from_date, to_date, multiplier, timespan)

#     # Display Income Statement and Cash Flow
#     if not income_statement.empty:
#         st.subheader("Income Statement")
#         st.dataframe(income_statement)
#         # Download button for Income Statement
#         income_output_filename = f"{ticker}_income_statement.xlsx"
#         income_statement.to_excel(income_output_filename)
#         st.download_button(label="Download Income Statement", data=open(income_output_filename, 'rb').read(),
#                            file_name=income_output_filename)
#     else:
#         st.error("No income statement data available.")

#     if not cash_flow.empty:
#         st.subheader("Cash Flow Statement")
#         st.dataframe(cash_flow)
#         # Download button for Cash Flow
#         cash_flow_output_filename = f"{ticker}_cash_flow.xlsx"
#         cash_flow.to_excel(cash_flow_output_filename)
#         st.download_button(label="Download Cash Flow Statement", data=open(cash_flow_output_filename, 'rb').read(),
#                            file_name=cash_flow_output_filename)
#     else:
#         st.error("No cash flow data available.")

#     # Display Balance Sheet
#     if not balance_sheet.empty:
#         st.subheader("Balance Sheet")
#         st.dataframe(balance_sheet)
#         # Download button for Balance Sheet
#         balance_sheet_output_filename = f"{ticker}_balance_sheet.xlsx"
#         balance_sheet.to_excel(balance_sheet_output_filename)
#         st.download_button(label="Download Balance Sheet", data=open(balance_sheet_output_filename, 'rb').read(),
#                            file_name=balance_sheet_output_filename)
#     else:
#         st.error("No balance sheet data available.")

# # Tab 3: Stock Analysis
# with tab3:
#     st.header("Stock Analysis")
#     subtab1, subtab2 = st.tabs(["Stock Comparison", "Gap Analysis"])

#     # Sub-tab 1: Stock Comparison
#     with subtab1:
#         st.header("Stock Comparison")

#         # User inputs for stock comparison
#         st.markdown('<div class="input-container">', unsafe_allow_html=True)
#         col1, col2 = st.columns(2)

#         with col1:
#             ticker1 = st.text_input("Enter First Ticker Symbol (e.g., AAPL):", value="AAPL").upper()
#             multiplier1 = st.number_input("Enter Multiplier for First Ticker (e.g., 1 for minute data):", min_value=1, value=1, key='multiplier1')
#             timespan1 = st.selectbox("Select Timespan for First Ticker:",
#                                      options=["second", "minute", "hour", "day", "week", "month", "quarter", "year"],
#                                      index=0, key='timespan1')
#             from_date1 = st.date_input("Start Date for First Ticker:", value=pd.to_datetime("2024-01-01"), key='from_date1')
#             to_date1 = st.date_input("End Date for First Ticker:", value=pd.to_datetime("2024-09-30"), key='to_date1')

#         with col2:
#             ticker2 = st.text_input("Enter Second Ticker Symbol (e.g., MSFT):", value="MSFT").upper()
#             multiplier2 = st.number_input("Enter Multiplier for Second Ticker (e.g., 1 for minute data):", min_value=1, value=1, key='multiplier2')
#             timespan2 = st.selectbox("Select Timespan for Second Ticker:",
#                                      options=["second", "minute", "hour", "day", "week", "month", "quarter", "year"],
#                                      index=0, key='timespan2')
#             from_date2 = st.date_input("Start Date for Second Ticker:", value=pd.to_datetime("2024-01-01"), key='from_date2')
#             to_date2 = st.date_input("End Date for Second Ticker:", value=pd.to_datetime("2024-09-30"), key='to_date2')

#         st.markdown('</div>', unsafe_allow_html=True)

#         # Fetch data for both tickers
#         df1, data1, _, _, _ = fetch_data(ticker1, from_date1, to_date1, multiplier1, timespan1)
#         df2, data2, _, _, _ = fetch_data(ticker2, from_date2, to_date2, multiplier2, timespan2)

#         if not data1.empty and not data2.empty:
#             fig1 = px.line(data1, x=data1.index, y='Close', title=f"{ticker1} Stock Prices",
#                            line_shape='linear',
#                            color_discrete_sequence=['#FF7F0E'])
#             fig2 = px.line(data2, x=data2.index, y='Close', title=f"{ticker2} Stock Prices",
#                            line_shape='linear',
#                            color_discrete_sequence=['#1F77B4'])

#             st.subheader(f"Comparison of {ticker1} and {ticker2}")
#             col1, col2 = st.columns(2)

#             with col1:
#                 st.plotly_chart(fig1)

#             with col2:
#                 st.plotly_chart(fig2)

#             comparison_df = pd.DataFrame({
#                 'Metrics': ['Highest Open Value', 'Lowest Close Value'],
#                 f'{ticker1}': [data1['Open'].max(), data1['Close'].min()],
#                 f'{ticker2}': [data2['Open'].max(), data2['Close'].min()]
#             })

#             st.subheader("Comparison Summary")
#             st.dataframe(comparison_df)

#         else:
#             st.error("No data available for one or both tickers.")


#     # Sub-tab 2: Gap Analysis
#     # Helper function to fetch gap data
#     def fetch_gap_data(ticker, from_date, to_date):
#         try:
#             stock = yf.Ticker(ticker)
#             data = stock.history(start=from_date, end=to_date)
#             return data
#         except Exception as e:
#             st.error(f"An error occurred: {e}")
#             return pd.DataFrame()


#     # Function to add colored KPI symbols for Gap %
#     def add_kpi_symbols(row):
#         if row['Gap %'] > 0:
#             return f"<span style='color: green;'>▲ {row['Gap %']:.2f}%</span>"
#         elif row['Gap %'] < 0:
#             return f"<span style='color: red;'>🔻 {row['Gap %']:.2f}%</span>"
#         else:
#             return f"<span>➖ {row['Gap %']:.2f}%</span>"


#     # Sub-tab 2: Gap Analysis
#     with subtab2:
#         st.header("Gap Analysis")

#         # User inputs for gap analysis
#         gap_ticker = st.text_input("Enter Ticker Symbol for Gap Analysis:", value="AAPL").upper()
#         gap_from_date = st.date_input("Start Date for Gap Analysis:", value=pd.to_datetime("2024-01-01"))
#         gap_to_date = st.date_input("End Date for Gap Analysis:", value=pd.to_datetime("2024-09-30"))

#         gap_data = fetch_gap_data(gap_ticker, gap_from_date, gap_to_date)

#         if not gap_data.empty:
#             # Calculate weekly high, low, opening, closing, and volume
#             gap_data['Week'] = gap_data.index.to_period('W')
#             weekly_data = gap_data.groupby('Week').agg(
#                 Highest_in_week=('High', 'max'),
#                 Lowest_in_week=('Low', 'min'),
#                 Opening_week=('Open', 'first'),
#                 Closing_week=('Close', 'last'),
#                 Volume=('Volume', 'sum')
#             ).reset_index()



#             # Calculate the week start and end dates
#             weekly_data['Week Start'] = weekly_data['Week'].apply(lambda x: x.start_time.strftime('%Y-%m-%d'))
#             weekly_data['Week End'] = weekly_data['Week'].apply(
#                 lambda x: (x.end_time - pd.Timedelta(days=2)).strftime('%Y-%m-%d'))
#             weekly_data['Week Range'] = weekly_data['Week Start'] + ' - ' + weekly_data['Week End']

#             # Add a "Week Number" column that shows Week 1, Week 2, etc.
#             weekly_data['Week Number'] = 'Week ' + (weekly_data.index + 1).astype(str)

#             # Calculate gap and gap percentage
#             weekly_data['Gap'] = weekly_data['Closing_week'].shift(-2) - weekly_data['Opening_week']
#             weekly_data['Gap %'] = (weekly_data['Gap'] / weekly_data['Opening_week'].shift(-1)) * 100

#             # Add KPI symbols column
#             weekly_data['Gap % with KPI'] = weekly_data.apply(add_kpi_symbols, axis=1)

#             # Select only the relevant columns, including "Week Range"
#             display_data = weekly_data[
#                 ['Week Number', 'Week Range', 'Highest_in_week', 'Lowest_in_week', 'Opening_week', 'Closing_week',
#                  'Volume', 'Gap % with KPI']]

#             # Set custom style to prevent wrapping and center-align the table
#             st.write("""
#             <style>
#             .table-container {
#                 width: auto;
#                 max-width: 100%;
#                 margin: auto;
#                 text-align: center;
#                 white-space: nowrap;
#                 overflow-x: auto;
#             }
#             .table-container table {
#                 margin: auto;
#             }
#             .summary-heading {
#                 margin: 0; /* Remove margin from the heading */
#             }
#             .summary-table-container {
#                 display: flex;
#                 justify-content: center;
#                 align-items: center;
#                 width: 100%;
#                 margin: 0; /* Remove margin from the table container */
#             }
#             .summary-table {
#                 width: auto;
#                 max-width: 80%; /* Adjust as needed */
#                 border-collapse: collapse;
#                 text-align: center;
#             }
#             .summary-table th, .summary-table td {
#                 border: 2px solid #ddd;
#                 padding: 10px;
#             }
#             .summary-table th {
#                 background-color: #f2f2f2;
#                 color: #333;
#             }
#             .summary-table td {
#                 background-color: #f9f9f9;
#             }
#             </style>
#             """, unsafe_allow_html=True)

#             # Display the table with custom style
#             st.write('<div class="table-container">' + display_data.to_html(index=False, escape=False) + '</div>',
#                      unsafe_allow_html=True)

#             # Calculate Gap Analysis Summary
#             highest_gap_row = weekly_data.loc[weekly_data['Gap %'].idxmax()]  # Find the row with the highest gap %

#             # Create a summary DataFrame
#             summary_df = pd.DataFrame({
#                 'Metrics': ['Week Number', 'Highest in Week', 'Lowest in Week', 'Opening in Week', 'Closing in Week',
#                             'Volume', 'Highest Gap %'],
#                 'Value': [
#                     highest_gap_row['Week Number'],
#                     f"{highest_gap_row['Highest_in_week']:.2f}",
#                     f"{highest_gap_row['Lowest_in_week']:.2f}",
#                     f"{highest_gap_row['Opening_week']:.2f}",
#                     f"{highest_gap_row['Closing_week']:.2f}",
#                     f"{highest_gap_row['Volume']:,}",
#                     highest_gap_row['Gap % with KPI']
#                 ]
#             })
#             if not gap_data.empty:
#                 gap_data['Gap'] = gap_data['Close'] - gap_data['Close'].shift(1)
#                 gap_data.dropna(inplace=True)

#                 st.subheader("Gap Analysis Data")
#                 st.dataframe(gap_data[['Open', 'Close', 'Gap']])

#                 # Graph for Gap Analysis
#                 fig = px.line(gap_data, x=gap_data.index, y='Gap', title=f"{gap_ticker} Gap Analysis",
#                               line_shape='linear', color_discrete_sequence=['#FF6347'])
#                 st.plotly_chart(fig)

#             # Display the summary DataFrame with st.write and HTML for KPI symbols
#             st.subheader("Gap Analysis Summary")
#             st.write('<div class="summary-heading"></div>', unsafe_allow_html=True)
#             st.write(
#                 '<div class="summary-table-container"><table class="summary-table">' + summary_df.to_html(index=False,
#                                                                                                           escape=False) + '</table></div>',
#                 unsafe_allow_html=True)

#         else:
#             st.error("No data available for the selected ticker and date range.")

# # Footer
# st.markdown('<div class="footer">Powered by Naf-Byte (Nafay Ur Rehman)</div>', unsafe_allow_html=True)
