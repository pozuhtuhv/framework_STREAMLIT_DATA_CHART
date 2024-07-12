import streamlit as st
import polars as pl
import plotly.express as px
import yfinance as yf
from datetime import date

def main():

    # Streamlit app setting
    st.header("Live Chart", divider='blue')

    # Sidebar Dropbox area
    st.sidebar.title("Chart_Control")
    ticker_symbol = st.sidebar.selectbox("Symbol",["TQQQ","CONY"])

    startdate = str(st.sidebar.date_input("Select a start date", date.today()))
    endtdate = str(st.sidebar.date_input("Select an end date", date.today()))

    ticker = yf.Ticker(ticker_symbol)

    # 지정 데이터 가져오기
    raw_data = ticker.history(period='1d', start=startdate,end=endtdate)

    # Polars 데이터로 변환
    df = pl.DataFrame(raw_data.reset_index())

    # Polars dataframe load confirm
    # print("Polars DataFrame columns:", df.columns)

    # 'Stock Splits', 'Capital Gains' 열 삭제
    df = df.drop(df.columns[-2:])

    dividends_data = df.drop(columns=['Open', 'High', 'Low', 'Close', 'Volume'])

    line_dividends_data = dividends_data.filter(pl.col("Dividends") != 0.0)

    # data load confirm
    print(dividends_data)
    # new chart
    st.header("Stock Data Chart")
    fig = px.line(line_dividends_data, x='Date', y='Dividends')
    fig.update_layout(hovermode='x unified') # tooltip set
    st.plotly_chart(fig)

    # data table view
    st.header("Live Data Table")
    st.dataframe(df)

if __name__ == "__main__":
    main()

# streamlit run Stock_info_chart.py
